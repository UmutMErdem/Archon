"""Create a persona draft from PERSONA_TEMPLATE.md and register it.

Registers the persona in detection_signals.md, README.md and architecture/00_detection.md,
then runs sync_matrix.py and validate_manifesto.py. The draft keeps the template's
<placeholders> for the sections only a domain expert can write, so the validator fails
until they are filled in.
"""

import argparse
import json
import os
import re
import subprocess
import sys

from archon_core import (
    DETECTION_PATH,
    PERSONAS_DIR,
    README_PATH,
    REPO_ROOT,
    SIGNALS_PATH,
    TEMPLATE_PATH,
    load_registry,
    read_text,
    setup_utf8,
    write_text,
)

FILENAME_RE = re.compile(r"[a-z0-9_]+\.md")
DETECTION_QUESTION_RE = re.compile(
    r'^(> "What is the technical domain of this project\? \(e\.g\., .*?)\)"$', re.M
)
README_COUNT_RE = re.compile(r"Domain Expert Personas \((\d+) personas\)")
README_LAST_PERSONA_RE = re.compile(
    r"^(\[\w+\.md\]\(personas/\w+\.md\)(?:, \[\w+\.md\]\(personas/\w+\.md\))*)$", re.M
)


def prompt(text):
    sys.stdout.write(text)
    sys.stdout.flush()
    return sys.stdin.readline().strip()


def yaml_str(value):
    # A JSON string literal is a valid YAML double-quoted scalar.
    return json.dumps(value, ensure_ascii=False)


def render_persona(template, domain, role, expertise, interfaces):
    body = re.sub(r"<!--\nHOW TO USE THIS TEMPLATE.*?-->\n+", "", template, flags=re.S)
    body = body.replace("<Domain Name>", domain).replace("<Senior Title>", role)
    body = body.replace(
        "<core skills, technologies, protocols, and sub-disciplines that define this domain>",
        expertise,
    )
    lines = [f"- **→ {label}:** <shared contract, artifact, or boundary>" for label in interfaces]
    body = re.sub(
        r"(## Cross-Domain Interfaces\n(?:<!--[^\n]*-->\n)?)(?:- \*\*→ [^\n]*\n?)+",
        lambda m: m.group(1) + "\n".join(lines) + "\n",
        body,
    )
    frontmatter = (
        "---\n"
        f"domain: {yaml_str(domain)}\n"
        f"expert_role: {yaml_str(f'You are a {role} with expertise in {expertise}.')}\n"
        'inherits: "none"\n'
        "---\n\n"
    )
    return frontmatter + body


def register_signals(signals_md, filename, domain, label, signals):
    if f"`personas/{filename}`" in signals_md:
        return signals_md, False
    row = f"| {signals} | {domain} | `personas/{filename}` | {label} | — |"
    return signals_md.rstrip("\n") + "\n" + row + "\n", True


def register_detection(detection_md, label):
    m = DETECTION_QUESTION_RE.search(detection_md)
    if not m:
        return detection_md, None
    if label in [s.strip() for s in m.group(1).split("(e.g., ", 1)[1].split(",")]:
        return detection_md, False
    return detection_md[: m.end(1)] + f", {label}" + detection_md[m.end(1) :], True


def register_readme(readme_md, filename):
    if f"(personas/{filename})" in readme_md:
        return readme_md, False
    count = README_COUNT_RE.search(readme_md)
    lists = list(README_LAST_PERSONA_RE.finditer(readme_md))
    if not count or not lists:
        return readme_md, None
    last = lists[-1]
    readme_md = (
        readme_md[: last.end(1)] + f", [{filename}](personas/{filename})" + readme_md[last.end(1) :]
    )
    n = int(count.group(1))
    return readme_md.replace(count.group(0), f"Domain Expert Personas ({n + 1} personas)"), True


def apply(path, transform, *args):
    new, changed = transform(read_text(path), *args)
    name = os.path.relpath(path, REPO_ROOT).replace(os.sep, "/")
    if changed is None:
        print(f"❌ Could not register in {name}: anchor not found, add it manually")
        return False
    if changed:
        write_text(path, new)
        print(f"✅ Registered in {name}")
    else:
        print(f"ℹ️  Already registered in {name}")
    return True


def gather(args):
    fields = [
        ("domain", "Domain name (e.g., Quantum Computing): "),
        ("filename", "Persona filename (e.g., quantum_computing.md): "),
        ("label", "Canonical interface label (e.g., Quantum): "),
        ("role", "Expert role title (e.g., Senior Quantum Software Engineer): "),
        ("expertise", "Expertise summary (e.g., circuit design, error mitigation, Qiskit): "),
        ("signals", "Detection signals, markdown (e.g., `*.qasm`, `qiskit` imports): "),
        (
            "interfaces",
            "Interface targets, comma-separated canonical labels (e.g., AI/ML, DevOps): ",
        ),
    ]
    for name, text in fields:
        if getattr(args, name) is None:
            setattr(args, name, prompt(text))
    return args


def validate_args(args, labels):
    errors = []
    for name in ("domain", "label", "role", "expertise", "signals", "interfaces"):
        if not getattr(args, name):
            errors.append(f"--{name} must not be empty")
    if args.filename and not args.filename.endswith(".md"):
        args.filename += ".md"
    if not FILENAME_RE.fullmatch(args.filename or ""):
        errors.append("--filename must match [a-z0-9_]+.md (no paths)")
    if args.label in labels:
        errors.append(f"--label '{args.label}' is already used by another persona")
    if "`" not in (args.signals or ""):
        errors.append("--signals must contain at least one `backticked` file pattern")
    targets = [t.strip() for t in (args.interfaces or "").split(",") if t.strip()]
    unknown = [t for t in targets if t not in labels]
    if unknown:
        errors.append(f"unknown interface labels {unknown}; use: {sorted(labels)}")
    args.interfaces = targets
    return errors


def main(argv=None):
    setup_utf8()
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    for name in ("domain", "filename", "label", "role", "expertise", "signals", "interfaces"):
        parser.add_argument(f"--{name}")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing persona file")
    args = gather(parser.parse_args(argv))

    errors = validate_args(args, {row["label"] for row in load_registry(SIGNALS_PATH).values()})
    if errors:
        for e in errors:
            print(f"❌ {e}")
        return 2

    target = os.path.join(PERSONAS_DIR, args.filename)
    if os.path.exists(target) and not args.force:
        print(f"❌ personas/{args.filename} already exists (use --force to overwrite)")
        return 2

    write_text(
        target,
        render_persona(
            read_text(TEMPLATE_PATH), args.domain, args.role, args.expertise, args.interfaces
        ),
    )
    print(f"✅ Created personas/{args.filename}")

    ok = apply(SIGNALS_PATH, register_signals, args.filename, args.domain, args.label, args.signals)
    ok &= apply(README_PATH, register_readme, args.filename)
    ok &= apply(DETECTION_PATH, register_detection, args.label)

    print(
        "\nNext steps:\n"
        "  1. Fill in every <placeholder> in the new persona\n"
        f"  2. Add a reciprocal '- **→ {args.label}:**' bullet in each interface target persona\n"
        "  3. Add the persona's standards to compliance.md\n"
        "  4. Run python scripts/sync_matrix.py && python scripts/validate_manifesto.py\n"
    )
    result = subprocess.run(
        [sys.executable, os.path.join(REPO_ROOT, "scripts", "validate_manifesto.py")],
        check=False,
    )
    return 1 if (not ok or result.returncode) else 0


if __name__ == "__main__":
    sys.exit(main())
