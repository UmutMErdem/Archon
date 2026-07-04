import os
import re
import sys
import urllib.parse
from domain_utils import load_domain_mappings as _load_mappings, resolve_domain_to_persona_file

# Set system output to UTF-8 to handle Unicode on Windows
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    pass

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PERSONAS_DIR = os.path.join(REPO_ROOT, "personas")
SIGNALS_PATH = os.path.join(REPO_ROOT, "detection_signals.md")
COMPLIANCE_PATH = os.path.join(REPO_ROOT, "compliance.md")
MATRIX_PATH = os.path.join(REPO_ROOT, "CROSS_DOMAIN_MATRIX.md")

MIN_PERSONA_LINES = 30
MAX_PERSONA_LINES = 200

REQUIRED_HEADINGS = [
    r"^## Expert Role",
    r"^## Domain-Specific Discovery Questions",
    r"^## Key Focus Areas for ARCHITECTURE\.md",
    r"^### System Mapping → ",
    r"^### Detailed Specifications",
    r"^### Performance Budget",
    r"^### Domain-Specific Sections",
    r"^## Compliance & Standards",
    r"^## Common Pitfalls",
    r"^## Recommended Toolchain",
    r"^## Domain-Specific Testing",
    r"^## Cross-Domain Interfaces"
]

def load_domain_mappings():
    mappings = _load_mappings(SIGNALS_PATH)
    if not mappings:
        print(f"❌ Error: {SIGNALS_PATH} not found or empty.")
        sys.exit(1)
    return mappings

def parse_frontmatter(content):
    if not content.strip().startswith("---"):
        return None, "Missing frontmatter start marker '---'"
    
    parts = content.split("---")
    if len(parts) < 3:
        return None, "Missing frontmatter end marker '---'"
        
    yaml_text = parts[1]
    metadata = {}
    
    for line in yaml_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
            
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        
        # Parse arrays: [item1, item2, ...]
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
            
    return metadata, None

def check_template_integrity(persona_path):
    with open(persona_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    errors = []
    
    # 1. Verify and parse frontmatter
    meta, fm_err = parse_frontmatter(content)
    if fm_err:
        errors.append(f"Frontmatter error: {fm_err}")
    else:
        required_keys = ["domain", "expert_role", "recommended_tools", "compliance"]
        for rk in required_keys:
            if rk not in meta:
                errors.append(f"Frontmatter missing required key: '{rk}'")
            elif not meta[rk]:
                errors.append(f"Frontmatter key '{rk}' is empty")
                
    # 2. Check headings
    lines = content.splitlines()
    for heading_pattern in REQUIRED_HEADINGS:
        found = False
        for line in lines:
            if re.match(heading_pattern, line):
                found = True
                break
        if not found:
            clean_heading = heading_pattern.replace("^", "").replace("\\", "")
            errors.append(f"Missing required heading: '{clean_heading}'")
            
    return errors


def check_bidirectional_interfaces(mappings):
    errors = []
    links = {}
    raw_targets = {}  # Track all targets per persona for duplicate detection
    
    # First pass: parse all interfaces declared in each persona
    for pf in mappings.keys():
        links[pf] = set()
        raw_targets[pf] = []
        pf_path = os.path.join(PERSONAS_DIR, pf)
        if not os.path.exists(pf_path):
            continue
            
        with open(pf_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        match = re.search(r"## Cross-Domain Interfaces\s*(.*?)\s*(?:##|$)", content, re.DOTALL)
        if match:
            lines = match.group(1).splitlines()
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                # Parse: - **→ Target Domain:** description
                m = re.match(r"-\s*\*\*\u2192\s*([^*:]+)(?:\*\*:\s*|:\*\*\s*)", line)
                if m:
                    target_domain = m.group(1).strip()
                    target_file = resolve_domain_to_persona_file(target_domain, mappings)
                    if target_file:
                        links[pf].add(target_file)
                        raw_targets[pf].append(target_file)
                    else:
                        errors.append(f"{pf}: Could not resolve interface target domain '{target_domain}' to any persona file.")

    # Duplicate interface check
    from collections import Counter
    for pf, targets_list in raw_targets.items():
        counts = Counter(targets_list)
        for target, n in counts.items():
            if n > 1:
                target_domain = mappings.get(target, target)
                errors.append(f"Duplicate interface: '{pf}' has {n} '→' bullets pointing to '{target}' ('{target_domain}'). Merge them into one.")

    # Second pass: verify symmetry
    for source, targets in links.items():
        for target in targets:
            if target not in links or source not in links[target]:
                source_domain = mappings[source]
                target_domain = mappings[target]
                errors.append(f"Asymmetry: '{source}' ('{source_domain}') links to '{target}' ('{target_domain}'), but '{target}' has no reciprocal link to '{source}'.")
                
    return errors

def check_compliance_matching(persona_path, compliance_content):
    with open(persona_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    errors = []
    match = re.search(r"## Compliance & Standards\s*(.*?)\s*(?:##|$)", content, re.DOTALL)
    if match:
        compliance_lines = match.group(1).splitlines()
        for line in compliance_lines:
            line = line.strip()
            if line.startswith("-"):
                std_text = re.sub(r"^-\s*", "", line).strip()
                tokens = re.split(r"[\/\-\(\)]", std_text)
                found_match = False
                stop_words = {"and", "for", "with", "the", "standards", "guidelines", "principles", "standard", "guideline", "testing", "development", "management", "system", "systems", "rules", "specifications", "specification"}
                for token in tokens:
                    token = token.strip()
                    if not token:
                        continue
                    if len(token) > 2 and token.lower() in compliance_content.lower():
                        found_match = True
                        break
                    words = re.findall(r"\b\w{3,}\b", token)
                    for word in words:
                        if word.lower() not in stop_words and word.lower() in compliance_content.lower():
                            found_match = True
                            break
                    if found_match:
                        break
                if not found_match and len(std_text) > 0:
                    errors.append(f"Compliance standard '{std_text}' may be missing or mismatched in compliance.md")
    return errors

def check_frontmatter_body_consistency(persona_path):
    with open(persona_path, "r", encoding="utf-8") as f:
        content = f.read()

    errors = []
    meta, fm_err = parse_frontmatter(content)
    if fm_err or not meta:
        return errors

    fm_role = meta.get("expert_role", "")
    body_match = re.search(r"## Expert Role\s*>\s*You are a \*\*(.+?)\*\*", content)
    if body_match and fm_role:
        body_title = body_match.group(1).strip()
        if body_title.lower() not in fm_role.lower():
            errors.append(f"Frontmatter expert_role does not contain body Expert Role title '{body_title}'")

    fm_domain = meta.get("domain", "")
    title_match = re.search(r"^# (.+?) Persona", content, re.MULTILINE)
    if title_match and fm_domain:
        body_domain = title_match.group(1).strip()
        fm_words = set(re.findall(r'[a-z]{3,}', fm_domain.lower()))
        body_words = set(re.findall(r'[a-z]{3,}', body_domain.lower()))
        def stem_match(w1, w2):
            prefix = min(len(w1), len(w2), 5)
            return w1[:prefix] == w2[:prefix]
        matched = 0
        smaller = fm_words if len(fm_words) <= len(body_words) else body_words
        larger = body_words if len(fm_words) <= len(body_words) else fm_words
        for sw in smaller:
            if any(stem_match(sw, lw) for lw in larger):
                matched += 1
        if len(smaller) > 0 and matched < len(smaller) * 0.5:
            errors.append(f"Frontmatter domain '{fm_domain}' does not match heading '# {body_domain} Persona'")

    return errors


def check_persona_size(persona_path):
    with open(persona_path, "r", encoding="utf-8") as f:
        line_count = sum(1 for _ in f)

    warnings = []
    name = os.path.basename(persona_path)
    if line_count < MIN_PERSONA_LINES:
        warnings.append(f"{name}: Too short ({line_count} lines, minimum {MIN_PERSONA_LINES})")
    elif line_count > MAX_PERSONA_LINES:
        warnings.append(f"{name}: Too long ({line_count} lines, maximum {MAX_PERSONA_LINES})")
    return warnings


def check_detection_signal_collisions():
    if not os.path.exists(SIGNALS_PATH):
        return []

    with open(SIGNALS_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    warnings = []
    signal_map = {}

    for line in content.splitlines():
        if "|" not in line:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 4 or not parts[3].startswith("`personas/"):
            continue

        persona = parts[3]
        signals_raw = parts[1]
        tokens = re.findall(r"`([^`]+)`", signals_raw)
        for token in tokens:
            for sig in re.split(r",\s*", token):
                sig = sig.strip()
                if not sig:
                    continue
                if sig in signal_map:
                    if signal_map[sig] != persona:
                        warnings.append(f"Signal '{sig}' is claimed by both {signal_map[sig]} and {persona}")
                else:
                    signal_map[sig] = persona

    return warnings


def check_matrix_sync(mappings):
    if not os.path.exists(MATRIX_PATH):
        return [f"CROSS_DOMAIN_MATRIX.md not found at {MATRIX_PATH}"]

    with open(MATRIX_PATH, "r", encoding="utf-8") as f:
        matrix_content = f.read()

    warnings = []
    matrix_pairs = set()
    for line in matrix_content.splitlines():
        if "|" not in line or "From Persona" in line:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 4 and parts[1] and parts[2] and not parts[1].startswith("-"):
            from_file = resolve_domain_to_persona_file(parts[1].strip(), mappings)
            to_file = resolve_domain_to_persona_file(parts[2].strip(), mappings)
            if from_file and to_file:
                matrix_pairs.add((from_file, to_file))

    persona_pairs = set()
    for pf, domain in mappings.items():
        pf_path = os.path.join(PERSONAS_DIR, pf)
        if not os.path.exists(pf_path):
            continue

        with open(pf_path, "r", encoding="utf-8") as f:
            content = f.read()

        match = re.search(r"## Cross-Domain Interfaces\s*(.*?)(?:\n## |\Z)", content, re.DOTALL)
        if not match:
            continue

        for line in match.group(1).splitlines():
            m = re.match(r"-\s*\*\*→\s*([^*:]+)(?:\*\*:\s*|:\*\*\s*)", line.strip())
            if m:
                target = m.group(1).strip()
                target_file = resolve_domain_to_persona_file(target, mappings)
                if target_file:
                    persona_pairs.add((pf, target_file))

    persona_only_set = persona_pairs - matrix_pairs
    matrix_only_set = matrix_pairs - persona_pairs

    persona_only = len(persona_only_set)
    matrix_only = len(matrix_only_set)

    if persona_only > 0:
        warnings.append(f"CROSS_DOMAIN_MATRIX.md is missing {persona_only} persona interface(s) (e.g. {list(persona_only_set)[:3]})")
    if matrix_only > 0:
        warnings.append(f"CROSS_DOMAIN_MATRIX.md has {matrix_only} obsolete or unmatched entry/entries (e.g. {list(matrix_only_set)[:3]})")

    return warnings


def check_broken_links():
    errors = []
    for root, dirs, files in os.walk(REPO_ROOT):
        if ".git" in root:
            continue
        for file in files:
            if file.endswith(".md"):
                md_path = os.path.join(root, file)
                with open(md_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)
                for text, url in links:
                    url = url.strip()
                    if url.startswith(("http://", "https://", "mailto:", "#")):
                        continue
                    
                    url_clean = url.split("#")[0]
                    if not url_clean:
                        continue
                    
                    url_clean = urllib.parse.unquote(url_clean)
                    
                    if url_clean.startswith("file:///"):
                        parsed = urllib.parse.urlparse(url_clean)
                        target_path = os.path.normpath(parsed.path)
                        if os.name == 'nt' and target_path.startswith('\\'):
                            if len(target_path) > 2 and target_path[2] == ':':
                                target_path = target_path[1:]
                    else:
                        target_path = os.path.normpath(os.path.join(root, url_clean))
                    
                    if not os.path.exists(target_path):
                        errors.append(f"{os.path.relpath(md_path, REPO_ROOT)}: Broken link to '{url}' (resolved to '{target_path}')")
    return errors

def main():
    print("==================================================")
    print("🛡️  Archon AI Manifesto Validator / Linter  🛡️")
    print("==================================================")
    
    has_errors = False
    
    # 1. Load mappings from detection_signals.md
    mappings = load_domain_mappings()
    
    # 2. Read compliance.md
    if not os.path.exists(COMPLIANCE_PATH):
        print(f"❌ CRITICAL ERROR: {COMPLIANCE_PATH} not found!")
        sys.exit(1)
    with open(COMPLIANCE_PATH, "r", encoding="utf-8") as f:
        compliance_content = f.read()
        
    # Check personas
    print("\n🔍 Checking domain personas...")
    persona_files = [f for f in os.listdir(PERSONAS_DIR) if f.endswith(".md")]
    for pf in sorted(persona_files):
        pf_path = os.path.join(PERSONAS_DIR, pf)
        print(f"  - Analyzing personas/{pf}...")

        # Template & Frontmatter
        template_errors = check_template_integrity(pf_path)
        if template_errors:
            has_errors = True
            for err in template_errors:
                print(f"    ❌ TEMPLATE ERROR: {err}")

        # Frontmatter-body consistency
        consistency_errors = check_frontmatter_body_consistency(pf_path)
        if consistency_errors:
            for err in consistency_errors:
                print(f"    ⚠️  CONSISTENCY WARNING: {err}")

        # Persona file size
        size_warnings = check_persona_size(pf_path)
        if size_warnings:
            for warn in size_warnings:
                print(f"    ⚠️  SIZE WARNING: {warn}")

        # Compliance matching
        compliance_errors = check_compliance_matching(pf_path, compliance_content)
        if compliance_errors:
            for err in compliance_errors:
                print(f"    ⚠️  COMPLIANCE WARNING: {err}")
                
    # 3. Detection Signal Collision Check
    print("\n🔍 Checking detection signal collisions...")
    signal_collisions = check_detection_signal_collisions()
    if signal_collisions:
        for sc in signal_collisions:
            print(f"  ⚠️  SIGNAL COLLISION: {sc}")
    else:
        print("  ✅ No detection signal collisions found.")

    # 4. CROSS_DOMAIN_MATRIX.md Sync Check
    print("\n🔍 Checking CROSS_DOMAIN_MATRIX.md sync...")
    matrix_warnings = check_matrix_sync(mappings)
    if matrix_warnings:
        for mw in matrix_warnings:
            print(f"  ⚠️  MATRIX SYNC: {mw}")
    else:
        print("  ✅ CROSS_DOMAIN_MATRIX.md is in sync with persona interfaces.")

    # 5. Check Bidirectional Symmetry
    print("\n🔍 Checking bidirectional interface symmetry...")
    symmetry_errors = check_bidirectional_interfaces(mappings)
    if symmetry_errors:
        has_errors = True
        for err in symmetry_errors:
            print(f"  ❌ INTERFACE ASYMMETRY: {err}")
    else:
        print("  ✅ All cross-domain interfaces are perfectly symmetrical!")
        
    # 4. Broken Link Verification
    print("\n🔍 Checking for broken links across all markdown files...")
    broken_links = check_broken_links()
    if broken_links:
        has_errors = True
        for bl in broken_links:
            print(f"  ❌ BROKEN LINK: {bl}")
    else:
        print("  ✅ All relative links resolved successfully.")
        
    print("\n==================================================")
    if has_errors:
        print("❌ Linter failed: One or more validation errors found.")
        sys.exit(1)
    else:
        print("✅ Validation complete: Manifesto is clean and fully synchronized!")
        sys.exit(0)

if __name__ == "__main__":
    main()
