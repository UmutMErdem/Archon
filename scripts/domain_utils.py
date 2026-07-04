"""
Shared domain resolution utilities for Archon scripts.

Centralizes domain-to-persona-file mapping logic that was previously
duplicated across validate_manifesto.py, sync_matrix.py, and generate_diagram.py.
"""

import os
import re

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SIGNALS_PATH = os.path.join(REPO_ROOT, "detection_signals.md")

# Canonical overrides for domain name variations -> persona filename
DOMAIN_OVERRIDES = {
    "ar": "ar_vr_xr.md",
    "arvrxr": "ar_vr_xr.md",
    "ar/vr/xr": "ar_vr_xr.md",
    "qa": "qa_testing.md",
    "db": "db_architect.md",
    "pm": "product_management.md",
    "erp": "erp_enterprise.md",
    "embedded/iot": "embedded_iot.md",
    "web/mobileapps": "web_mobile_apps.md",
    "ai/ml": "ai_ml.md",
    "cybersecurity": "cybersecurity.md",
    "devops": "devops.md",
    "cloudinfrastructure": "cloud_architecture.md",
    "qa/testautomation": "qa_testing.md",
    "databasearchitect/dba": "db_architect.md",
    "databasearchitect": "db_architect.md",
    "productmanagement/businessanalysis": "product_management.md",
    "securitycompliance/devsecops": "security_compliance.md",
    "apidesign": "api_design.md",
    "ui/uxdesign": "ui_ux_design.md",
    "mobilenative": "mobile_native.md",
    "erp/enterprisesystems": "erp_enterprise.md",
    "technicalwriting&documentation": "technical_writing.md",
    "technicalwriting": "technical_writing.md",
    "cloudarchitecture": "cloud_architecture.md",
}


def load_domain_mappings(signals_path=None):
    """Load persona file -> domain name mappings from detection_signals.md."""
    if signals_path is None:
        signals_path = SIGNALS_PATH

    mappings = {}
    if not os.path.exists(signals_path):
        return mappings

    with open(signals_path, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()
    for line in lines:
        if "|" in line:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 4 and parts[3].startswith("`personas/"):
                persona_file = (
                    parts[3].replace("`personas/", "").replace("`", "").strip()
                )
                domain_name = parts[2].strip()
                mappings[persona_file] = domain_name
    return mappings


def resolve_domain_to_persona_file(domain_str, mappings):
    """Resolve a domain name string to its corresponding persona filename.

    Uses a multi-pass strategy:
    1. Exact match against canonical overrides
    2. Exact match against detection_signals.md mappings
    3. Base filename match
    4. Exact word/part match in domain
    5. Substring match with safety checks
    6. Fallback filename substring match
    """
    norm_str = re.sub(r"[\s/&:_-]", "", domain_str).lower()

    # Check overrides exact match first
    for key, val in DOMAIN_OVERRIDES.items():
        norm_key = re.sub(r"[\s/&:_-]", "", key).lower()
        if norm_str == norm_key:
            return val

    # Check mappings exact match next
    for fn, dom in mappings.items():
        norm_dom = re.sub(r"[\s/&:_-]", "", dom).lower()
        if norm_str == norm_dom:
            return fn

    # Check base filename exact match
    for fn in mappings.keys():
        base = fn.replace(".md", "").replace("_", "")
        if norm_str == base:
            return fn

    # Check exact word/part match in domain
    for fn, dom in mappings.items():
        parts = [re.sub(r"[\s/&:_-]", "", p).lower() for p in re.split(r"[/&|-]", dom)]
        if norm_str in parts:
            return fn

    # Substring mappings match with safety checks for short generic terms
    for fn, dom in mappings.items():
        norm_dom = re.sub(r"[\s/&:_-]", "", dom).lower()
        if norm_str in norm_dom:
            if norm_str == "automation" and fn != "automation.md":
                continue
            if norm_str == "qa" and fn != "qa_testing.md":
                continue
            if norm_str == "db" and fn != "db_architect.md":
                continue
            return fn

    # Fallback to filename parts substring match
    for fn in mappings.keys():
        base = fn.replace(".md", "").replace("_", "")
        if base in norm_str or norm_str in base:
            return fn

    return None
