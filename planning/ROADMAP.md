# ROADMAP.md
> Prioritized milestones. Update PROJECT_STATE.md on completion.
---
## M-001 · Stop data-destroying and broken tools
**Priority:** P0
**Status:** ~~DONE (2026-10-14)~~
**Goal:** No script corrupts files, installs packages without consent, or reports false success.
**Tasks:**
- [x] KI-001, KI-002, KI-003, KI-004, KI-005, KI-006, KI-027, KI-033, KI-036, KI-037

## M-002 · Remove engine doc contradictions
**Priority:** P0
**Status:** ~~DONE (2026-10-14)~~
**Goal:** `architecture/*.md` and README agree and reference only things that exist.
**Tasks:**
- [x] KI-007, KI-015, KI-017, KI-018, KI-019, KI-020, KI-021, KI-022, KI-029, KI-031, KI-035, KI-038

## M-003 · Harden the validator and fix the data it exposes
**Priority:** P1
**Status:** ~~DONE (2026-10-14)~~
**Goal:** Every class of hand-found error is a validator error; the repo validates clean.
**Tasks:**
- [x] KI-008, KI-009, KI-010, KI-011, KI-012, KI-013, KI-014, KI-023, KI-034

## M-004 · Consolidation, tests, CI
**Priority:** P1
**Status:** ~~DONE (2026-10-14)~~
**Goal:** Shared core module, coverage ≥ 80 %, deterministic CI.
**Tasks:**
- [x] F-02, F-03, F-05, F-06, F-07, F-08, F-09, F-11, F-17, KI-016, KI-025, KI-026

## M-005 · Content refresh, UX, dogfooding
**Priority:** P2
**Status:** ~~DONE (2026-10-14)~~
**Goal:** Current standards, complete README, Archon follows its own rules.
**Tasks:**
- [x] KI-030, KI-032, F-01, F-04, F-10, F-12, F-13, F-14, F-15, F-16

## M-006 · Release v0.1.0
**Priority:** P2
**Status:** ~~DONE (2026-10-14)~~
**Goal:** First tagged manifesto version so target projects can record which Archon they used.
**Tasks:**
- [x] Merge `fix/review-plan` into `main` (PR #1)
- [x] Tag `v0.1.0` (bootstrap then writes it via `git describe`)

## M-007 · Persona depth
**Priority:** P1
**Status:** ~~DONE (2026-10-14)~~
**Goal:** Personas tell the auditor how to judge a project, not only what to document (D-008).
**Tasks:**
- [x] Template and `check_depth` validator rule
- [x] Pilots: `embedded_iot.md`, `ai_ml.md`
- [x] Remaining 25 personas; DEPTH check enforced

## M-008 · Content gaps and new personas
**Priority:** P1
**Status:** OPEN
**Goal:** Cover current regulations and practices missing from every persona, and add high-regulation domains.
**Tasks:**
- [ ] EU Cyber Resilience Act, SBOM / SLSA / Sigstore, NIS2, DORA, OpenTelemetry, ETSI EN 303 645, RFC 9457
- [ ] LLM / GenAI applications persona
- [ ] Automotive software persona (ISO 26262, ISO/SAE 21434, AUTOSAR)
- [ ] Medical device software persona (IEC 62304, ISO 14971)
