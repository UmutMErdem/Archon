# Archon: The AI Manifesto Project

> **Archon** is a centralized governance, architectural framework, and behavioral manifesto repository. It is designed to define, guide, and instruct AI agents (like senior architects, domain specialists, and auditors) as they develop, refactor, and document target projects (such as embedded controllers, magnetic levitation systems, robotic software, and web applications).

Instead of embedding rules and personas directly inside target codebases, Archon acts as a **Manifesto Project** — a single source of truth for AI behavior, coding standards, compliance matrices, and documentation rules.

---

## Manifesto Core Pillars

1. **AI Alignment & Persona Governance:** Define exact technical personas with precise boundaries, verification checklists, and toolchains.
2. **Standardized Documentation Architectures:** Enforce strict blueprints for critical target files such as `ARCHITECTURE.md`, `AGENTS.md`, `KNOWN_ISSUES.md`, and `PROJECT_STATE.md`.
3. **Multi-Persona Collaboration:** Orchestrate complex projects spanning multiple domains using lead/specialist roles, tier-based loading, and safety-first conflict resolution rules.
4. **Maintenance & Incremental Sync:** Instruct the AI to preserve manual annotations and make targeted code/documentation edits rather than destructive full-file rewrites.
5. **Quality & Link Validation:** Ensure that every file path, function, symbol, and API route referenced by the AI actually exists in the target codebase (Zero Dead Links policy).

---

## Repository Structure

### Core Engine
| File | Description |
|---|---|
| [architecture.md](architecture.md) | Index for all execution phases and output specifications |
| [architecture/00_detection.md](architecture/00_detection.md) | Phase 0: Domain detection, persona loading, tier system |
| [architecture/05_orchestration.md](architecture/05_orchestration.md) | Phase 0.5: Multi-persona orchestration and conflict resolution |
| [architecture/06_maintenance.md](architecture/06_maintenance.md) | Phase 0.6-0.7: Incremental updates and scope control |
| [architecture/files_spec.md](architecture/files_spec.md) | Output file specifications (AGENTS.md, ARCHITECTURE.md, etc.) |
| [architecture/rules.md](architecture/rules.md) | Quality gates, validation rules, and behavioral constraints |

### Reference Files
| File | Description |
|---|---|
| [detection_signals.md](detection_signals.md) | Auto-detection heuristics for domain identification |
| [compliance.md](compliance.md) | Cross-domain regulatory standards reference |
| [CROSS_DOMAIN_MATRIX.md](CROSS_DOMAIN_MATRIX.md) | Persona cross-domain interface relationships |
| [PERSONA_TEMPLATE.md](PERSONA_TEMPLATE.md) | Blueprint for creating new domain personas |

### Domain Expert Personas (30 personas)

**Hardware & Low-Level:**
[embedded_iot.md](personas/embedded_iot.md), [hardware_design.md](personas/hardware_design.md), [fpga_digital.md](personas/fpga_digital.md), [systems_programming.md](personas/systems_programming.md)

**Software & Systems:**
[web_mobile_apps.md](personas/web_mobile_apps.md), [mobile_native.md](personas/mobile_native.md), [api_design.md](personas/api_design.md), [ui_ux_design.md](personas/ui_ux_design.md), [data_engineering.md](personas/data_engineering.md), [devops.md](personas/devops.md), [cloud_architecture.md](personas/cloud_architecture.md), [network_telecom.md](personas/network_telecom.md)

**Specialized Tech:**
[ai_ml.md](personas/ai_ml.md), [llm_applications.md](personas/llm_applications.md), [blockchain.md](personas/blockchain.md), [cybersecurity.md](personas/cybersecurity.md)

**Interactive & Physical:**
[game_dev.md](personas/game_dev.md), [ar_vr_xr.md](personas/ar_vr_xr.md), [robotics.md](personas/robotics.md), [mechanical_cad.md](personas/mechanical_cad.md)

**Theory & Signal:**
[signal_processing.md](personas/signal_processing.md), [automation.md](personas/automation.md)

**Regulated Industries:**
[automotive.md](personas/automotive.md), [medical_device.md](personas/medical_device.md)

**Process, Data & Quality:**
[qa_testing.md](personas/qa_testing.md), [db_architect.md](personas/db_architect.md), [product_management.md](personas/product_management.md), [security_compliance.md](personas/security_compliance.md), [erp_enterprise.md](personas/erp_enterprise.md), [technical_writing.md](personas/technical_writing.md)

### Helper Utilities & Validation
| File / Folder | Description |
|---|---|
| [scripts/validate_manifesto.py](scripts/validate_manifesto.py) | Linter: template integrity, inheritance, placeholders, compliance IDs, registry (signals / README / Phase 0 question), canonical and symmetric interfaces, signal overlaps, matrix freshness, and links with anchors. Any error exits 1 |
| [scripts/sync_matrix.py](scripts/sync_matrix.py) | Generator: the only writer of `CROSS_DOMAIN_MATRIX.md` (table + relationship diagram). `--check` exits 1 if the file is stale |
| [scripts/calculate_complexity.py](scripts/calculate_complexity.py) | Report: per-persona completeness score (sections + interfaces + compliance bullets). `--min-score N` turns it into a gate |
| [scripts/detect_domain.py](scripts/detect_domain.py) | Detector: scores a target workspace against `detection_signals.md` and proposes Tier 1 / Tier 2 personas |
| [scripts/bootstrap_target.py](scripts/bootstrap_target.py) | Scaffolder: creates the 12 documentation skeletons from `architecture/files_spec.md` in a target project. Never overwrites existing files unless `--force` |
| [scripts/create_persona.py](scripts/create_persona.py) | Generator: creates a persona draft from `PERSONA_TEMPLATE.md` and registers it in `detection_signals.md`, `README.md`, and `architecture/00_detection.md` |
| [scripts/graphify_helper.py](scripts/graphify_helper.py) | Graphify: builds, updates, and queries a codebase knowledge graph. Installs `graphifyy` only with `--install` / `--install-only` |
| [scripts/archon_core.py](scripts/archon_core.py) | Shared parsing, canonical persona labels, and paths used by every script |
| [scripts/tests/](scripts/tests/) | Unit tests (`pytest`) |

---

## How it Works (Integration Workflow)

To integrate Archon into your development workflow, choose one of the two paths below depending on your project:

> [!TIP]
> **Static Scaffolding (Path A)** is recommended for new or clean projects where you want a script to pre-generate all templates.
> **Dynamic Auto-Detection (Path B)** is recommended for existing codebases where you want the AI agent to analyze the project and build documentation on-the-fly.

Both paths end in the same Phase 0 flow. Which questions the AI asks is decided by Step 3 of [00_detection.md](architecture/00_detection.md#step-3--discovery-questions).

---

### Path A: Static Scaffolding (For New/Clean Projects)
This method pre-populates your target directory with the necessary documentation skeletons before the AI starts coding.

1. **Detect the domain (optional):**
   ```bash
   python scripts/detect_domain.py ../my-project
   ```
2. **Bootstrap the workspace:**
   ```bash
   python scripts/bootstrap_target.py --target ../my-project --primary embedded_iot.md --supporting hardware_design.md
   ```
   Run it without arguments for interactive mode. Add `--graphify` to set up Graphify (add `--install-graphify` if the `graphify` CLI is not installed yet). Existing files are skipped and listed; `--force` overwrites them.
3. **Commit the scaffolded files** (`AGENTS.md`, `ARCHITECTURE.md`, `PROJECT_STATE.md`, …). `PROJECT_STATE.md` starts with `Status: SCAFFOLDED`, which tells the AI to run a full analysis instead of treating the skeletons as existing documentation.
4. **Initialize the AI session** with the System Prompt below.

---

### Path B: Dynamic Auto-Detection (For Existing Projects)
This method allows the AI agent to analyze your existing codebase, auto-detect the tech stack, and build documentation dynamically.

1. **Provide Context:** Grant your AI agent access to both your target project workspace and this `Archon` manifesto directory.
2. **Initialize AI Session:** Paste the **System Prompt** below as the initial instruction in your AI editor.
3. **Discovery & Graphify Setup:** The AI scans the project using `detection_signals.md`, selects the persona(s), analyzes the code, and asks only the discovery questions the code cannot answer. It also asks whether to set up **Graphify**.

---

### System Prompt

English:

```markdown
You are a Senior Systems Architect and Auditor (Archon). You will either create a new project for me or optimize an existing one.

Follow the rules in this workspace exactly. Run these steps in order:

1. Read `architecture.md` and follow its index; apply the Phase 0 instructions in `architecture/00_detection.md`.
2. Determine the project's domain and load the matching persona from `detection_signals.md` and the `personas/` folder.
3. If the project spans several domains, apply `architecture/05_orchestration.md`.
4. If we are updating an existing project, follow `architecture/06_maintenance.md`.
5. Use the `compliance.md` reference tables for standards compliance.
6. Start by analyzing the project, then ask me the Discovery Questions selected by Step 3 of `architecture/00_detection.md` (plus the persona-specific ones).
```

Türkçe:

```markdown
Sen bir Kıdemli Sistem Mimarı ve Denetçisisin (Archon). Benim için bir proje oluşturacaksın veya mevcut bir projeyi optimize edeceksin.

Bu süreçte, çalışma alanında yer alan kuralları harfiyen uygulaman gerekiyor. Lütfen sırasıyla şu adımları işlet:

1. `architecture.md` dosyasını oku ve oradaki index'i takip ederek `architecture/00_detection.md` içindeki Phase 0 yönergelerini uygula.
2. Projenin domain'ini belirleyip `detection_signals.md` ve `personas/` klasöründen ilgili personayı yükle.
3. Eğer proje birden fazla uzmanlık alanı içeriyorsa, `architecture/05_orchestration.md` kurallarını devreye al.
4. Mevcut bir projeyi güncelliyorsak, `architecture/06_maintenance.md` yönergelerine sadık kal.
5. Standart uyumluluğu için `compliance.md` referans tablosunu kullan.
6. İlk adım olarak projemizi analiz et, ardından `architecture/00_detection.md` Step 3'ün seçtiği Discovery Questions'ı (ve seçilen persona dosyasındaki özel soruları) bana yönelt.
```

---

## Development

```bash
pip install -r requirements-dev.txt
pytest
ruff check scripts
black --check scripts
python scripts/sync_matrix.py --check
python scripts/validate_manifesto.py
```

CI ([.github/workflows/ci.yml](.github/workflows/ci.yml)) runs the same commands on Python 3.10 and 3.14. After editing a persona's `## Cross-Domain Interfaces`, run `python scripts/sync_matrix.py` and commit the regenerated matrix.

Graphify is optional (`pip install -r requirements-graphify.txt`). `.graphifyignore` excludes all Markdown, so the Archon graph covers `scripts/` only; `graphify-out/` is git-ignored and must be rebuilt locally with `python scripts/graphify_helper.py --update`.

Project planning documents (known issues, decisions, roadmap) live in [planning/](planning/PROJECT_STATE.md); release history is in [CHANGELOG.md](CHANGELOG.md).

## License

Apache License 2.0, see [LICENSE](LICENSE).
