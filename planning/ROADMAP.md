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
**Status:** ~~DONE (2026-10-14)~~
**Goal:** Cover current regulations and practices missing from every persona, and add high-regulation domains.
**Tasks:**
- [x] EU Cyber Resilience Act, SBOM / SLSA / Sigstore, NIS2, DORA, OpenTelemetry, ETSI EN 303 645, EN 18031, ISO/IEC 42001, RFC 9457
- [x] LLM / GenAI applications persona (`llm_applications.md`)
- [x] Automotive software persona (`automotive.md`: ISO 26262, ISO/SAE 21434, UN R155/R156, AUTOSAR)
- [x] Medical device software persona (`medical_device.md`: IEC 62304, ISO 14971, EU MDR, FDA QMSR / 524B)

## M-009 · PCB design guide integration
**Priority:** P1
**Status:** ~~DONE (2026-11-21)~~
**Goal:** Bring the reusable rules of the user's PCB design guide (v3.1) into Archon: generic audit rules into the engine (D-010), PCB depth into `hardware_design.md` (D-009).
**Tasks:**
- [x] Persona size limit 400 lines; template ranges widened
- [x] Engine: evidence tags, absolute dates, applicability, rule traceability, source precedence, explicit approval, supersede-not-delete, session handoff
- [x] `hardware_design.md`: 12 Hard Rules, 16 pitfalls, 8 budgets, source-document gate, stack-up, material, PDN, interface reference, EMC, via/HDI/flex, DFM/DFA/DFT, cost and sourcing, design gates, simulation and bring-up tests
- [x] `compliance.md`: IPC-2152, IPC-4101, IPC-4761, IPC-6012, IPC-A-600, IPC-2581, IPC-D-356, IEC 60664-1, IEC 61010-1, CISPR 32, CISPR 11, IEC 61000-4-2, IEC 61249-2-21, J-STD-020 / J-STD-033, IEC 60204-1
- [x] `detection_signals.md`: `*.kicad_sch`, `*.kicad_pro`, `*.PcbDoc`

## M-010 · Profiles and web verification of PCB values
**Priority:** P1
**Status:** ~~DONE (2026-11-21)~~
**Goal:** Keep the tool-, vendor-, and region-specific parts of the PCB guide as reusable profiles (D-011) and verify the numbers added in M-009 (KI-040).
**Tasks:**
- [x] Web check of persona values; 10 corrections (KI-040)
- [x] `PROFILE_TEMPLATE.md`, `profiles/eda_kicad.md`, `fab_jlcpcb.md`, `sourcing_base.md`, `sourcing_tr.md`
- [x] Phase 0 Step 2b, Source Precedence, AGENTS.md spec, validator PROFILE check, `bootstrap_target.py --profile`, tests
- [x] `hardware_design.md`: schematic conventions, schematic equivalence, DRC rule tests, independent calculation check, layer connectivity report, release manifest
