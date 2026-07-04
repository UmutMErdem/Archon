import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except AttributeError:
    pass

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PERSONAS_DIR = os.path.join(REPO_ROOT, "personas")

INHERITS_MAP = {
    "api_design.md": {
        "base": "web_mobile_apps.md",
        "base_reason": "HTTP standards, authentication patterns, web security practices",
        "overrides": "API contract design, versioning policy, rate limiting rules",
    },
    "ui_ux_design.md": {
        "base": "web_mobile_apps.md",
        "base_reason": "frontend framework conventions, build tooling, testing patterns",
        "overrides": "component API design, visual regression standards, accessibility requirements",
    },
    "mobile_native.md": {
        "base": "web_mobile_apps.md",
        "base_reason": "general application architecture patterns, API integration conventions",
        "overrides": "platform-specific lifecycle, native UI toolkit patterns, app store guidelines",
    },
    "cloud_architecture.md": {
        "base": "devops.md",
        "base_reason": "CI/CD pipeline patterns, containerization standards, IaC conventions",
        "overrides": "cloud-native service selection, multi-region topology, cost optimization",
    },
    "security_compliance.md": {
        "base": "cybersecurity.md",
        "base_reason": "threat modeling methodology, vulnerability assessment patterns",
        "overrides": "compliance audit frameworks, governance policies, regulatory controls",
    },
    "qa_testing.md": {
        "base": "web_mobile_apps.md",
        "base_reason": "packaging, logging, linting standards from primary dev persona",
        "overrides": "test strategy, coverage targets, flakiness rules, CI test stages",
    },
    "data_engineering.md": {
        "base": "db_architect.md",
        "base_reason": "database fundamentals, query optimization, schema design",
        "overrides": "pipeline orchestration, warehouse modeling, streaming architecture",
    },
}


def add_inherits_to_frontmatter(filename, inherits_info):
    filepath = os.path.join(PERSONAS_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.strip().startswith("---"):
        print(f"  SKIP {filename}: no frontmatter found")
        return

    parts = content.split("---", 2)
    if len(parts) < 3:
        print(f"  SKIP {filename}: malformed frontmatter")
        return

    yaml_block = parts[1]

    if "inherits:" in yaml_block:
        print(f"  SKIP {filename}: already has inherits")
        return

    if inherits_info:
        inherits_yaml = f'\ninherits:\n  base: "{inherits_info["base"]}"\n  base_reason: "{inherits_info["base_reason"]}"\n  overrides: "{inherits_info["overrides"]}"'
    else:
        inherits_yaml = '\ninherits: "none"'

    new_yaml = yaml_block.rstrip() + inherits_yaml + "\n"
    new_content = "---" + new_yaml + "---" + parts[2]

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    if inherits_info:
        print(f"  OK {filename}: inherits {inherits_info['base']}")
    else:
        print(f"  OK {filename}: standalone (no inheritance)")


def main():
    print("Adding inherits to persona frontmatter...")
    persona_files = sorted([f for f in os.listdir(PERSONAS_DIR) if f.endswith(".md")])

    for pf in persona_files:
        inherits_info = INHERITS_MAP.get(pf, None)
        add_inherits_to_frontmatter(pf, inherits_info)

    print(f"\nDone. {len(persona_files)} personas processed.")


if __name__ == "__main__":
    main()
