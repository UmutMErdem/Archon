import os
import re
import sys
from domain_utils import load_domain_mappings, resolve_domain_to_persona_file

try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    pass

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PERSONAS_DIR = os.path.join(REPO_ROOT, "personas")
MATRIX_PATH = os.path.join(REPO_ROOT, "CROSS_DOMAIN_MATRIX.md")

SHORT_NAMES = {
    "embedded_iot.md": "Embedded",
    "hardware_design.md": "Hardware",
    "automation.md": "Automation",
    "web_mobile_apps.md": "Web/Mobile",
    "ai_ml.md": "AI/ML",
    "data_engineering.md": "DataEng",
    "devops.md": "DevOps",
    "robotics.md": "Robotics",
    "fpga_digital.md": "FPGA",
    "game_dev.md": "GameDev",
    "ar_vr_xr.md": "AR/VR/XR",
    "cybersecurity.md": "CyberSec",
    "signal_processing.md": "DSP",
    "systems_programming.md": "SysProg",
    "mechanical_cad.md": "MechCAD",
    "blockchain.md": "Blockchain",
    "network_telecom.md": "NetTelecom",
    "qa_testing.md": "QA",
    "db_architect.md": "Database",
    "product_management.md": "ProdMgmt",
    "security_compliance.md": "SecCompl",
    "cloud_architecture.md": "CloudArch",
    "api_design.md": "API",
    "ui_ux_design.md": "UI/UX",
    "mobile_native.md": "MobileNat",
    "erp_enterprise.md": "ERP",
    "technical_writing.md": "TechWrite",
}

TIER_COLORS = {
    "Comprehensive": "#FF6B6B",
    "Thorough": "#FFA94D",
    "Moderate": "#69DB7C",
    "Sparse": "#74C0FC",
}

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
    r"^## Cross-Domain Interfaces"
]

def count_sections(content):
    return sum(1 for p in REQUIRED_HEADINGS if re.search(p, content, re.MULTILINE))

def count_interfaces(content):
    match = re.search(r"## Cross-Domain Interfaces\s*(.*?)(?:\n## |\Z)", content, re.DOTALL)
    if not match:
        return 0
    return len(re.findall(r"^\s*-\s*\*\*→", match.group(1), re.MULTILINE))

def count_compliance(content):
    match = re.search(r"## Compliance & Standards\s*(.*?)(?:\n## |\Z)", content, re.DOTALL)
    if not match:
        return 0
    return len([l for l in match.group(1).splitlines() if l.strip().startswith("-")])

def score_label(score):
    if score <= 22:
        return "Sparse"
    elif score <= 26:
        return "Moderate"
    elif score <= 32:
        return "Thorough"
    return "Comprehensive"

def resolve_target(target_domain, file_map):
    """Resolve target domain using shared domain_utils."""
    return resolve_domain_to_persona_file(target_domain, file_map)

def parse_frontmatter_domain(content):
    if not content.strip().startswith("---"):
        return None
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None
    for line in parts[1].splitlines():
        line = line.strip()
        if line.startswith("domain:"):
            val = line.split(":", 1)[1].strip().strip('"').strip("'")
            return val
    return None

def main():
    print("Generating Mermaid diagram from persona interfaces...\n")

    file_map = {}
    edges = set()
    scores = {}

    persona_files = sorted([f for f in os.listdir(PERSONAS_DIR) if f.endswith(".md")])

    for pf in persona_files:
        with open(os.path.join(PERSONAS_DIR, pf), "r", encoding="utf-8") as f:
            content = f.read()

        domain = parse_frontmatter_domain(content) or pf.replace(".md", "").replace("_", " ").title()
        file_map[pf] = domain

        s = count_sections(content) + count_interfaces(content) + count_compliance(content)
        scores[pf] = score_label(s)

    for pf in persona_files:
        with open(os.path.join(PERSONAS_DIR, pf), "r", encoding="utf-8") as f:
            content = f.read()

        match = re.search(r"## Cross-Domain Interfaces\s*(.*?)(?:\n## |\Z)", content, re.DOTALL)
        if not match:
            continue

        for line in match.group(1).splitlines():
            m = re.match(r"-\s*\*\*→\s*([^*:]+)(?:\*\*:\s*|:\*\*\s*)", line.strip())
            if m:
                target = m.group(1).strip()
                target_file = resolve_target(target, file_map)
                if target_file:
                    edges.add((pf, target_file))

    node_id = lambda f: f.replace(".md", "").replace("_", "")
    short = lambda f: SHORT_NAMES.get(f, f.replace(".md", ""))

    lines = ["```mermaid", "graph LR"]

    for pf in persona_files:
        nid = node_id(pf)
        label = short(pf)
        tier = scores.get(pf, "Light")
        lines.append(f"    {nid}[\"{label}\"]")

    lines.append("")

    for tier_name, color in TIER_COLORS.items():
        tier_nodes = [node_id(pf) for pf in persona_files if scores.get(pf) == tier_name]
        if tier_nodes:
            lines.append(f"    style {','.join(tier_nodes)} fill:{color},stroke:#333,stroke-width:1px")

    lines.append("")

    for src, dst in sorted(edges):
        lines.append(f"    {node_id(src)} --> {node_id(dst)}")

    lines.append("```")

    mermaid_block = "\n".join(lines)

    with open(MATRIX_PATH, "r", encoding="utf-8") as f:
        matrix_content = f.read()

    if "```mermaid" in matrix_content:
        matrix_content = re.sub(r"## Relationship Diagram.*?```\s*", "", matrix_content, flags=re.DOTALL)

    legend = """
## Relationship Diagram

> Auto-generated by `scripts/generate_diagram.py`. Color indicates completeness tier:
> - 🔴 Comprehensive (33+) — 🟠 Thorough (27-32) — 🟢 Moderate (23-26) — 🔵 Sparse (≤22)

"""

    insert_pos = matrix_content.find("\n---\n\n## Missing")
    if insert_pos == -1:
        matrix_content = matrix_content.rstrip() + "\n\n" + legend + mermaid_block + "\n"
    else:
        matrix_content = matrix_content[:insert_pos] + "\n\n" + legend + mermaid_block + "\n" + matrix_content[insert_pos:]

    with open(MATRIX_PATH, "w", encoding="utf-8") as f:
        f.write(matrix_content)

    print(f"✅ Mermaid diagram with {len(edges)} edges inserted into CROSS_DOMAIN_MATRIX.md")
    print(f"   Tier distribution: " + ", ".join(
        f"{t}: {sum(1 for p in persona_files if scores.get(p)==t)}"
        for t in ["Sparse", "Moderate", "Thorough", "Comprehensive"]
    ))

if __name__ == "__main__":
    main()
