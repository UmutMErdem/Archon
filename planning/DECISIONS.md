# DECISIONS.md
> Design/architecture decision log. Newest first.
---
## D-011 · Profiles bind personas to tools, vendors, and regions
**Date:** 2026-11-21
**Decision:** New `profiles/` folder. A profile (`type: eda | fab | sourcing`) holds what is specific to one EDA tool, fabricator, or sourcing region: bindings from persona rules to that tool, a Values table where every row has a Source and a Checked date, a procedure, and pitfalls. `extends` lets a regional profile reuse a base (`sourcing_tr.md` → `sourcing_base.md`). Phase 0 Step 2b loads profiles by `applies_to` and `signals`, re-verifies values older than 180 days, and records them in the target's AGENTS.md; `bootstrap_target.py --profile` does the same. The validator checks the contract (category PROFILE).
**Rationale:** The PCB guide mixed generic rules with KiCad commands, one fabricator's capability numbers, Turkish suppliers, and one workbook layout. In a persona these would be wrong for every other tool, fabricator, or country; dropping them lost real value. A dated, sourced profile keeps them usable and makes staleness visible.
**Impact:** Personas stay vendor-neutral. Adding a tool, fabricator, or region is a new profile file, not a persona edit. Profile values rank at Source Precedence level 4, below the live vendor page.

## D-010 · Generic audit rules taken from the PCB design guide
**Date:** 2026-11-21
**Decision:** Five rules from the user's PCB design guide (v3.1, sections 0.2, 0.6–0.8) become domain-independent engine rules: evidence tags `[verified]` / `[hypothesis]` / `[estimate]`, absolute dates, justified not-applicable verdicts with "applicable when unsure", explicit-only user approval, superseding instead of deleting decisions, plus a source precedence order and a session handoff section in PROJECT_STATE.md. PCB-specific content goes into `personas/hardware_design.md` only.
**Rationale:** Each rule prevents a failure that is not specific to PCBs: unrun tests reported as done, relative dates that lose meaning in the next session, silently skipped conditional rules, another agent's message taken as approval, and a later session repeating an approach that already failed.
**Impact:** `architecture/rules.md`, `05_orchestration.md`, `06_maintenance.md`, `files_spec.md`. Personas may write conditional Hard Rules as `**MUST** (if <trigger>) …`.

## D-009 · Persona size limit 400 lines
**Date:** 2026-11-21
**Decision:** `MAX_PERSONA_LINES` goes from 200 to 400; template ranges widen (Hard Rules 5–12, questions 5–10, budgets 4–8, domain sections 3 or more, pitfalls 5–16). The size check stays warning-only (D-006).
**Rationale:** 200 lines was set when personas were checklists. Since D-008 a deep domain such as PCB design needs sourced numeric rules (stack-up, PDN, creepage, termination) that do not fit. A Tier 1 persona is loaded whole, so the limit still caps context cost: 400 lines is roughly 15–25 k tokens.
**Impact:** Only `hardware_design.md` uses the extra room now. New depth must change an audit verdict, not restate textbook material.

## D-008 · Persona depth format: hard rules, Detect/Fix pitfalls, references not targets
**Date:** 2026-10-14
**Decision:** Every persona has `## Hard Rules` (5–8 MUST/NEVER rules ending in a KNOWN_ISSUES severity), pitfalls in the form `**Title:** failure. Detect: … Fix: … → severity`, Performance Budget items as `**Metric (unit):** Measure: … Reference: …`, and a filled `- Example:` row in System Mapping. `validate_manifesto.py` enforces the shapes (category DEPTH).
**Rationale:** The review found personas described what to document but not how to judge it: no MUST/NEVER rules, one-line pitfalls without detection hints or severity, and 9 budgets with no numbers while others hardcoded arbitrary targets (e.g. "1000 req/s"), which contradicts the "do not invent" rule.
**Impact:** A Reference is a sanity check with its source (standard, vendor guidance, physics), never the project's target; the target goes into the target project's ARCHITECTURE.md or is reported as "not found in source". Security and physical-safety rules are always `critical`.

## D-007 · Pinned, split requirements
**Date:** 2026-10-14
**Decision:** `requirements.txt` is replaced by `requirements-dev.txt` (pinned black/ruff/pytest/pytest-cov) and optional `requirements-graphify.txt` (pinned `graphifyy`). Tool config lives in `pyproject.toml`.
**Rationale:** Unpinned `black>=23` changes its stable style every January and breaks CI by itself; CI never needed graphify because tests mock it.
**Impact:** Bump pins deliberately; keep `GRAPHIFY_REQUIREMENT` in `scripts/graphify_helper.py` equal to the graphify pin.

## D-006 · Validator findings are errors
**Date:** 2026-10-14
**Decision:** Every check except persona size sets the exit code. No `--strict` flag.
**Rationale:** Five warning-only checks (consistency, compliance, collisions, matrix sync) let real drift pass CI. All data was fixed in the same change, so a strict default costs nothing.
**Impact:** New checks must be clean on the current repo when they land.

## D-005 · `$primary` inheritance token
**Date:** 2026-10-14
**Decision:** `inherits.base` may be `$primary`, meaning the Tier 1 persona of the analyzed folder. `qa_testing.md` uses it.
**Rationale:** QA inherited `web_mobile_apps.md` unconditionally, so embedded projects got web packaging rules. The orchestration doc already described dynamic inheritance.
**Impact:** Validator accepts `$primary`; `05_orchestration.md` documents it.

## D-004 · Persona frontmatter without tool/standard lists
**Date:** 2026-10-14
**Decision:** `recommended_tools` and `compliance` were removed from persona frontmatter.
**Rationale:** They duplicated the body sections and had already drifted in 21 files (hyphens stripped: `NIST SP 80053`, `JLink`). No script consumed them.
**Impact:** Body sections are the single source; `PERSONA_TEMPLATE.md` and `create_persona.py` updated.

## D-003 · Interface labels live in the registry
**Date:** 2026-10-14
**Decision:** `detection_signals.md` gets an **Interface Label** column; interface bullets must use it verbatim and the resolver matches exactly (label, domain name, or file stem).
**Rationale:** 36 label spellings for 27 personas forced a fuzzy resolver that mapped `Testing`→cybersecurity and `Compliance`→security_compliance (which produced a bogus interface pair).
**Impact:** `create_persona.py` registers the label in one place; no code edit is needed for a new persona.

## D-002 · One generator for CROSS_DOMAIN_MATRIX.md
**Date:** 2026-10-14
**Decision:** `generate_diagram.py` merged into `sync_matrix.py`, which renders the table and a single undirected, completeness-colored diagram. `--check` guards freshness in CI.
**Rationale:** Two writers disagreed on section boundaries; `generate_diagram.py` appended ~252 orphan lines per run. Two diagrams of the same 212 edges doubled the file.
**Impact:** Matrix went from 734 to 371 lines; completeness column removed from `detection_signals.md` (it is a quality metric, not routing data).

## D-001 · Target-project finding IDs are KI-NNN / F-NN
**Date:** 2026-10-14
**Decision:** `files_spec.md` and `06_maintenance.md` use `KI-NNN` (issues) and `F-NN` (optimizations) instead of `I-NNN` / `O-NN`.
**Rationale:** Matches the maintainer's convention used across their projects; avoids two ID schemes in one target repo.
**Impact:** Existing target projects using `I-NNN` keep working but new output uses the new IDs.
