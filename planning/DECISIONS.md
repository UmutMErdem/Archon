# DECISIONS.md
> Design/architecture decision log. Newest first.
---
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
