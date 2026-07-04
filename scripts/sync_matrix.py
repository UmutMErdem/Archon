import os
import re
import sys
from domain_utils import load_domain_mappings, resolve_domain_to_persona_file

# Set system output to UTF-8
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except AttributeError:
    pass

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PERSONAS_DIR = os.path.join(REPO_ROOT, "personas")
SIGNALS_PATH = os.path.join(REPO_ROOT, "detection_signals.md")
MATRIX_PATH = os.path.join(REPO_ROOT, "CROSS_DOMAIN_MATRIX.md")

# Canonical short display names for matrix table presentation
SHORT_NAMES = {
    "embedded_iot.md": "Embedded/IoT",
    "hardware_design.md": "Hardware Design",
    "automation.md": "Automation",
    "web_mobile_apps.md": "Web/Mobile Apps",
    "ai_ml.md": "AI/ML",
    "data_engineering.md": "Data Engineering",
    "devops.md": "DevOps",
    "robotics.md": "Robotics",
    "fpga_digital.md": "FPGA",
    "game_dev.md": "Game Dev",
    "ar_vr_xr.md": "AR/VR/XR",
    "cybersecurity.md": "Cybersecurity",
    "signal_processing.md": "Signal Processing",
    "systems_programming.md": "Systems Programming",
    "mechanical_cad.md": "Mechanical CAD",
    "blockchain.md": "Blockchain",
    "network_telecom.md": "Network/Telecom",
    "qa_testing.md": "QA/Testing",
    "db_architect.md": "Database Architect",
    "product_management.md": "Product Management",
    "security_compliance.md": "Security Compliance",
    "cloud_architecture.md": "Cloud Architecture",
    "api_design.md": "API Design",
    "ui_ux_design.md": "UI/UX Design",
    "mobile_native.md": "Mobile Native",
    "erp_enterprise.md": "ERP/Enterprise",
    "technical_writing.md": "Technical Writing",
}


def get_short_name(persona_file, mappings):
    """Get display name from SHORT_NAMES, falling back to domain mapping."""
    if persona_file in SHORT_NAMES:
        return SHORT_NAMES[persona_file]
    return mappings.get(
        persona_file, persona_file.replace(".md", "").replace("_", " ").title()
    )


def main():
    mappings = load_domain_mappings()

    # Extract interfaces from persona files
    interfaces = []
    persona_files = sorted([f for f in os.listdir(PERSONAS_DIR) if f.endswith(".md")])

    for pf in persona_files:
        pf_path = os.path.join(PERSONAS_DIR, pf)
        with open(pf_path, "r", encoding="utf-8") as f:
            content = f.read()

        match = re.search(
            r"## Cross-Domain Interfaces\s*(.*?)(?:\n## |\Z)", content, re.DOTALL
        )
        if not match:
            continue

        mappings.get(pf, pf.replace(".md", "").replace("_", " ").title())
        source_presentation = get_short_name(pf, mappings)

        lines = match.group(1).splitlines()
        for line in lines:
            m = re.match(
                r"-\s*\*\*\u2192\s*([^*:]+)(?:\*\*:\s*|:\*\*\s*)(.*)", line.strip()
            )
            if m:
                target_domain = m.group(1).strip()
                desc = m.group(2).strip()

                target_file = resolve_domain_to_persona_file(target_domain, mappings)
                target_presentation = (
                    get_short_name(target_file, mappings)
                    if target_file
                    else target_domain
                )

                interfaces.append(
                    (source_presentation, target_presentation, desc, pf, target_domain)
                )

    # Sort interfaces alphabetically
    interfaces.sort(key=lambda x: (x[0], x[1]))

    # 1. Generate Table Content
    table_lines = [
        "| From Persona | To Persona | Interface Contract |",
        "|---|---|---|",
    ]
    for from_p, to_p, desc, _, _ in interfaces:
        table_lines.append(f"| {from_p} | {to_p} | {desc} |")

    table_content = "\n".join(table_lines)

    # 2. Generate Mermaid Flowchart
    mermaid_lines = ["```mermaid", "flowchart TD"]
    nodes = set()
    connections = []
    for from_p, to_p, _, from_file, to_dom in interfaces:
        from_id = from_file.replace(".md", "").replace("_", "").lower()

        to_file = resolve_domain_to_persona_file(to_dom, mappings)
        if to_file:
            to_id = to_file.replace(".md", "").replace("_", "").lower()
            nodes.add(f'    {from_id}["{from_p}"]')
            nodes.add(f'    {to_id}["{to_p}"]')
            connections.append(f"    {from_id} --> {to_id}")

    mermaid_lines.extend(sorted(list(nodes)))
    mermaid_lines.extend(sorted(connections))
    mermaid_lines.append("```")
    mermaid_content = "\n".join(mermaid_lines)

    # 3. Preserve existing Relationship Diagram section if present
    relationship_diagram = ""
    if os.path.exists(MATRIX_PATH):
        with open(MATRIX_PATH, "r", encoding="utf-8") as f:
            existing_content = f.read()
        diag_match = re.search(
            r"(## Relationship Diagram.*?)(?=\n---\n|\Z)", existing_content, re.DOTALL
        )
        if diag_match:
            relationship_diagram = diag_match.group(1).rstrip() + "\n"

    # 4. Write MATRIX
    new_matrix_text = "# Cross-Domain Interface Matrix\n\n"
    new_matrix_text += (
        "> Single source of truth for all persona-to-persona interface contracts.\n"
    )
    new_matrix_text += "> Each row = a directional interface. Both directions should exist for bidirectional relationships.\n"
    new_matrix_text += "> Updated whenever a persona's `## Cross-Domain Interfaces` section changes.\n\n"
    new_matrix_text += "---\n\n"
    new_matrix_text += "## Interface Table\n\n"
    new_matrix_text += table_content + "\n\n"
    new_matrix_text += "---\n\n"
    new_matrix_text += "## Interface Graph\n\n"
    new_matrix_text += mermaid_content + "\n\n"
    if relationship_diagram:
        new_matrix_text += "---\n\n"
        new_matrix_text += relationship_diagram + "\n\n"
    new_matrix_text += "---\n\n"
    new_matrix_text += "## Missing Bidirectional Interfaces\n\n"
    new_matrix_text += (
        "Run `python scripts/validate_manifesto.py` to verify bidirectional symmetry.\n"
    )

    with open(MATRIX_PATH, "w", encoding="utf-8") as f:
        f.write(new_matrix_text)

    print("✅ CROSS_DOMAIN_MATRIX.md has been successfully synchronized!")


if __name__ == "__main__":
    main()
