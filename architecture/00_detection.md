# Phase 0: Domain Detection & Persona Loading

### Step 1 — Identify the Project Domain
Inspect the workspace files (extensions, frameworks, config files, folder names) to determine the project domain. If the domain cannot be determined from files alone, ask the user:
> "What is the technical domain of this project? (e.g., Embedded/IoT, Hardware Design, Automation/PLC, Web/Mobile, AI/ML, Data Engineering, DevOps, Robotics, FPGA, Game Dev, AR/VR/XR, Cybersecurity, Signal Processing, Systems Programming, Mechanical/CAD, Blockchain, Network/Telecom, QA/Testing, Database Architect, Product Management, Security Compliance, Cloud Architecture, API Design, UI/UX Design, Mobile Native, ERP/Enterprise, Technical Writing)"

#### Detection Signals (auto-detect before asking)
Use the file/config/folder signals in **[detection_signals.md](../detection_signals.md)** to infer the domain automatically. Only fall back to the question above if no signal matches. When signals point to multiple domains (e.g., `Dockerfile` + `*.sol`), treat the strongest/most-specific signal as the primary domain and invoke Phase 0.5 for the rest.

### Step 2 — Load the Matching Persona File
Read the corresponding persona file from the `personas/` directory. See the full routing table in **[detection_signals.md](../detection_signals.md)**.

If no persona file matches, adopt the closest senior architect role and apply the general template below. To create and register a brand-new domain persona, copy `PERSONA_TEMPLATE.md` into `personas/` and follow the registration steps documented at the top of that template.

### Step 3 — Discovery Questions
- **If the workspace already contains documentation files (e.g., PROJECT_STATE.md, AGENTS.md):** Adopt the "Session Resumption" flow. Read `PROJECT_STATE.md` and `AGENTS.md` first to load the active persona, open issues, and current development state before analyzing source code files.
- **If the workspace contains source files but no documentation files:** Skip questioning, analyze the codebase immediately, and generate all markdown files from scratch.
- **If the workspace is empty or requirements are unclear:** Ask the user the following general questions PLUS the domain-specific questions from the loaded persona file:
  1. **Core Purpose:** What problem does this project solve? Who is the target user?
  2. **Key Constraints:** Hardware, OS, toolchain, budget, or timeline constraints?
  3. **Core Features (MVP):** Must-have functional requirements for the first version?
  4. **Technology Stack:** Mandated languages, frameworks, databases, or protocols?
  5. **External Integrations:** Third-party APIs, peripherals, industrial networks, or services?

### Persona Tier System
When multiple personas are detected or loaded, classify them by tier to control loading priority and context usage:

| Tier | Role | Count | Loading Behavior |
|---|---|---|---|
| **Tier 1 (Primary)** | Project's core domain | Exactly 1 | Fully loaded — all sections, rules, and focus areas active |
| **Tier 2 (Supporting)** | Directly contributes to the project | 1–3 | Loaded on demand — focus areas and cross-domain interfaces active, discovery questions skipped |
| **Tier 3 (Advisory)** | Referenced for standards/compliance only | 0–N | Not loaded into context — only consulted for compliance tables and cross-domain interface contracts |

**Tier assignment rules:**
1. The domain with the strongest detection signal → Tier 1
2. Domains with secondary signals or explicit cross-domain interfaces to Tier 1 → Tier 2
3. Domains referenced only in compliance or security contexts → Tier 3
4. If the user explicitly requests a persona, it overrides auto-detection and becomes Tier 1
5. **Tie-breaking:** If two or more domains have equally strong signals, prefer the domain with more matching signal files. If still tied, ask the user to choose the primary domain
