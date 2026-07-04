import os
import re

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PERSONAS_DIR = os.path.join(REPO_ROOT, "personas")

missing_links = [
    # (Target File, Link Header, Description)
    ("security_compliance.md", "Hardware Design", "Securing physical PCB designs, firmware validation audits"),
    ("cloud_architecture.md", "Data Engineering", "Cloud data warehousing resources scaling, data lake security policies"),
    ("erp_enterprise.md", "Data Engineering", "Sync schedules to OLAP data warehouses, ETL processes orchestration"),
    ("erp_enterprise.md", "DevOps", "Corporate middleware deployments, ERP build runners infrastructure"),
    ("api_design.md", "Security Compliance", "API security control guidelines, API access auditing and logs"),
    ("erp_enterprise.md", "Security Compliance", "SOX compliance auditing configuration, corporate audit trails validation"),
    ("web_mobile_apps.md", "Cloud Architecture", "API Gateway DNS integration, CDN caching configurations"),
    ("qa_testing.md", "API Design", "API contract testing integration (Pact), endpoint schema validation"),
    ("api_design.md", "Mobile Native", "Mobile client SDK generation, push notification payload schemas"),
    ("ui_ux_design.md", "Mobile Native", "Designing mobile safe area layouts, notch padding specifications"),
    ("db_architect.md", "Mobile Native", "Local SQLite/Room schema designs, offline synchronization schemas"),
    ("cybersecurity.md", "ERP & Enterprise Systems", "Corporate ERP access privilege controls, financial auditing security"),
    ("web_mobile_apps.md", "ERP & Enterprise Systems", "Corporate sales portals integration, client dashboard reporting pipelines"),
    ("product_management.md", "ERP & Enterprise Systems", "Corporate business rule mappings, release milestone planning"),
    ("web_mobile_apps.md", "Technical Writing", "Developer onboarding manuals integration, API docs portal mapping"),
    ("api_design.md", "Technical Writing", "OpenAPI spec formatting rules, documentation generator integration")
]

def add_link(filename, target_domain, desc):
    file_path = os.path.join(PERSONAS_DIR, filename)
    if not os.path.exists(file_path):
        print(f"Error: {file_path} does not exist.")
        return
        
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    match = re.search(r"## Cross-Domain Interfaces\s*(.*?)\s*(?:##|$)", content, re.DOTALL)
    if not match:
        print(f"Error: Cross-Domain Interfaces not found in {filename}")
        return
        
    section_text = match.group(1)
    
    if f"→ {target_domain}" in section_text or f"\u2192 {target_domain}" in section_text:
        print(f"Link to '{target_domain}' already exists in {filename}")
        return
        
    new_link_line = f"- **\u2192 {target_domain}:** {desc}"
    new_section_text = section_text.rstrip() + "\n" + new_link_line + "\n"
    new_content = content.replace(section_text, new_section_text)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Added link to '{target_domain}' in {filename}")

def main():
    for fn, domain, desc in missing_links:
        add_link(fn, domain, desc)

if __name__ == "__main__":
    main()
