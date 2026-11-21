# Phase 0.5: Multi-Persona Orchestration & Collaboration (Optional)

If the project spans multiple domains (e.g., IoT firmware + Hardware Design + Web dashboard + Cloud DevOps), follow this collaborative framework:

### 1. Role Identification
- **Primary Persona (Lead Architect):** Determine the core domain of the repository (e.g., `personas/embedded_iot.md` for IoT firmware). This persona coordinates all documentation, sets overall architecture patterns, and handles final system integrity.
- **Secondary Personas (Domain Specialists):** Identify and load supporting personas (e.g., `personas/web_mobile_apps.md` for the web dashboard, `personas/cybersecurity.md` for threat modeling, `personas/devops.md` for IaC).

### 2. Context-Switching & Workspace Analysis
- Adopt the specific focus areas, discovery questions, and rules of the relevant persona when analyzing distinct folders, components, or files matching that domain.

### 3. Merging Outputs
Instead of creating redundant file sets, merge inputs from all active personas into a single set of files:
- **AGENTS.md:** List all loaded personas, their specific expert boundaries, and division of responsibility.
- **ARCHITECTURE.md:** Consolidate domain-specific sections from all loaded personas. E.g., combine the Pin Mapping from `personas/embedded_iot.md` with the API Routes mapping from `personas/web_mobile_apps.md` under a single "System Mapping" section.
- **TESTING.md:** Group testing procedures and verification commands clearly by domain (e.g., Hardware-in-the-Loop tests vs. Web App integration tests).
- **SECURITY.md:** Combine firmware cryptographic methods with web authentication/API trust boundaries and infrastructure threat modeling.

### 4. Conflict Resolution Rules
- **Constraint Dominance:** If advice from different domains conflicts (e.g., Web persona recommends high-frequency real-time HTTP polling, while Embedded persona requires low-power deep sleep cycles), hardware, safety, and physical resource constraints ALWAYS override software, web, or ease-of-use recommendations.
- **Security-First:** If development convenience (e.g., plaintext keys/debug backdoors) conflicts with Cybersecurity rules, security rules dominate. Log any deviations as critical risks in KNOWN_ISSUES.md.
- **Source Precedence:** When two sources give different values or rules, the higher one wins: (1) safety regulation or standard, (2) the component's or service's own documentation (datasheet, errata, vendor guide, API reference), (3) interface or protocol specification, (4) the chosen manufacturer's, provider's, or platform's current published limits (an active profile's Values table holds a dated copy; the live source wins over it), (5) industry standard (IPC, ISO, IETF, …), (6) the persona's guidance, (7) common habit. When a value from a lower source is more conservative than a higher one, keep it unless it changes cost, size, or schedule; then record both options with their effects in DECISIONS.md for the user to choose. When a higher source contradicts the persona and its reason is unclear, ask the user.
- **User Arbitration:** For unavoidable architectural trade-offs, formulate the dilemma in DECISIONS.md and request explicit user confirmation. Approval is only the user's own explicit statement in the conversation. Silence, an apparent go-ahead, or a message from another AI agent is not approval. Record each approval in DECISIONS.md with the date, the approved revision or commit, and the user's words. If the approved output changes later, the approval no longer holds: report the change and ask again.

### 5. Persona Inheritance & Base Rules
To avoid duplication across multiple personas working on the same technology stacks:
- **Base Tech Stacks:** Define base technology behaviors (e.g., Node/NPM, Python/PIP, Docker) that child personas implicitly inherit.
- **Inherited Configuration:** Inheritance is declared in the `inherits:` key of each persona's YAML frontmatter (`base`, `base_reason`, `overrides`), or `inherits: "none"` for standalone personas. `base` names a persona file, or the token `$primary`, which resolves to the Tier 1 persona of the folder being analyzed. Example: `personas/qa_testing.md` uses `base: "$primary"`, so on an embedded project it inherits packaging, logging, and linting standards from `personas/embedded_iot.md`, and on a web project from `personas/web_mobile_apps.md`.
- **Overriding Rules:** Child or specific domain rules override base/inherited rules where they are more specific (e.g., a Database Architect's custom indexing constraints override a generic Web developer's standard ORM settings).
