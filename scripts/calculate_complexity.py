import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except AttributeError:
    pass

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PERSONAS_DIR = os.path.join(REPO_ROOT, "personas")
SIGNALS_PATH = os.path.join(REPO_ROOT, "detection_signals.md")

REQUIRED_HEADINGS = [
    r"^## Expert Role",
    r"^## Domain-Specific Discovery Questions",
    r"^## Key Focus Areas for ARCHITECTURE\.md",
    r"^### System Mapping",
    r"^### Detailed Specifications",
    r"^### Performance Budget",
    r"^### Domain-Specific Sections",
    r"^## Compliance & Standards",
    r"^## Common Pitfalls",
    r"^## Recommended Toolchain",
    r"^## Domain-Specific Testing",
    r"^## Cross-Domain Interfaces",
]


def count_sections(content):
    count = 0
    for pattern in REQUIRED_HEADINGS:
        if re.search(pattern, content, re.MULTILINE):
            count += 1
    return count


def count_interfaces(content):
    match = re.search(
        r"## Cross-Domain Interfaces\s*(.*?)(?:\n## |\Z)", content, re.DOTALL
    )
    if not match:
        return 0
    block = match.group(1)
    return len(re.findall(r"^\s*-\s*\*\*→", block, re.MULTILINE))


def count_compliance(content):
    match = re.search(
        r"## Compliance & Standards\s*(.*?)(?:\n## |\Z)", content, re.DOTALL
    )
    if not match:
        return 0
    block = match.group(1)
    return len([line for line in block.splitlines() if line.strip().startswith("-")])


def score_label(score):
    if score <= 22:
        return "Sparse"
    elif score <= 26:
        return "Moderate"
    elif score <= 32:
        return "Thorough"
    else:
        return "Comprehensive"


def main():
    print("Calculating persona completeness scores...\n")

    scores = {}
    persona_files = sorted([f for f in os.listdir(PERSONAS_DIR) if f.endswith(".md")])

    print(
        f"{'Persona':<30} {'Sections':>8} {'Interfaces':>10} {'Compliance':>10} {'Score':>6} {'Label':>10}"
    )
    print("-" * 84)

    for pf in persona_files:
        with open(os.path.join(PERSONAS_DIR, pf), "r", encoding="utf-8") as f:
            content = f.read()

        sections = count_sections(content)
        interfaces = count_interfaces(content)
        compliance = count_compliance(content)
        score = sections + interfaces + compliance

        scores[pf] = {
            "sections": sections,
            "interfaces": interfaces,
            "compliance": compliance,
            "score": score,
            "label": score_label(score),
        }

        print(
            f"{pf:<30} {sections:>8} {interfaces:>10} {compliance:>10} {score:>6} {score_label(score):>10}"
        )

    with open(SIGNALS_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()
    new_lines = []

    for i, line in enumerate(lines):
        if i == 0:
            new_lines.append(line)
            continue

        parts = [p.strip() for p in line.split("|")]

        if len(parts) >= 4 and parts[3].startswith("`personas/"):
            persona_file = parts[3].replace("`personas/", "").replace("`", "").strip()
            if persona_file in scores:
                s = scores[persona_file]
                complexity_str = f"{s['score']} ({s['label']})"
                if len(parts) == 5 and parts[4] == "":
                    parts.insert(4, complexity_str)
                elif len(parts) >= 5:
                    parts[4] = complexity_str
                else:
                    parts.append(complexity_str)
                    parts.append("")
                new_lines.append("| " + " | ".join(parts[1:-1]) + " |")
                continue

        if "Signal Indicators" in line and "Domain" in line and "Persona File" in line:
            if "Completeness" not in line:
                line = line.rstrip("|").rstrip() + " Completeness |"
            new_lines.append(line)
            continue

        if re.match(r"^\|[-\s|]+\|$", line):
            if line.count("|") == 4:
                line = line.rstrip("|").rstrip() + "---|"
            new_lines.append(line)
            continue

        new_lines.append(line)

    with open(SIGNALS_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines) + "\n")

    print("\n✅ Completeness scores added to detection_signals.md")


if __name__ == "__main__":
    main()
