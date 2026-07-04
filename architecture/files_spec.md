# Files to Create

The AI must generate ALL of the following markdown files. Domain-specific content and additional sections are defined in the loaded persona file.

### AGENTS.md
- Expert persona definition for this project (refreshed every session)
- Must-follow constraints: domain-specific boundaries, safety rules, timing, API/protocol contracts
- Architecture quick-reference: key components/services/hardware and relationships (table)
- Validation checklist: exact commands or procedures to verify correctness
- Repo conventions: naming, branching, commit rules

### DECISIONS.md
- Non-obvious design/architecture decisions already in the code
- Format: `D-NNN` (newest first) | Date | Decision | Rationale | Impact
- Focus on WHY — the WHAT is visible in the code

### KNOWN_ISSUES.md
- Every bug, misconfig, errata, or dangerous pattern found
- Format: `I-NNN` | Severity (critical/high/medium/low) | Status (OPEN/FIXED)
- Each entry: Symptom, Root cause (file:line or module), Fix/Workaround
- Security & safety issues → CRITICAL severity, logged immediately

### OPTIMIZATIONS.md
- Performance, memory, resource, cost, and dead code/component findings
- Format: `O-NN` | Category | Severity | Status
- Each entry: Evidence (file:line), Why suboptimal, Recommendation, Removal safety, Impact

### PROJECT_STATE.md
- **Version Snapshot:** Record the analysis timestamp, Git commit hash (if available), and branch name at the top of the file. Update this on every incremental sync.
- Version, platform, build/revision status table
- Architecture summary (3-5 bullets or component table)
- Links to all open `I-NNN` and `O-NN` items
- Link to CHANGELOG.md

### ROADMAP.md
- Open issues grouped into milestones by priority (P0/P1/P2)
- Format: `M-NNN` | Priority | Status | Goal | Task checklist

### TESTING.md
- Test strategy: frameworks, directory structure, runner commands
- Mocking, simulation, or hardware-in-the-loop (HIL) details
- Coverage targets and CI/CD pipeline configuration

### SECURITY.md
- Threat modeling: endpoints, buses, trust boundaries
- Encryption: data-at-rest and data-in-transit methods
- Dependency scanning and update processes

### DEPENDENCIES.md
- Third-party libraries, components, and external services inventory
- License compliance (MIT, Apache, GPL, proprietary)
- Deprecated/outdated items with upgrade recommendations

### ONBOARDING.md
- Step-by-step environment setup for new team members
- IDE/EDA settings, plugins, toolchains
- Formatting, linting, and design rule checks

### CHANGELOG.md
- Version/revision history
- Format: Keep a Changelog (Added, Changed, Deprecated, Removed, Fixed, Security)

### ARCHITECTURE.md  (most detailed file)
Produce ALL of the following generic sections, PLUS any domain-specific sections defined in the loaded persona file:

1. **Main Idea & Project Recap**
   - One-paragraph project description and key capabilities table

2. **System Mapping**
   - Domain-specific mapping (defined in persona file: pin maps, API routes, I/O lists, model layers, network topology, etc.)

3. **File, Folder & Resource Tree**
   - Full directory tree with one-line description per item

4. **Detailed Specifications**
   - Domain-specific details (defined in persona file: function signatures, component specs, hyperparameters, resource tables, etc.)

5. **Build, Deploy & Run**
   - All commands: build, upload/flash, deploy, clean, test, simulate
   - Expected outputs and prerequisites

6. **Critical Points of Failure**
   - Table: Item | Criticality (3-star scale) | Why critical / Failure mode

7. **Configuration & Parameters**
   - All config files annotated with purpose
   - Magic constants, feature flags, registers, or hyperparameters with values and effects

8. **Communication & Protocol Details**
   - Every protocol/interface with addresses, rates, formats, timing, and memory layouts

9. **Data Flow & State Machines**
    - Mermaid.js state diagrams for core logic/modes
    - Sequence/data flow diagrams for component interactions
    - **Diagram Standards:** Use the following Mermaid diagram types consistently:
      - `stateDiagram-v2` → State machines, mode transitions, lifecycle flows
      - `sequenceDiagram` → Data flow between components, request/response chains, protocol handshakes
      - `flowchart TD/LR` → Decision trees, build pipelines, boot sequences
      - `classDiagram` → Software module relationships, inheritance, interface contracts
      - `erDiagram` → Database schemas, data models, entity relationships
    - Label all nodes with descriptive names (not abbreviations). Use consistent color themes per domain when possible.

10. **Error Handling & Diagnostics**
    - Error-handling architecture and Error Code Dictionary
    - Logging channels and severity levels (DEBUG → CRITICAL)

11. **Performance Budget**
    - Domain-specific performance limits and resource budgets (defined in persona file)

12. **Compliance & Regulatory**
    - Applicable standards and certifications (see `compliance.md` for reference)

13. **Known Problems & TODO**
    - Summary table linking to KNOWN_ISSUES.md and ROADMAP.md with severity and status
