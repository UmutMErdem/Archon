import os
import re
import sys
import shutil

# Set system output to UTF-8
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    pass

# Paths
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PERSONAS_DIR = os.path.join(REPO_ROOT, "personas")
TEMPLATE_PATH = os.path.join(REPO_ROOT, "PERSONA_TEMPLATE.md")
SIGNALS_PATH = os.path.join(REPO_ROOT, "detection_signals.md")
README_PATH = os.path.join(REPO_ROOT, "README.md")
DETECTION_PATH = os.path.join(REPO_ROOT, "architecture/00_detection.md")

def prompt(text):
    sys.stdout.write(text)
    sys.stdout.flush()
    return sys.stdin.readline().strip()

def main():
    print("==================================================")
    print("✨  Archon Persona Generator CLI  ✨")
    print("==================================================")
    
    domain = prompt("Enter Domain Name (e.g., Cloud Architecture): ")
    if not domain:
        print("Domain Name cannot be empty.")
        return
        
    filename = prompt("Enter Persona filename (e.g., cloud_architecture.md): ")
    if not filename:
        print("Filename cannot be empty.")
        return
    if not filename.endswith(".md"):
        filename += ".md"
        
    expert_role = prompt("Enter Expert Role Title (e.g., Senior Cloud Solutions Architect): ")
    tools_str = prompt("Enter recommended tools (comma-separated): ")
    compliance_str = prompt("Enter compliance standards (comma-separated): ")
    
    tools = [t.strip() for t in tools_str.split(",") if t.strip()]
    compliance = [c.strip() for c in compliance_str.split(",") if c.strip()]
    
    target_path = os.path.join(PERSONAS_DIR, filename)
    if os.path.exists(target_path):
        overwrite = prompt("File already exists. Overwrite? (y/n): ")
        if overwrite.lower() != 'y':
            return
            
    # Read template
    if not os.path.exists(TEMPLATE_PATH):
        print(f"Error: {TEMPLATE_PATH} not found.")
        return
        
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = f.read()
        
    # Replace placeholders
    filled = template.replace("<Domain Name>", domain)
    filled = filled.replace("<Senior Title>", expert_role)
    filled = filled.replace("<core skills, technologies, protocols, and sub-disciplines that define this domain>", expert_role)
    
    # Format lists for YAML frontmatter
    tools_yaml = ", ".join([f'"{t}"' for t in tools])
    comp_yaml = ", ".join([f'"{c}"' for c in compliance])
    
    frontmatter = f"""---
domain: "{domain}"
expert_role: "You are a {expert_role}."
recommended_tools: [{tools_yaml}]
compliance: [{comp_yaml}]
inherits: "none"
---

"""
    new_content = frontmatter + filled
    
    # Write new persona file
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"✅ Created persona file at personas/{filename}")
    
    # Register in detection_signals.md
    if os.path.exists(SIGNALS_PATH):
        with open(SIGNALS_PATH, "a", encoding="utf-8") as f:
            f.write(f"| `*.{filename.split('.')[0]}_config`, config files | {domain} | `personas/{filename}` | — |\n")
        print("✅ Registered in detection_signals.md")
        
    # Register in README.md
    if os.path.exists(README_PATH):
        with open(README_PATH, "r", encoding="utf-8") as f:
            readme = f.read()
        # Find personas count and update
        count_match = re.search(r"Domain Expert Personas \((\d+) personas\)", readme)
        if count_match:
            current_count = int(count_match.group(1))
            readme = readme.replace(f"Domain Expert Personas ({current_count} personas)", f"Domain Expert Personas ({current_count + 1} personas)")
        # Append to the end of the lists
        if f"({filename})" not in readme:
            new_readme = readme.replace("erp_enterprise.md](personas/erp_enterprise.md), [technical_writing.md](personas/technical_writing.md)", f"erp_enterprise.md](personas/erp_enterprise.md), [technical_writing.md](personas/technical_writing.md), [{filename}](personas/{filename})")
            if new_readme != readme:
                with open(README_PATH, "w", encoding="utf-8") as f:
                    f.write(new_readme)
                print("✅ Registered in README.md")
            else:
                print("⚠️  Could NOT register in README.md — anchor text not found, please add manually")
        else:
            print("ℹ️  Already registered in README.md")
        
    # Register in architecture/00_detection.md
    if os.path.exists(DETECTION_PATH):
        with open(DETECTION_PATH, "r", encoding="utf-8") as f:
            det = f.read()
        new_det = det.replace("Technical Writing)", f"Technical Writing, {domain})")
        if new_det == det:
            # Try a more general pattern: insert before the last closing parenthesis in the domain list
            new_det = re.sub(r"(\([^()]*)\)(\s*$)", rf"\1, {domain})", det, count=1, flags=re.MULTILINE)
        if new_det != det:
            with open(DETECTION_PATH, "w", encoding="utf-8") as f:
                f.write(new_det)
            print("✅ Registered in architecture/00_detection.md")
        else:
            print("⚠️  Could NOT register in architecture/00_detection.md — anchor text not found, please add manually")
        
    print("\nRunning complexity calculator and linter to verify compliance...")
    import subprocess
    subprocess.run(["python", "scripts/calculate_complexity.py"], cwd=REPO_ROOT)
    subprocess.run(["python", "scripts/validate_manifesto.py"], cwd=REPO_ROOT)

if __name__ == "__main__":
    main()
