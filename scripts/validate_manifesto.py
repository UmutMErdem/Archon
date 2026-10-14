"""Archon manifesto linter. Every finding except persona size is an error (exit 1)."""

import argparse
import fnmatch
import os
import re
import subprocess
import sys
import urllib.parse
from collections import Counter

import sync_matrix
from archon_core import (
    COMPLIANCE_PATH,
    DETECTION_PATH,
    INHERIT_PRIMARY,
    MATRIX_PATH,
    PERSONAS_DIR,
    README_PATH,
    REPO_ROOT,
    REQUIRED_HEADINGS,
    SIGNALS_PATH,
    iter_interfaces,
    list_persona_files,
    load_registry,
    parse_frontmatter,
    read_text,
    resolve_domain_to_persona_file,
    section_bullets,
    setup_utf8,
)

MIN_PERSONA_LINES = 30
MAX_PERSONA_LINES = 200

REQUIRED_FRONTMATTER_KEYS = ["domain", "expert_role", "inherits"]
PLACEHOLDER_RE = re.compile(r"<[A-Za-z][^<>\n]{2,}>")
EXTENSION_GLOB_RE = re.compile(r"\*\.[\w.]+")
SKIP_DIRS = {
    ".git",
    ".arena",
    ".venv",
    "venv",
    "node_modules",
    "graphify-out",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
}


def compliance_key(text):
    """Identifier part of a standard: the text before the first ` (` or ` —`."""
    return re.split(r"\s+\(|\s+—", text.strip(), maxsplit=1)[0].strip()


def split_ids(key):
    # Only a spaced slash separates IDs, so `ISO/IEC 27001` and `TCP/IP` stay whole.
    return [p.strip() for p in re.split(r"\s+/\s+", key) if p.strip()]


def canonical_compliance_ids(compliance_md):
    ids = set()
    for line in compliance_md.splitlines():
        if not line.startswith("|") or line.startswith("|---"):
            continue
        cell = line.split("|")[1].strip()
        if not cell or cell in ("Standard", "Practice"):
            continue
        key = compliance_key(cell)
        ids.add(key)
        ids.update(split_ids(key))
    return ids


def check_compliance_ids(content, ids):
    errors = []
    for bullet in section_bullets(content, "## Compliance & Standards"):
        key = compliance_key(bullet)
        if key not in ids and not all(p in ids for p in split_ids(key)):
            errors.append(f"Compliance ID '{key}' not found in compliance.md column 1")
    return errors


def check_template_integrity(content):
    errors = []
    meta, fm_err = parse_frontmatter(content)
    if fm_err:
        return [f"Frontmatter error: {fm_err}"]
    for key in REQUIRED_FRONTMATTER_KEYS:
        if key not in meta:
            errors.append(f"Frontmatter missing required key: '{key}'")
        elif meta[key] in ("", [], {}):
            errors.append(f"Frontmatter key '{key}' is empty")
    for heading in REQUIRED_HEADINGS:
        if not re.search(r"^" + re.escape(heading), content, re.MULTILINE):
            errors.append(f"Missing required heading: '{heading.strip()}'")
    return errors


def check_inherits(content, persona_files):
    meta, fm_err = parse_frontmatter(content)
    if fm_err or "inherits" not in meta:
        return []
    inherits = meta["inherits"]
    if inherits == "none":
        return []
    if not isinstance(inherits, dict) or "base" not in inherits:
        return ["'inherits' must be \"none\" or a block with a 'base' key"]
    errors = []
    base = inherits["base"]
    if base != INHERIT_PRIMARY and base not in persona_files:
        errors.append(f"inherits.base '{base}' does not exist in personas/")
    for key in ("base_reason", "overrides"):
        if not inherits.get(key):
            errors.append(f"inherits.{key} is missing or empty")
    return errors


def check_placeholders(content):
    return [f"Unfilled placeholder '{m}'" for m in PLACEHOLDER_RE.findall(content)]


def check_frontmatter_body_consistency(content):
    meta, fm_err = parse_frontmatter(content)
    if fm_err or not meta:
        return []
    errors = []

    fm_role = meta.get("expert_role", "")
    body = re.search(r"## Expert Role\s*>\s*You are an? \*\*(.+?)\*\*", content)
    if body and fm_role and body.group(1).strip().lower() not in fm_role.lower():
        errors.append(
            f"Frontmatter expert_role does not contain body Expert Role title '{body.group(1).strip()}'"
        )

    fm_domain = meta.get("domain", "")
    title = re.search(r"^# (.+?) Persona", content, re.MULTILINE)
    if title and fm_domain:
        fm_words = set(re.findall(r"[a-z]{3,}", fm_domain.lower()))
        body_words = set(re.findall(r"[a-z]{3,}", title.group(1).lower()))
        smaller, larger = sorted((fm_words, body_words), key=len)
        matched = sum(
            1 for s in smaller if any(s[:5] == w[: min(len(s), len(w), 5)] for w in larger)
        )
        if smaller and matched < len(smaller) * 0.5:
            errors.append(
                f"Frontmatter domain '{fm_domain}' does not match heading '# {title.group(1).strip()} Persona'"
            )
    return errors


def check_persona_size(persona_path):
    with open(persona_path, encoding="utf-8") as f:
        line_count = sum(1 for _ in f)
    name = os.path.basename(persona_path)
    if line_count < MIN_PERSONA_LINES:
        return [f"{name}: Too short ({line_count} lines, minimum {MIN_PERSONA_LINES})"]
    if line_count > MAX_PERSONA_LINES:
        return [f"{name}: Too long ({line_count} lines, maximum {MAX_PERSONA_LINES})"]
    return []


def check_registry(registry, persona_files):
    on_disk = set(persona_files)
    errors = [
        f"detection_signals.md references missing personas/{f}"
        for f in sorted(set(registry) - on_disk)
    ]
    errors += [
        f"personas/{f} is not registered in detection_signals.md"
        for f in sorted(on_disk - set(registry))
    ]
    labels = Counter(row["label"] for row in registry.values())
    errors += [
        f"detection_signals.md: interface label '{label}' is used by {n} personas"
        for label, n in sorted(labels.items())
        if n > 1
    ]
    errors += [
        f"detection_signals.md: personas/{f} has an empty Interface Label"
        for f, row in sorted(registry.items())
        if not row["label"] or row["label"] == "—"
    ]

    readme = read_text(README_PATH) if os.path.exists(README_PATH) else ""
    errors += [
        f"personas/{f} is not listed in README.md"
        for f in sorted(on_disk)
        if f"(personas/{f})" not in readme
    ]
    count = re.search(r"Domain Expert Personas \((\d+) personas\)", readme)
    if not count or int(count.group(1)) != len(on_disk):
        errors.append(f"README.md persona count is not '({len(on_disk)} personas)'")

    detection = read_text(DETECTION_PATH) if os.path.exists(DETECTION_PATH) else ""
    question = re.search(r"technical domain of this project\? \(e\.g\., (.*?)\)\"", detection)
    listed = {s.strip() for s in question.group(1).split(",")} if question else set()
    errors += [
        f"architecture/00_detection.md Step 1 question does not list '{registry[f]['label']}'"
        for f in sorted(on_disk & set(registry))
        if registry[f]["label"] not in listed
    ]
    return errors


def check_interfaces(contents, registry):
    """Labels must be canonical and resolvable, unique per persona, and symmetric."""
    errors = []
    canonical = {row["label"] for row in registry.values()}
    links = {}
    for pf, content in contents.items():
        targets = []
        for label, _ in iter_interfaces(content):
            target = resolve_domain_to_persona_file(label, registry)
            if target is None:
                errors.append(f"UNRESOLVED: {pf}: interface target '{label}' matches no persona")
                continue
            if label not in canonical:
                errors.append(
                    f"LABEL: {pf}: '{label}' is not canonical, use '{registry[target]['label']}'"
                )
            if target == pf:
                errors.append(f"SELF: {pf}: interface points to itself")
            targets.append(target)
        for target, n in Counter(targets).items():
            if n > 1:
                errors.append(f"DUPLICATE: {pf}: {n} bullets point to {target}, merge them")
        links[pf] = set(targets)

    for source, targets in sorted(links.items()):
        for target in sorted(targets):
            if source not in links.get(target, set()):
                errors.append(
                    f"ASYMMETRY: {source} → {target}, but {target} has no '→ {registry.get(source, {}).get('label', source)}' bullet"
                )
    return errors


def _signal_globs(cell):
    globs = []
    for token in re.findall(r"`([^`]+)`", cell):
        globs += [g.strip() for g in re.split(r",\s*", token) if g.strip()]
    return globs


def _glob_overlap(a, b):
    """Exact duplicates, or one specific pattern matching another. A bare `*.ext` glob
    overlapping a named file is expected: the more specific signal wins (00_detection.md)."""
    if a == b:
        return True
    if EXTENSION_GLOB_RE.fullmatch(a) or EXTENSION_GLOB_RE.fullmatch(b):
        return False
    wild = set("*?[")
    if not (wild & set(a)) and fnmatch.fnmatch(a, b):
        return True
    return not (wild & set(b)) and fnmatch.fnmatch(b, a)


def check_signal_collisions(registry):
    rows = [
        (f"personas/{f}", _signal_globs(row["signals"] + " " + row["weak"]))
        for f, row in sorted(registry.items())
    ]
    errors = []
    for i, (pa, ga) in enumerate(rows):
        for pb, gb in rows[i + 1 :]:
            for a in ga:
                for b in gb:
                    if _glob_overlap(a, b):
                        errors.append(f"Signal '{a}' ({pa}) overlaps '{b}' ({pb})")
    return errors


def check_matrix_sync():
    expected = sync_matrix.render_matrix(*sync_matrix.collect())
    current = read_text(MATRIX_PATH) if os.path.exists(MATRIX_PATH) else ""
    if current != expected:
        return ["CROSS_DOMAIN_MATRIX.md is stale. Run: python scripts/sync_matrix.py"]
    return []


def github_slug(heading):
    slug = heading.strip().lower()
    slug = re.sub(r"[^\w\- ]", "", slug)
    return slug.replace(" ", "-")


def heading_slugs(md_text):
    slugs, seen = set(), Counter()
    in_fence = False
    for line in md_text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        m = None if in_fence else re.match(r"^#{1,6}\s+(.*?)\s*#*\s*$", line)
        if m:
            base = github_slug(m.group(1))
            slugs.add(base if not seen[base] else f"{base}-{seen[base]}")
            seen[base] += 1
    return slugs


def _markdown_files():
    try:
        out = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "*.md"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.split()
        return [
            os.path.join(REPO_ROOT, p)
            for p in out
            if not SKIP_DIRS & set(p.split("/")) and os.path.exists(os.path.join(REPO_ROOT, p))
        ]
    except (OSError, subprocess.CalledProcessError):
        files = []
        for root, dirs, names in os.walk(REPO_ROOT):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            files += [os.path.join(root, n) for n in names if n.endswith(".md")]
        return files


def _display_path(path):
    try:
        return os.path.relpath(path, REPO_ROOT).replace(os.sep, "/")
    except ValueError:  # different drive on Windows
        return path


def check_broken_links(md_files=None):
    errors = []
    md_files = md_files if md_files is not None else _markdown_files()
    slug_cache = {}
    for md_path in sorted(md_files):
        content = read_text(md_path)
        text = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
        text = re.sub(r"`[^`\n]*`", "", text)
        rel = _display_path(md_path)
        for _, url in re.findall(r"\[([^\]]+)\]\(([^)\s]+)\)", text):
            if url.startswith(("http://", "https://", "mailto:")):
                continue
            if url.startswith("file:"):
                errors.append(f"{rel}: machine-specific link '{url}'")
                continue
            path_part, _, anchor = url.partition("#")
            target = (
                md_path
                if not path_part
                else os.path.normpath(
                    os.path.join(os.path.dirname(md_path), urllib.parse.unquote(path_part))
                )
            )
            if not os.path.exists(target):
                errors.append(f"{rel}: broken link '{url}'")
                continue
            if anchor and target.endswith(".md"):
                if target not in slug_cache:
                    slug_cache[target] = heading_slugs(read_text(target))
                if anchor.lower() not in slug_cache[target]:
                    errors.append(f"{rel}: broken anchor '{url}'")
    return errors


def run():
    """Run every check. Returns (errors, warnings) as lists of (category, message)."""
    errors, warnings = [], []
    registry = load_registry(SIGNALS_PATH)
    if not registry:
        return [("CONFIG", f"{SIGNALS_PATH} not found or has no persona rows")], []
    compliance_ids = canonical_compliance_ids(read_text(COMPLIANCE_PATH))
    persona_files = list_persona_files(PERSONAS_DIR)
    contents = {pf: read_text(os.path.join(PERSONAS_DIR, pf)) for pf in persona_files}

    for pf, content in contents.items():
        for category, found in (
            ("TEMPLATE", check_template_integrity(content)),
            ("INHERITS", check_inherits(content, persona_files)),
            ("PLACEHOLDER", check_placeholders(content)),
            ("CONSISTENCY", check_frontmatter_body_consistency(content)),
            ("COMPLIANCE", check_compliance_ids(content, compliance_ids)),
        ):
            errors += [(category, f"personas/{pf}: {msg}") for msg in found]
        warnings += [("SIZE", w) for w in check_persona_size(os.path.join(PERSONAS_DIR, pf))]

    errors += [("REGISTRY", e) for e in check_registry(registry, persona_files)]
    errors += [("INTERFACE", e) for e in check_interfaces(contents, registry)]
    errors += [("SIGNALS", e) for e in check_signal_collisions(registry)]
    errors += [("MATRIX", e) for e in check_matrix_sync()]
    errors += [("LINK", e) for e in check_broken_links()]
    return errors, warnings


def main(argv=None):
    setup_utf8()
    argparse.ArgumentParser(description=__doc__).parse_args(argv)
    print("🛡️  Archon manifesto validator")
    errors, warnings = run()
    for category, msg in warnings:
        print(f"  ⚠️  {category}: {msg}")
    for category, msg in errors:
        print(f"  ❌ {category}: {msg}")
    counts = Counter(c for c, _ in errors)
    if errors:
        summary = ", ".join(f"{c}={n}" for c, n in sorted(counts.items()))
        print(f"\n❌ {len(errors)} error(s): {summary}")
        return 1
    print(f"\n✅ Manifesto is clean ({len(warnings)} warning(s)).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
