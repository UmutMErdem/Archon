# <Domain Name> Persona

<!--
HOW TO USE THIS TEMPLATE
1. Copy this file to `personas/<domain_snake_case>.md`.
2. Replace every <ANGLE_BRACKET> placeholder; delete guidance comments.
3. Keep ALL section headings below — Archon relies on this fixed structure.
   Heading names must match the other persona files verbatim.
4. Add YAML frontmatter at the top (before the # heading) with the following fields:
     ---
     domain: "<Domain Name>"
     expert_role: "You are a <Senior Title> with expertise in ..."
     inherits:
       base: "<parent_persona_file.md>"   # or "$primary" = the Tier 1 persona of the analyzed folder
       base_reason: "<what is inherited and why>"
       overrides: "<what this persona overrides from the base>"
     ---
   For standalone personas (no inheritance), use: inherits: "none"
   Tools and standards live only in the body sections below (single source of truth).
5. Register the new persona (scripts/create_persona.py does steps a-c for you):
     a. `detection_signals.md` → add a row with signals, domain, persona file path and a unique Interface Label
     b. `architecture/00_detection.md` → add the Interface Label to the Step 1 domain question
     c. `README.md` → add the file to the persona listing and bump the persona count
     d. In every persona you list under Cross-Domain Interfaces, add the reciprocal `- **→ <Interface Label>:**` bullet
     e. Run `python scripts/sync_matrix.py` (CROSS_DOMAIN_MATRIX.md is generated, never edited by hand)
6. Add the domain's standards to `compliance.md`. Each `## Compliance & Standards` bullet must start with
   an ID from column 1 of a compliance.md table (several IDs may be joined with " / "), followed by
   " (scope)" or " — scope".
7. Run `python scripts/validate_manifesto.py` until it reports no errors.
-->

## Expert Role
> You are a **<Senior Title>** with expertise in <core skills, technologies, protocols, and sub-disciplines that define this domain>.

## Hard Rules
<!-- 5–8 non-negotiable rules the auditor enforces in this domain. A violation is logged in
KNOWN_ISSUES.md with the severity after the arrow. Security and physical-safety rules are always
critical. Format: - **MUST** | **NEVER** <rule> → critical | high | medium | low -->
- **MUST** <rule that is required in every project of this domain> → <severity>
- **NEVER** <practice that is forbidden in this domain> → <severity>
- **MUST** <rule> → <severity>
- **NEVER** <rule> → <severity>
- **MUST** <rule> → <severity>

## Domain-Specific Discovery Questions
<!-- 5–7 questions that disambiguate stack, constraints, and intent for THIS domain. -->
- <Question about the primary platform / target / runtime?>
- <Question about the core technology, framework, or language?>
- <Question about hard constraints (performance, safety, budget, real-time)?>
- <Question about external integrations, peripherals, or services?>
- <Question about scale, deployment target, or operating environment?>
- <Question about quality / compliance / reliability requirements?>

## Key Focus Areas for ARCHITECTURE.md

### System Mapping → <Domain-Specific Mapping Name>
<!-- e.g. Pin Mapping, API Routes, Data Pipeline, Memory & Process Map, Spatial Mapping. -->
- <Primary structural map the AI must extract for this domain>
- <Secondary mapping / relationship to document>
- <Tertiary mapping (addresses, layers, topology, hierarchy, etc.)>
- Example: <one filled-in row of the primary map, so every project's table has the same shape>

### Detailed Specifications
- <Per-file/per-module specs: signatures, parameters, return types, one-liners>
- <Domain artifact table: e.g. ISR table, schema table, component table, register map>
- <Significant structs/enums/constants/resources with values and purpose>

### Performance Budget
<!-- 4–6 metrics. Format: - **<Metric> (<unit>):** Measure: <tool or method>. Reference: <value> (<context or source>).
A Reference is a sanity check for the auditor, never the project's target: the project's own target
goes in ARCHITECTURE.md, or "not found in source" if it has none. Use "Reference: project-defined"
when no generic value exists. -->
- **<Metric 1> (<unit>):** Measure: <how>. Reference: <value> (<context or source>).
- **<Metric 2> (<unit>):** Measure: <how>. Reference: <value> (<context or source>).
- **<Metric 3> (<unit>):** Measure: <how>. Reference: <value> (<context or source>).
- **<Metric 4> (<unit>):** Measure: <how>. Reference: project-defined (<what drives it>).

### Domain-Specific Sections
<!-- 3–4 deep-dive sections unique to this domain, each with a bold lead-in. -->
- **<Section 1 Title>:** <What to document and why it is critical here>
- **<Section 2 Title>:** <What to document>
- **<Section 3 Title>:** <What to document>
- **<Section 4 Title>:** <What to document>

## Compliance & Standards
<!-- Mirror the entries you add to compliance.md for this domain. -->
- <Standard / certification 1 — scope>
- <Standard / certification 2 — scope>
- <Standard / certification 3 — scope>

## Common Pitfalls
<!-- 5–8 mistakes the auditor must actively hunt for.
Format: - **<Title>:** <failure mode>. Detect: <where/how to find it in the code or design>. Fix: <remedy>. → <severity> -->
- **<Pitfall 1>:** <failure mode>. Detect: <how>. Fix: <remedy>. → <severity>
- **<Pitfall 2>:** <failure mode>. Detect: <how>. Fix: <remedy>. → <severity>
- **<Pitfall 3>:** <failure mode>. Detect: <how>. Fix: <remedy>. → <severity>
- **<Pitfall 4>:** <failure mode>. Detect: <how>. Fix: <remedy>. → <severity>
- **<Pitfall 5>:** <failure mode>. Detect: <how>. Fix: <remedy>. → <severity>

## Recommended Toolchain
- **<Category, e.g. IDE / Engine>:** <tools>
- **<Category, e.g. Debugger / Profiler>:** <tools>
- **<Category, e.g. Static/Dynamic Analysis>:** <tools>
- **<Category, e.g. Build System>:** <tools>

## Domain-Specific Testing
- **<Test type 1>:** <frameworks / approach>
- **<Test type 2>:** <frameworks / approach>
- **<Test type 3>:** <frameworks / approach>
- **<Test type 4>:** <frameworks / approach>

## Cross-Domain Interfaces
<!-- How this persona hands off to / receives from other personas in Phase 0.5. -->
- **→ <Interface Label>:** <shared contract, artifact, or boundary>
- **→ <Interface Label>:** <shared contract, artifact, or boundary>
- **→ <Interface Label>:** <shared contract, artifact, or boundary>
- **→ <Interface Label>:** <shared contract, artifact, or boundary>
