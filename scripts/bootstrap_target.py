import os
import re
import sys
import datetime
import shutil
import subprocess

# Set system output to UTF-8
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except AttributeError:
    pass

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PERSONAS_DIR = os.path.join(REPO_ROOT, "personas")


def prompt(text):
    sys.stdout.write(text)
    sys.stdout.flush()
    return sys.stdin.readline().strip()


def parse_frontmatter(content):
    if not content.strip().startswith("---"):
        return None
    parts = content.split("---")
    if len(parts) < 3:
        return None

    yaml_text = parts[1]
    metadata = {}
    for line in yaml_text.splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            items = []
            val_clean = value[1:-1].strip()
            quoted_items = re.findall(r'"([^"]*)"|\'([^\']*)\'', val_clean)
            for q in quoted_items:
                items.append(q[0] or q[1])
            metadata[key] = items
        else:
            if value.startswith(('"', "'")) and value.endswith(('"', "'")):
                value = value[1:-1]
            metadata[key] = value
    return metadata


def select_personas():
    files = sorted([f for f in os.listdir(PERSONAS_DIR) if f.endswith(".md")])
    print("\nAvailable Personas:")
    for idx, f in enumerate(files):
        print(f"  [{idx + 1}] {f}")

    choices = prompt("\nEnter persona numbers to load (comma-separated, e.g. 7,10): ")
    selected = []
    for c in choices.split(","):
        try:
            val = int(c.strip()) - 1
            if 0 <= val < len(files):
                selected.append(files[val])
        except ValueError:
            pass
    return selected


def main():
    print("==================================================")
    print("🚀  Archon Target Project Scaffolder  🚀")
    print("==================================================")

    target_dir = prompt("Enter target project workspace path: ")
    if not target_dir:
        print("Target path cannot be empty.")
        return

    target_dir = os.path.abspath(target_dir)
    if not os.path.exists(target_dir):
        create = prompt(f"Directory {target_dir} does not exist. Create it? (y/n): ")
        if create.lower() == "y":
            os.makedirs(target_dir, exist_ok=True)
        else:
            return

    selected_personas = select_personas()
    if not selected_personas:
        print("No personas selected. Scaffolding cancelled.")
        return

    setup_graphify = prompt("\nDo you want to initialize and configure Graphify for the target project? (y/n): ").strip().lower() == "y"

    personas_meta = []
    for pf in selected_personas:
        pf_path = os.path.join(PERSONAS_DIR, pf)
        with open(pf_path, "r", encoding="utf-8") as f:
            content = f.read()
        meta = parse_frontmatter(content)
        if meta:
            meta["file"] = pf
            personas_meta.append(meta)

    if not personas_meta:
        print("Failed to read metadata for selected personas.")
        return

    primary = personas_meta[0]
    supporting = personas_meta[1:]

    date_str = datetime.date.today().strftime("%Y-%m-%d")

    # 1. Write AGENTS.md
    agents_content = f"""# AGENTS.md - Persona Configuration

This file defines the expert roles, behaviors, and verification checklists active in this workspace.

## Active Personas

### Primary Lead Architect
- **Domain:** {primary.get("domain")}
- **Role:** {primary.get("expert_role")}
- **Persona Reference:** [personas/{primary.get("file")}](file:///{os.path.join(PERSONAS_DIR, primary.get("file")).replace(os.sep, '/')})

"""
    if supporting:
        agents_content += "### Supporting Specialists\n"
        for idx, sup in enumerate(supporting):
            agents_content += f"""- **Domain {idx + 1}:** {sup.get("domain")}
- **Role:** {sup.get("expert_role")}
- **Persona Reference:** [personas/{sup.get("file")}](file:///{os.path.join(PERSONAS_DIR, sup.get("file")).replace(os.sep, '/')})

"""
    agents_content += """## Coding Conventions & Quality Gates
1. **Zero Dead Links:** All file and symbol references must be clickable links that exist on disk.
2. **Explicit Verification:** Every modification must pass linter and test validation steps before completion.
"""
    with open(os.path.join(target_dir, "AGENTS.md"), "w", encoding="utf-8") as f:
        f.write(agents_content)

    # 2. Write PROJECT_STATE.md
    state_content = f"""# PROJECT_STATE.md

## Snapshot Details
- **Analysis Date:** {date_str}
- **Git Branch:** N/A (initialized)
- **Commit Hash:** N/A

## Version Table
| Component | Platform / Version | Status |
|---|---|---|
| Core | Initialized | Under Construction |

## Open Issues Summary
- Links to [KNOWN_ISSUES.md](KNOWN_ISSUES.md)
- Links to [OPTIMIZATIONS.md](OPTIMIZATIONS.md)
- Links to [ROADMAP.md](ROADMAP.md)
- Link to [CHANGELOG.md](CHANGELOG.md)
"""
    with open(os.path.join(target_dir, "PROJECT_STATE.md"), "w", encoding="utf-8") as f:
        f.write(state_content)

    onboarding_content = "# ONBOARDING.md\n\n## Environment Setup\nInstructions for setting up the local development workspace.\n"
    architecture_content = f"""# ARCHITECTURE.md - System Architecture

## 1. Main Idea & Project Recap
Project initialized using Archon Manifesto with the `{primary.get("domain")}` persona.

## 2. System Mapping
- Domain Specific Map: [Document pin layout, API endpoints, schema relations here]

## 3. Build, Deploy & Run
- Build commands:
- Deploy commands:
- Run/execute:
"""

    if setup_graphify:
        onboarding_content += """
## Graphify Knowledge Graph
This project integrates **Graphify** for codebase knowledge representation.
To build, update, or query the graph, use the helper script:
- **Build/Rebuild Graph:** `python scripts/graphify_helper.py --build`
- **Incremental Update:** `python scripts/graphify_helper.py --update`
- **Query Graph:** `python scripts/graphify_helper.py --query "your question"`
- **Visualizations:** After building, open `graphify-out/graph.html` in your browser, or import the `graphify-out/obsidian/` folder into Obsidian.
"""
        architecture_content = f"""# ARCHITECTURE.md - System Architecture

## 1. Main Idea & Project Recap
Project initialized using Archon Manifesto with the `{primary.get("domain")}` persona.

## 2. System Mapping
- Domain Specific Map: [Document pin layout, API endpoints, schema relations here]
- **Interactive Codebase Graph:** Refer to [graphify-out/graph.svg](file:///{os.path.join(target_dir, 'graphify-out', 'graph.svg').replace(os.sep, '/')}) for the auto-generated visual relationship diagram of modules.

## 3. Build, Deploy & Run
- Build commands:
- Deploy commands:
- Run/execute:
"""

    # 3. Write other files boilerplate
    boilerplates = {
        "DECISIONS.md": "# DECISIONS.md\n\n| Decision ID | Date | Decision | Rationale | Impact |\n|---|---|---|---|---|\n",
        "KNOWN_ISSUES.md": "# KNOWN_ISSUES.md\n\n| Issue ID | Severity | Status | Symptom | Root Cause | Fix |\n|---|---|---|---|---|---|\n",
        "OPTIMIZATIONS.md": "# OPTIMIZATIONS.md\n\n| Opt ID | Category | Severity | Status | Recommendation |\n|---|---|---|---|---|\n",
        "ROADMAP.md": "# ROADMAP.md\n\n| Milestone | Priority | Status | Goal | Task List |\n|---|---|---|---|---|\n",
        "TESTING.md": "# TESTING.md\n\n## Test Strategy\nConfigure your testing commands and frameworks here.\n",
        "SECURITY.md": "# SECURITY.md\n\n## Threat Modeling\nEndpoints, trust boundaries, and encryption models.\n",
        "DEPENDENCIES.md": "# DEPENDENCIES.md\n\n## Third-Party Libraries\n| Dependency | Version | License | Status |\n|---|---|---|---|\n",
        "ONBOARDING.md": onboarding_content,
        "CHANGELOG.md": "# CHANGELOG.md\n\n## [Unreleased]\n- Initialized target project using Archon Scaffolder.\n",
        "ARCHITECTURE.md": architecture_content,
    }

    for filename, content in boilerplates.items():
        with open(os.path.join(target_dir, filename), "w", encoding="utf-8") as f:
            f.write(content)

    print("\n✅ Scaffolding complete! Generated 12 compliance files in:")
    print(f"   {target_dir}")

    if setup_graphify:
        print("\n🔧 Setting up Graphify for the target project...")
        # Create scripts directory if not exists
        scripts_dir = os.path.join(target_dir, "scripts")
        os.makedirs(scripts_dir, exist_ok=True)
        
        # Copy helper script
        helper_src = os.path.join(REPO_ROOT, "scripts", "graphify_helper.py")
        helper_dst = os.path.join(scripts_dir, "graphify_helper.py")
        try:
            shutil.copy2(helper_src, helper_dst)
            print(f"   Copied graphify_helper.py to {helper_dst}")
        except Exception as e:
            print(f"   Failed to copy graphify_helper.py: {e}")
            
        # Run graphify_helper.py to build the initial graph
        print("   Running Graphify initial build...")
        try:
            subprocess.run([sys.executable, helper_dst, "--path", target_dir, "--build"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"   Graphify initial build failed or was interrupted: {e}")
            
        # Update/Create .gitignore in target directory
        gitignore_path = os.path.join(target_dir, ".gitignore")
        ignore_line = "\n# Graphify Outputs\ngraphify-out/\n"
        try:
            if os.path.exists(gitignore_path):
                with open(gitignore_path, "r", encoding="utf-8") as f:
                    git_content = f.read()
                if "graphify-out/" not in git_content:
                    with open(gitignore_path, "a", encoding="utf-8") as f:
                        f.write(ignore_line)
                    print("   Updated target's .gitignore")
            else:
                with open(gitignore_path, "w", encoding="utf-8") as f:
                    f.write(ignore_line)
                print("   Created target's .gitignore")
        except Exception as e:
            print(f"   Failed to update .gitignore: {e}")

        # Create default .graphifyignore in target directory
        graphifyignore_path = os.path.join(target_dir, ".graphifyignore")
        graphifyignore_content = """# Default Graphify Ignore File
graphify-out/
.git/
__pycache__/
.pytest_cache/
.ruff_cache/
node_modules/
dist/
build/
.venv/
venv/
"""
        try:
            with open(graphifyignore_path, "w", encoding="utf-8") as f:
                f.write(graphifyignore_content)
            print("   Created target's .graphifyignore")
        except Exception as e:
            print(f"   Failed to create .graphifyignore: {e}")



if __name__ == "__main__":
    main()

