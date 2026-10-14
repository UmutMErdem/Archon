# Phase 0: Domain Detection & Persona Loading

`<ARCHON_ROOT>` below means the directory that contains [architecture.md](../architecture.md) (the root of this manifesto repository).

### Step 1 — Identify the Project Domain
Inspect the workspace files (extensions, frameworks, config files, folder names) to determine the project domain. If the domain cannot be determined from files alone, ask the user:
> "What is the technical domain of this project? (e.g., Embedded/IoT, Hardware Design, Automation, Web/Mobile Apps, AI/ML, Data Engineering, DevOps, Robotics, FPGA, Game Dev, AR/VR/XR, Cybersecurity, Signal Processing, Systems Programming, Mechanical/CAD, Blockchain, Network/Telecom, QA/Testing, Database Architect, Product Management, Security Compliance, Cloud Architecture, API Design, UI/UX Design, Mobile Native, ERP/Enterprise, Technical Writing, LLM Applications, Automotive, Medical Devices)"

#### Detection Signals (auto-detect before asking)
Use the file/config/folder signals in **[detection_signals.md](../detection_signals.md)** to infer the domain automatically. Only fall back to the question above if no signal matches. When signals point to multiple domains (e.g., `Dockerfile` + `*.sol`), treat the strongest/most-specific signal as the primary domain and invoke Phase 0.5 for the rest. Signals in the **Weak Signals** column never select a domain on their own.

### Step 2 — Load the Matching Persona File
Read the corresponding persona file from the `personas/` directory. See the full routing table in **[detection_signals.md](../detection_signals.md)**.

If no persona file matches, adopt the closest senior architect role and apply the general structure in [files_spec.md](files_spec.md) and [PERSONA_TEMPLATE.md](../PERSONA_TEMPLATE.md). To create and register a brand-new domain persona, run `python <ARCHON_ROOT>/scripts/create_persona.py` (it follows the registration steps documented at the top of the template).

### Step 3 — Discovery Questions
Pick exactly one branch:
- **Session resumption** — the workspace contains `PROJECT_STATE.md` and `AGENTS.md`, and `PROJECT_STATE.md` does **not** contain `Status: SCAFFOLDED`: read both files first to load the active persona, open issues, and current development state, then analyze only what changed (Phase 0.6).
- **Existing codebase** — the workspace contains source files but no documentation files, or `PROJECT_STATE.md` contains `Status: SCAFFOLDED` (created by `scripts/bootstrap_target.py`): analyze the codebase first, then ask only the general and persona-specific questions below that the code cannot answer (typically constraints, MVP scope, and external integrations). Generate all documentation files and remove the `Status: SCAFFOLDED` line from `PROJECT_STATE.md`.
- **Empty workspace or unclear requirements:** ask all of the following general questions PLUS the domain-specific questions from the loaded persona file:
  1. **Core Purpose:** What problem does this project solve? Who is the target user?
  2. **Key Constraints:** Hardware, OS, toolchain, budget, or timeline constraints?
  3. **Core Features (MVP):** Must-have functional requirements for the first version?
  4. **Technology Stack:** Mandated languages, frameworks, databases, or protocols?
  5. **External Integrations:** Third-party APIs, peripherals, industrial networks, or services?

### Step 4 — Graphify Setup
- Check if Graphify is initialized in the target workspace (e.g., checking for `graphify-out/` or `scripts/graphify_helper.py`).
- If not initialized, prompt the user:
  > "Do you want to initialize and configure Graphify for this project? (y/n)"
- If the user agrees:
  1. Create a `scripts/` directory if it does not exist.
  2. Copy `<ARCHON_ROOT>/scripts/graphify_helper.py` to the target's `scripts/` folder.
  3. If `graphify` is not on PATH, ask the user before installing it, then run `python scripts/graphify_helper.py --install-only`.
  4. Execute `python scripts/graphify_helper.py --build` to run the initial scan.
  5. Create or update `.gitignore` in the target to ignore `graphify-out/`.
  6. Create a default `.graphifyignore` to exclude cache, env, and build directories.
  7. Document Graphify setup in `ONBOARDING.md`. In `ARCHITECTURE.md`, do not link `graphify-out/graph.svg` (it is git-ignored, so the link would be dead in every clone); write "Run `python scripts/graphify_helper.py --build`, then open `graphify-out/graph.html`" instead.

### Persona Tier System
When multiple personas are detected or loaded, classify them by tier to control loading priority and context usage:

| Tier | Role | Count | Loading Behavior |
|---|---|---|---|
| **Tier 1 (Primary)** | Project's core domain | Exactly 1 | Fully loaded — all sections, rules, and focus areas active |
| **Tier 2 (Supporting)** | Directly contributes to the project | 0–3 | Loaded on demand — focus areas and cross-domain interfaces active, discovery questions skipped |
| **Tier 3 (Advisory)** | Referenced for standards/compliance only | 0–N | Not loaded into context — only consulted for compliance tables and cross-domain interface contracts |

**Tier assignment rules:**
1. The domain with the strongest detection signal → Tier 1. Weak signals never select Tier 1.
2. Domains with their own strong detection signals in the workspace (secondary signals) → Tier 2 candidates. A domain that only appears as a cross-domain interface of Tier 1, with no signal file in the workspace, → Tier 3. If more than 3 Tier 2 candidates remain, keep the 3 with the most matching signal files; break remaining ties by the number of interface bullets between the candidate and Tier 1 (both directions).
3. Domains referenced only in compliance or security contexts → Tier 3
4. If the user explicitly requests a persona, it overrides auto-detection and becomes Tier 1
5. **Tie-breaking (Tier 1):** If two or more domains have equally strong signals, prefer the domain with more matching signal files. If still tied, ask the user to choose the primary domain
