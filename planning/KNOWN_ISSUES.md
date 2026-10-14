# KNOWN_ISSUES.md
> Bug/issue tracker. Format: KI-NNN | severity | status.
> KI-001…KI-038 come from the 2026-10-13 full review; all were fixed on branch `fix/review-plan`. IDs KI-024 and KI-028 were not assigned.
---
## KI-038 · Tier 2 count contradicted the Tier 2 assignment rule
**Status:** FIXED 2026-10-14 · **Severity:** medium
**Symptom:** Tier table allowed 1–3 Tier 2 personas, but rule 2 made every interface partner of Tier 1 a candidate (up to 21 for web).
**Root cause:** `architecture/00_detection.md` tier table vs rule 2.
**Fix:** Count `0–3`; candidates need their own strong signals; capped at 3 with a tie-break. Implemented in `scripts/detect_domain.py`.

## KI-037 · `graphify_helper.py --path X` exited 0 without building
**Status:** FIXED 2026-10-14 · **Severity:** medium
**Symptom:** Build ran only when `len(sys.argv) == 1`.
**Fix:** Build is the default action whenever no other action flag is given.

## KI-036 · `create_persona.py` corrupted `00_detection.md` on the second run
**Status:** FIXED 2026-10-14 · **Severity:** high
**Symptom:** Fallback regex appended the new domain to `#### Detection Signals (auto-detect before asking)`.
**Fix:** Anchored regex on the Step 1 question line; idempotent; missing anchor is an error.

## KI-035 · `rules.md` "no placeholders" vs deferred-module placeholders
**Status:** FIXED 2026-10-14 · **Severity:** low
**Fix:** `[DEFERRED — shallow scan only]` summary entries are an explicit exception in both files.

## KI-034 · Validator warnings never failed CI
**Status:** FIXED 2026-10-14 · **Severity:** high
**Symptom:** Consistency, compliance, collision, and matrix-sync findings printed ⚠️ and exited 0.
**Fix:** All findings except persona size are errors (D-006).

## KI-033 · CI workflow had no `permissions:` block
**Status:** FIXED 2026-10-14 · **Severity:** critical (security rule; real risk low)
**Fix:** `permissions: contents: read` at workflow level.

## KI-032 · Graphify output stale and Markdown-blind
**Status:** FIXED 2026-10-14 · **Severity:** low
**Fix:** Documented in README Development section (graph covers `scripts/` only; rebuild with `--update`).

## KI-031 · Two finding-ID schemes (`I-NNN`/`O-NN` vs `KI-NNN`/`F-NN`)
**Status:** FIXED 2026-10-14 · **Severity:** low
**Fix:** D-001.

## KI-030 · Outdated standards in personas and compliance.md
**Status:** FIXED 2026-10-14 · **Severity:** low
**Fix:** FID→INP, WCAG 2.1→2.2, RFC 7231→RFC 9110, Machinery Directive→Regulation (EU) 2023/1230, W3C CORS→WHATWG Fetch.

## KI-029 · CROSS_DOMAIN_MATRIX.md claimed to be the source of truth
**Status:** FIXED 2026-10-14 · **Severity:** low
**Fix:** Header now says it is generated from personas by `sync_matrix.py`.

## KI-027 · Path traversal in `create_persona.py` filename
**Status:** FIXED 2026-10-14 · **Severity:** critical (security rule; real risk low, local CLI)
**Symptom:** `../README.md` wrote outside `personas/`; quotes in the domain broke YAML.
**Fix:** Filename must match `[a-z0-9_]+.md`; values written as JSON strings (valid YAML).

## KI-026 · `create_persona.py` hardcoded `python`
**Status:** FIXED 2026-10-14 · **Severity:** low
**Fix:** `sys.executable`.

## KI-025 · `graphify_helper.py` swallowed failures
**Status:** FIXED 2026-10-14 · **Severity:** low
**Fix:** Every step's result counts; failures exit 1; PATH re-checked after install.

## KI-023 · Misleading detection signals
**Status:** FIXED 2026-10-14 · **Severity:** medium
**Symptom:** `*requirements*.txt` routed every Python project (including Archon) to Product Management; `*.swift` in web and mobile rows; generic `*.json`, `docs/`, `*.csv`, `*.m`.
**Fix:** Weak Signals column (never selects Tier 1), named-file-beats-glob rule, glob-overlap check in the validator.

## KI-022 · Turkish-only, ASCII-folded system prompt and hard-coded reply language
**Status:** FIXED 2026-10-14 · **Severity:** low
**Fix:** `rules.md` replies in the user's language; README ships English and correctly-spelled Turkish prompts.

## KI-021 · "Read every source file" vs Phase 0.7 scope control
**Status:** FIXED 2026-10-14 · **Severity:** medium
**Fix:** Rule now says "in scope (see Phase 0.7)".

## KI-020 · QA inheritance hard-wired to web persona
**Status:** FIXED 2026-10-14 · **Severity:** low
**Fix:** D-005.

## KI-019 · `05_orchestration.md` referenced a non-existent `## Inherits` section
**Status:** FIXED 2026-10-14 · **Severity:** low
**Fix:** Points to the `inherits:` frontmatter key.

## KI-018 · `00_detection.md` referenced "the general template below" that did not exist
**Status:** FIXED 2026-10-14 · **Severity:** low
**Fix:** Links `files_spec.md` and `PERSONA_TEMPLATE.md`.

## KI-017 · Phase 0 linked a git-ignored SVG
**Status:** FIXED 2026-10-14 · **Severity:** medium
**Fix:** ARCHITECTURE.md gets a "run `--build`, open `graph.html`" instruction instead of a dead link.

## KI-016 · Bootstrap output violated Archon's own spec
**Status:** FIXED 2026-10-14 · **Severity:** medium
**Fix:** Skeletons derived from `architecture/files_spec.md` (all 13 ARCHITECTURE.md sections, KI/F formats), no placeholders.

## KI-015 · Step 3 contradicted the README prompt
**Status:** FIXED 2026-10-14 · **Severity:** medium
**Fix:** Single rule in Step 3 (existing codebase → analyze, then ask what the code cannot answer); `Status: SCAFFOLDED` marks bootstrap skeletons.

## KI-014 · Unresolved interface targets reported as asymmetry
**Status:** FIXED 2026-10-14 · **Severity:** low
**Fix:** Separate `UNRESOLVED`, `LABEL`, `SELF`, `DUPLICATE`, `ASYMMETRY` categories.

## KI-013 · Link walker skipped `.github/`, scanned `graphify-out/`, ignored anchors
**Status:** FIXED 2026-10-14 · **Severity:** low
**Fix:** Uses `git ls-files`; skips generated dirs; validates `#anchors` with GitHub slugs; flags `file:` links.

## KI-012 · Validator missed registry, inheritance, and placeholder errors
**Status:** FIXED 2026-10-14 · **Severity:** medium
**Fix:** New checks: registry ↔ files ↔ README ↔ Phase 0 question, unique labels, `inherits` base, `<placeholder>` detection.

## KI-011 · Compliance matcher accepted any shared word
**Status:** FIXED 2026-10-14 · **Severity:** medium
**Symptom:** 57 of 131 persona standard bullets did not match a `compliance.md` ID, yet 0 warnings.
**Fix:** Exact ID matching; 8 missing standards added, 39 spellings canonicalized, 10 practices moved to a non-normative table.

## KI-010 · Bogus Hardware Design ↔ Security Compliance interface
**Status:** FIXED 2026-10-14 · **Severity:** medium
**Fix:** Both bullets deleted (created by the fuzzy resolver mapping "Compliance").

## KI-009 · Fuzzy domain resolver mis-resolved labels
**Status:** FIXED 2026-10-14 · **Severity:** medium
**Fix:** Exact resolver over registry labels (D-003).

## KI-008 · Frontmatter lists drifted from body sections
**Status:** FIXED 2026-10-14 · **Severity:** medium
**Fix:** Lists removed (D-004).

## KI-007 · Machine-specific path in `00_detection.md`
**Status:** FIXED 2026-10-14 · **Severity:** medium
**Fix:** `<ARCHON_ROOT>` defined once at the top of the file.

## KI-006 · Unpinned automatic package installation
**Status:** FIXED 2026-10-14 · **Severity:** critical (security rule; real risk medium)
**Symptom:** Any `graphify_helper.py` call (also via bootstrap) ran `pip install graphifyy` without consent or version pin.
**Fix:** Install only with `--install`/`--install-only`; pinned `graphifyy==0.9.90`.

## KI-005 · Bootstrap wrote `file:///` links
**Status:** FIXED 2026-10-14 · **Severity:** medium
**Fix:** Plain-text persona references with Archon version; validator rejects `file:` links.

## KI-004 · Bootstrap overwrote existing target files
**Status:** FIXED 2026-10-14 · **Severity:** high
**Fix:** Existing files are skipped and listed; `--force` to overwrite.

## KI-003 · `create_persona.py` produced invalid personas and fake signals
**Status:** FIXED 2026-10-14 · **Severity:** high
**Fix:** Real signals and interface labels required; title kept; registry row includes label; validator result is the exit code.

## KI-002 · `generate_diagram.py` appended ~252 lines per run
**Status:** FIXED 2026-10-14 · **Severity:** high
**Fix:** D-002 (single generator with `--check`).

## KI-001 · Migration scripts crashed on a wrong REPO_ROOT
**Status:** FIXED 2026-10-14 · **Severity:** high
**Fix:** `scripts/migrations/` deleted (already applied; history keeps them).
