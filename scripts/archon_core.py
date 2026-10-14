"""Shared parsing, naming and path helpers for every Archon script."""

import contextlib
import os
import re
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PERSONAS_DIR = os.path.join(REPO_ROOT, "personas")
SIGNALS_PATH = os.path.join(REPO_ROOT, "detection_signals.md")
COMPLIANCE_PATH = os.path.join(REPO_ROOT, "compliance.md")
MATRIX_PATH = os.path.join(REPO_ROOT, "CROSS_DOMAIN_MATRIX.md")
README_PATH = os.path.join(REPO_ROOT, "README.md")
DETECTION_PATH = os.path.join(REPO_ROOT, "architecture", "00_detection.md")
TEMPLATE_PATH = os.path.join(REPO_ROOT, "PERSONA_TEMPLATE.md")
FILES_SPEC_PATH = os.path.join(REPO_ROOT, "architecture", "files_spec.md")

REQUIRED_HEADINGS = [
    "## Expert Role",
    "## Hard Rules",
    "## Domain-Specific Discovery Questions",
    "## Key Focus Areas for ARCHITECTURE.md",
    "### System Mapping → ",
    "### Detailed Specifications",
    "### Performance Budget",
    "### Domain-Specific Sections",
    "## Compliance & Standards",
    "## Common Pitfalls",
    "## Recommended Toolchain",
    "## Domain-Specific Testing",
    "## Cross-Domain Interfaces",
]

INTERFACE_RE = re.compile(r"^-\s*\*\*→\s*([^*:]+?)\s*(?::\*\*|\*\*:)\s*(.*)$")
INHERIT_PRIMARY = "$primary"

COMPLETENESS_LEVELS = [
    (22, "Sparse"),
    (26, "Moderate"),
    (32, "Thorough"),
    (float("inf"), "Comprehensive"),
]


def setup_utf8():
    for stream in (sys.stdout, sys.stderr):
        with contextlib.suppress(AttributeError):
            stream.reconfigure(encoding="utf-8")


def read_text(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write_text(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def list_persona_files(personas_dir=PERSONAS_DIR):
    return sorted(f for f in os.listdir(personas_dir) if f.endswith(".md"))


def _parse_scalar(value):
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        return [a or b for a, b in re.findall(r'"([^"]*)"|\'([^\']*)\'', value[1:-1])]
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_frontmatter(content):
    """Return (metadata, error). One level of nesting is supported (e.g. `inherits:`)."""
    if not content.lstrip().startswith("---"):
        return None, "Missing frontmatter start marker '---'"
    parts = content.lstrip().split("---", 2)
    if len(parts) < 3:
        return None, "Missing frontmatter end marker '---'"

    meta = {}
    parent = None
    for raw in parts[1].splitlines():
        if not raw.strip() or raw.strip().startswith("#") or ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        nested = raw[:1] in (" ", "\t")
        key = key.strip()
        if nested and parent is not None:
            meta[parent][key] = _parse_scalar(value)
            continue
        if value.strip() == "":
            meta[key] = {}
            parent = key
        else:
            meta[key] = _parse_scalar(value)
            parent = None
    return meta, None


def extract_section(content, heading):
    """Body of a heading, up to the next heading of the same or a higher level, or EOF."""
    level = len(heading) - len(heading.lstrip("#"))
    m = re.search(
        r"^" + re.escape(heading) + r"[^\n]*\n(.*?)(?=^#{1," + str(level) + r"} |\Z)",
        content,
        re.DOTALL | re.MULTILINE,
    )
    return m.group(1) if m else None


def section_bullets(content, heading):
    body = extract_section(content, heading) or ""
    return [line.strip()[2:].strip() for line in body.splitlines() if line.strip().startswith("- ")]


def iter_interfaces(content):
    """(target_label, description) for every `- **→ Label:** text` bullet."""
    out = []
    for line in (extract_section(content, "## Cross-Domain Interfaces") or "").splitlines():
        m = INTERFACE_RE.match(line.strip())
        if m:
            out.append((m.group(1).strip(), m.group(2).strip()))
    return out


def count_sections(content):
    return sum(
        1 for h in REQUIRED_HEADINGS if re.search(r"^" + re.escape(h), content, re.MULTILINE)
    )


def completeness(content):
    sections = count_sections(content)
    interfaces = len(iter_interfaces(content))
    compliance = len(section_bullets(content, "## Compliance & Standards"))
    score = sections + interfaces + compliance
    label = next(name for limit, name in COMPLETENESS_LEVELS if score <= limit)
    return {
        "sections": sections,
        "interfaces": interfaces,
        "compliance": compliance,
        "score": score,
        "label": label,
    }


def load_registry(signals_path=SIGNALS_PATH):
    """persona file -> {domain, label, signals, weak} from the detection_signals.md table."""
    if not os.path.exists(signals_path):
        return {}
    registry = {}
    for line in read_text(signals_path).splitlines():
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 7 and parts[3].startswith("`personas/"):
            registry[parts[3].strip("`").replace("personas/", "")] = {
                "signals": parts[1],
                "domain": parts[2],
                "label": parts[4],
                "weak": parts[5],
            }
    return registry


def _norm(text):
    return re.sub(r"[\s/&:_()-]", "", text).lower()


def resolve_domain_to_persona_file(label, registry):
    """Exact (normalized) match on interface label, domain name or file stem."""
    key = _norm(label)
    for fn, row in registry.items():
        if key in (_norm(row["label"]), _norm(row["domain"]), _norm(fn[:-3])):
            return fn
    return None


def display_name(persona_file, registry):
    row = registry.get(persona_file)
    return row["label"] if row else persona_file[:-3].replace("_", " ").title()


def node_id(persona_file):
    return persona_file[:-3].replace("_", "")
