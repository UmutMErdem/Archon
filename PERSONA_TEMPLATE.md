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
     recommended_tools: ["<Tool 1>", "<Tool 2>"]
     compliance: ["<Standard 1>", "<Standard 2>"]
     inherits:
       base: "<parent_persona_file.md>"
       base_reason: "<what is inherited and why>"
       overrides: "<what this persona overrides from the base>"
     ---
   For standalone personas (no inheritance), use: inherits: "none"
5. Register the new persona in FOUR places:
     - `architecture/00_detection.md` → Step 1 domain list (the user-facing question)
     - `detection_signals.md` → Add a row with file/config heuristics and persona file path
     - `CROSS_DOMAIN_MATRIX.md` → Add cross-domain interface entries
     - `README.md` → Add to the persona listing
6. Add the domain's standards to `compliance.md`.
-->

## Expert Role
> You are a **<Senior Title>** with expertise in <core skills, technologies, protocols, and sub-disciplines that define this domain>.

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

### Detailed Specifications
- <Per-file/per-module specs: signatures, parameters, return types, one-liners>
- <Domain artifact table: e.g. ISR table, schema table, component table, register map>
- <Significant structs/enums/constants/resources with values and purpose>

### Performance Budget
<!-- Quantified limits specific to this domain. Always give units. -->
- <Metric 1 with unit and target (e.g. latency µs/ms, throughput Mbps)>
- <Metric 2 with unit and target (e.g. memory MB, Flash/RAM %, VRAM)>
- <Metric 3 with unit and target (e.g. fps, query latency, startup ms)>
- <Resource ceiling (CPU %, nodes, draw calls, binary size, power µA/mA)>

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
<!-- Concrete, domain-specific mistakes the auditor must actively hunt for. -->
- <Pitfall 1 — the failure mode it causes>
- <Pitfall 2>
- <Pitfall 3>
- <Pitfall 4>
- <Pitfall 5>

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
- **→ <Other Domain>:** <shared contract, artifact, or boundary>
- **→ <Other Domain>:** <shared contract, artifact, or boundary>
- **→ <Other Domain>:** <shared contract, artifact, or boundary>
- **→ <Other Domain>:** <shared contract, artifact, or boundary>
