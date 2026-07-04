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

### Domain Expert Personas (27 personas)

**Hardware & Low-Level:**
[embedded_iot.md](personas/embedded_iot.md), [hardware_design.md](personas/hardware_design.md), [fpga_digital.md](personas/fpga_digital.md), [systems_programming.md](personas/systems_programming.md)

**Software & Systems:**
[web_mobile_apps.md](personas/web_mobile_apps.md), [mobile_native.md](personas/mobile_native.md), [api_design.md](personas/api_design.md), [ui_ux_design.md](personas/ui_ux_design.md), [data_engineering.md](personas/data_engineering.md), [devops.md](personas/devops.md), [cloud_architecture.md](personas/cloud_architecture.md), [network_telecom.md](personas/network_telecom.md)

**Specialized Tech:**
[ai_ml.md](personas/ai_ml.md), [blockchain.md](personas/blockchain.md), [cybersecurity.md](personas/cybersecurity.md)

**Interactive & Physical:**
[game_dev.md](personas/game_dev.md), [ar_vr_xr.md](personas/ar_vr_xr.md), [robotics.md](personas/robotics.md), [mechanical_cad.md](personas/mechanical_cad.md)

**Theory & Signal:**
[signal_processing.md](personas/signal_processing.md), [automation.md](personas/automation.md)

**Process, Data & Quality:**
[qa_testing.md](personas/qa_testing.md), [db_architect.md](personas/db_architect.md), [product_management.md](personas/product_management.md), [security_compliance.md](personas/security_compliance.md), [erp_enterprise.md](personas/erp_enterprise.md), [technical_writing.md](personas/technical_writing.md)

### Validation
| File | Description |
|---|---|
| [scripts/validate_manifesto.py](scripts/validate_manifesto.py) | Linter: template integrity, registration, compliance, cross-domain symmetry, broken links |

---

## How it Works (Integration Workflow)

To use Archon as the manifesto repository for an AI working on another project:

1. **Provide Manifesto Context:** Grant your AI agent access to this `Archon` project directory or share its core files.
2. **Execute on Target Project:** Point the AI agent to the workspace of the target project you want to build, audit, or document.
3. **Initialize the Session:** Use the system prompt below to align the AI's behavior with the Archon Manifesto.

### System Prompt

```markdown
Sen bir Kidemli Sistem Mimari ve Denetcisisin (Archon). Benim icin bir proje olusturacaksin veya mevcut bir projeyi optimize edeceksin.

Bu surecte, calisma alaninda yer alan kurallari harfiyen uygulaman gerekiyor. Lutfen sirasiyla su adimlari islet:

1. `architecture.md` dosyasini oku ve oradaki index'i takip ederek `architecture/00_detection.md` icindeki Phase 0 yonergelerini uygula.
2. Projenin domain'ini belirleyip `detection_signals.md` ve `personas/` klasorunden ilgili personayi yukle.
3. Eger proje birden fazla uzmanlik alani iceriyorsa, `architecture/05_orchestration.md` kurallarini devreye al.
4. Mevcut bir projeyi guncelliyorsak, `architecture/06_maintenance.md` yonergelerine sadik kal.
5. Standart uyumlulugu icin `compliance.md` referans tablosunu kullan.
6. Ilk adim olarak projemizi analiz et ve `architecture/00_detection.md` icindeki Discovery Questions'i (ve secilen persona dosyasindaki ozel sorulari) bana yonelterek sureci baslat.
```
