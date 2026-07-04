import os
import re
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PERSONAS_DIR = os.path.join(REPO_ROOT, "personas")
SIGNALS_PATH = os.path.join(REPO_ROOT, "detection_signals.md")

# Set system output to UTF-8 to handle Unicode on Windows
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    pass

def load_domain_mappings():
    mappings = {}
    if not os.path.exists(SIGNALS_PATH):
        print(f"Warning: {SIGNALS_PATH} not found. Fallback names will be used.")
        return mappings
        
    with open(SIGNALS_PATH, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Parse markdown table lines
    lines = content.splitlines()
    for line in lines:
        if "|" in line:
            parts = [p.strip() for p in line.split("|")]
            # Format: | Signal | Domain | Persona File |
            # parts has elements: ['', Signal, Domain, Persona File, '']
            if len(parts) >= 4 and parts[3].startswith("`personas/"):
                persona_file = parts[3].replace("`personas/", "").replace("`", "").strip()
                domain_name = parts[2].strip()
                mappings[persona_file] = domain_name
    return mappings

def extract_meta(content):
    expert_role = ""
    tools = []
    compliance = []
    
    # Extract Expert Role
    role_match = re.search(r"## Expert Role\s*>\s*(.*?)\s*(?:##|$)", content, re.DOTALL)
    if role_match:
        expert_role = role_match.group(1).strip().replace("\n", " ").replace("  ", " ")
        # Strip bold markers
        expert_role = re.sub(r"\*\*([^*]+)\*\*", r"\1", expert_role)
        
    # Extract Recommended Toolchain
    tools_match = re.search(r"## Recommended Toolchain\s*(.*?)\s*(?:##|$)", content, re.DOTALL)
    if tools_match:
        tool_lines = tools_match.group(1).splitlines()
        for tl in tool_lines:
            tl = tl.strip()
            if tl.startswith("-"):
                # Clean tool text: extract bold title and details, or just the whole line
                t_clean = re.sub(r"^-\s*", "", tl).strip()
                t_clean = re.sub(r"\*\*([^*]+)\*\*:", r"\1:", t_clean)
                tools.append(t_clean)
                
    # Extract Compliance & Standards
    comp_match = re.search(r"## Compliance & Standards\s*(.*?)\s*(?:##|$)", content, re.DOTALL)
    if comp_match:
        comp_lines = comp_match.group(1).splitlines()
        for cl in comp_lines:
            cl = cl.strip()
            if cl.startswith("-"):
                c_clean = re.sub(r"^-\s*", "", cl).strip()
                compliance.append(c_clean)
                
    return expert_role, tools, compliance

def migrate_file(file_name, domain_mappings):
    file_path = os.path.join(PERSONAS_DIR, file_name)
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Check if already has frontmatter
    if content.strip().startswith("---"):
        print(f"  - {file_name} already contains frontmatter. Skipping.")
        return
        
    domain = domain_mappings.get(file_name, file_name.replace(".md", "").replace("_", " ").title())
    expert_role, tools, compliance = extract_meta(content)
    
    # Clean lists for YAML output
    tools_yaml = ", ".join([f'"{t}"' for t in tools])
    comp_yaml = ", ".join([f'"{c}"' for c in compliance])
    
    # Construct frontmatter block
    frontmatter = f"""---
domain: "{domain}"
expert_role: "{expert_role}"
recommended_tools: [{tools_yaml}]
compliance: [{comp_yaml}]
---

"""
    new_content = frontmatter + content
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"  - Migrated {file_name} successfully.")

def main():
    print("==================================================")
    print("📦  Archon Frontmatter Migration Script  📦")
    print("==================================================")
    
    if not os.path.exists(PERSONAS_DIR):
        print(f"Error: {PERSONAS_DIR} does not exist.")
        sys.exit(1)
        
    domain_mappings = load_domain_mappings()
    persona_files = [f for f in os.listdir(PERSONAS_DIR) if f.endswith(".md")]
    
    print(f"Found {len(persona_files)} persona files to migrate...")
    for pf in sorted(persona_files):
        migrate_file(pf, domain_mappings)
        
    print("\n✅ Migration completed successfully!")

if __name__ == "__main__":
    main()
