# KNOWN_ISSUES.md
> Bug/issue tracker. Format: KI-NNN | severity | status.
> KI-001…KI-038 come from the 2026-10-13 full review; all were fixed on branch `fix/review-plan`. IDs KI-024 and KI-028 were not assigned.
---
## KI-040 · PCB guide values in hardware_design were stated more precisely than sources support
**Status:** FIXED 2026-11-21 · **Severity:** medium
**Symptom:** A web check of the numeric references added in M-009 found values that were too absolute, outdated, or presented as standard text when they come from one handbook.
**Root cause:** Values were copied from the user's PCB guide (built from fabricator e-books) without an independent check. [verified] by the searches below; the IPC/IEC texts themselves are paywalled, so the sources are vendor application notes and secondary summaries.
**Fix:**
| Topic | Was | Now | Source |
|---|---|---|---|
| PCIe impedance | "85 or 100 Ω by generation" | Gen1/2 100 Ω, Gen3+ 85 Ω | [TI SLAAE45](https://www.ti.com/document-viewer/lit/html/SLAAE45/GUID-20D0DD8D-AB27-4081-983E-5BC21CAE3A14) |
| MIPI D-PHY | 100 Ω | 90–100 Ω, per device layout guide | [Intel MIPI layout](https://www.intel.com/content/www/us/en/docs/programmable/817561/24-1-2-2-0/mipi-interface-layout-design-guidelines.html), [AMD UG863](https://docs.amd.com/r/en-US/ug863-versal-pcb-design/MIPI-D-PHY) |
| ENIG gold | Au 0.05–0.10 µm | Au per IPC-4552 revision, 0.04 µm minimum since the 2012 amendment | [SMTA paper on IPC-4552A](https://smtnet.com/library/files/upload/Achieving-A-Successful-ENIG-Finished-PCB-Under-Revision-A-Of-IPC-4552-SMTAI-2017-Paper.pdf) |
| PTH fill | ≥ 75 % for Class 2 and 3 | Class 3 always 75 %; Class 2 accepts 50 % in listed cases | [IPC E16&S29-02](https://www.ipc.org/system/files/technical_resource/E16%26S29-02.pdf) |
| Flex bend radius | 6× / 10× / 20–40× / 100× as fixed | Commonly cited values; multilayer 12–24×; confirm with IPC-2223 | [JLCPCB bend radius](https://jlcpcb.com/blog/flex-pcb-bend-radius-calculation-minimum-radius-design-guidelines) |
| Courtyard | 0.15 mm below 0603, 0.5 mm connectors | Only IPC-7351B nominal 0.25 mm and BGA 1.0 mm kept | [PCB Libraries forum, Table 3-17](https://www.pcblibraries.com/forum/topic1752.html) |
| Via stubs | USB3 0.3 / PCIe3 0.25 / 10GbE 0.2 mm | Vendor layout guide; typical 10–15 mil at 5–8 Gbps | [TI SLLA414](https://ti.com/lit/slla414), [Protoexpress back-drilling](https://www.protoexpress.com/blog/back-drilling-pcb-design-and-manufacturing/) |
| Tg margin | 20–25 °C | 20–30 °C rule of thumb, plus laminate UL MOT | [Eurocircuits Tg](https://www.eurocircuits.com/?p=9358) |
| I²C capacitance | 400 pF | 400 pF, 550 pF in Fast-mode Plus | [I²C spec v2.1](https://www.csd.uoc.gr/~hy428/reading/i2c_spec.pdf) |
| RS-485 failsafe | "required" | One bias network per bus, both ends on long cables | [Renesas AN1986](https://renesas.com/en/document/apn/an1986-external-fail-safe-biasing-rs-485-networks) |

Verified unchanged: USB 2.0 90 Ω ±15 % / 45 Ω SE, HDMI and SATA 100 Ω, ES1 60 V DC / 30 V RMS / 42.4 V peak, IEC 60204-1 e-stop category 0 or 1 by risk assessment, IPC-4101 lead-free slash sheets, IPC-4761 Type VII, IEC 61249-2-21 (Br, Cl < 900 ppm, sum < 1500 ppm), IPC-6012 bow/twist 0.75 % / 1.5 %, IPC-T-50 microvia (AR ≤ 1:1, depth ≤ 0.25 mm), RS-485/CAN termination at both ends, KiCad custom rules (last match wins, Board Setup is a floor). Not verifiable from open sources: IEC 60664-1 Table A.2 altitude factors (not quoted in the persona).

---
## KI-039 · Persona reference values contained unverified or wrong facts
**Status:** FIXED 2026-10-14 · **Severity:** medium
**Symptom:** A web check of every dated or numeric reference added in M-007/M-008 found wrong or stale statements.
**Root cause:** References were written from memory without source verification.
**Fix:** Corrected after checking primary or vendor sources:
| Persona | Was | Now | Source |
|---|---|---|---|
| cybersecurity | CISA BOD 22-01, ~2 weeks for KEV CVEs | BOD 26-04 (2026-06-10) supersedes and revokes BOD 22-01; risk-based deadlines down to 3 days | [CISA directives](https://www.cisa.gov/news-events/directives), [BOD 22-01 (Revoked)](https://www.cisa.gov/news-events/directives/bod-22-01-reducing-significant-risk-known-exploited-vulnerabilities-revoked) |
| fpga_digital | "UltraFast: hard above 70–80 % LUT" | Congestion judged from `report_design_analysis -congestion`; no such percentage in UG949 | [AMD UG949](https://docs.amd.com/r/en-US/ug949-vivado-design-methodology/Congestion-Area-and-Level-Definition) |
| devops | DORA elite lead time < 1 day | Compare with the current DORA clusters; elite failed-deployment recovery < 1 h | [Apache DevLake on DORA 2023](https://devlake.apache.org/docs/Metrics/FailedDeploymentRecoveryTime) |
| ar_vr_xr | "low hundreds" draw calls | Meta Unity Runtime Optimizer target < 300 | [Meta Quest runtime optimizer](https://developers.meta.com/vr/documentation/unity/unity-quest-runtime-optimizer/) |
| hardware_design | TPS62133 as 3.3 V buck | TPS62132 (TPS62133 is the 5 V variant) | [TI TPS62133](https://www.ti.com/product/TPS62133) |
| automation | PROFINET RT "commonly 1–4 ms" | Update times from 250 µs; many applications at 1 ms | [PROFINET real-time classes](https://profinetuniversity.com/profinet-basics/profinet-real-time-classes/) |
| blockchain | ERC-20 transfer ~50k gas | 50k–65k depending on implementation | [OpenZeppelin forum](https://forum.openzeppelin.com/t/deploying-erc20-and-cost-of-transfers/4883) |
| robotics | PREEMPT_RT "tens of µs" | Tens of µs on tuned x86, ~100 µs+ on embedded boards under load | [arXiv 2307.04148](https://arxiv.org/pdf/2307.04148) |
| llm_applications | OpenTelemetry GenAI conventions | Marked as still in development | [semantic-conventions-genai](https://github.com/open-telemetry/semantic-conventions-genai) |
| automotive | MC/DC "as ISO 26262 recommends" | Coverage per ISO 26262-6 Table 12 by ASIL | ISO 26262-6:2018 Table 12 |

Verified unchanged: EU CRA dates, EN 18031 / RED DA (2025-08-01), Machinery Regulation (2027-01-20), DORA (2025-01-17), FDA QMSR (2026-02-02), Android vitals (1.09 % / 0.47 %, cold start ≥ 5 s), EIP-170, S7-1500 150 ms default, NAMUR NE 43, EEMUA 191 / ISA-18.2 rates, ITU-T G.114, Cisco voice targets, Core Web Vitals, WCAG 2.2 target size, Apple 44 pt / Material 48 dp, Cortex-M3/M4 12 cycles, AMD junction grades, nginx / Express limits, FMVSS 111, OWASP LLM Top 10 2025, RFC 9457 / 9110, NIST AI 600-1, IEC 60204-1 stop categories, REP 103 / 105, PyTorch `weights_only`, Chainlink heartbeat, motion-to-photon 20 ms, Flesch 60.

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
