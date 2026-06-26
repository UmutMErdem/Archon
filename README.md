# 👑 Archon: The AI Manifesto Project

> **Archon** is a centralized governance, architectural framework, and behavioral manifesto repository. It is designed to define, guide, and instruct AI agents (like senior architects, domain specialists, and auditors) as they develop, refactor, and document target projects (such as embedded controllers, magnetic levitation systems, robotic software, and web applications).

Instead of embedding rules and personas directly inside target codebases, Archon acts as a **Manifesto Project**—a single source of truth for AI behavior, coding standards, compliance matrices, and documentation rules.

---

## 🎯 Manifesto Core Pillars

1. **AI Alignment & Persona Governance:** Define exact technical personas (e.g., Embedded Systems, Systems Programming, DevOps) with precise boundaries, verification checklists, and toolchains.
2. **Standardized Documentation Architectures:** Enforce strict blueprints for critical target files such as `ARCHITECTURE.md`, `AGENTS.md`, `KNOWN_ISSUES.md`, and `PROJECT_STATE.md`.
3. **Multi-Persona Collaboration:** Orchestrate complex projects spanning multiple domains (e.g., hardware layout + real-time firmware + cloud telemetry) using lead/specialist roles and safety-first conflict resolution rules.
4. **Maintenance & Incremental Sync:** Instruct the AI to preserve manual annotations and make targeted code/documentation edits rather than destructive full-file rewrites.
5. **Quality & Link Validation:** Ensure that every file path, function, symbol, and API route referenced by the AI actually exists in the target codebase (Zero Dead Links policy).

---

## 📁 Repository Structure

* 📜 **[architecture.md](architecture.md) (The Core Engine):** Defines the execution phases (detection, audit, generation, maintenance), output file templates, scope controls, and quality gate rules for the AI.
* 🛡️ **[compliance.md](compliance.md) (Compliance Registry):** A cross-domain matrix containing relevant regulatory standards (GDPR, ISO 27001, FCC Part 15, OpenXR, MISRA, etc.) for AI audit reference.
* 👥 **[personas/](personas/) (Domain Expert Personas):** Directory containing 17 technical persona files. Each file outlines role descriptions, discovery questions, recommended toolchains, test patterns, and cross-domain interfaces:
  * ⚙️ **Hardware & Low-Level:** [embedded_iot.md](personas/embedded_iot.md), [hardware_design.md](personas/hardware_design.md), [fpga_digital.md](personas/fpga_digital.md), [systems_programming.md](personas/systems_programming.md)
  * 🌐 **Software & Systems:** [web_mobile_apps.md](personas/web_mobile_apps.md), [data_engineering.md](personas/data_engineering.md), [devops.md](personas/devops.md), [network_telecom.md](personas/network_telecom.md)
  * 🧠 **Specialized Tech:** [ai_ml.md](personas/ai_ml.md), [blockchain.md](personas/blockchain.md), [cybersecurity.md](personas/cybersecurity.md)
  * 🎮 **Interactive & Physical:** [game_dev.md](personas/game_dev.md), [ar_vr_xr.md](personas/ar_vr_xr.md), [robotics.md](personas/robotics.md), [mechanical_cad.md](personas/mechanical_cad.md)
  * 📊 **Theory & Signal:** [signal_processing.md](personas/signal_processing.md), [automation.md](personas/automation.md)
* 📄 **[PERSONA_TEMPLATE.md](PERSONA_TEMPLATE.md) (Authoring Template):** A standard blueprint for adding new domain personas, ensuring they conform to the Archon structural rules.

---

## 🚀 How it Works (Integration Workflow)

To use Archon as the manifesto repository for an AI working on another project (e.g., your target software or hardware project):

1. **Provide Manifesto Context:** Grant your AI agent access to this `Archon` project directory or share its core files ([architecture.md](architecture.md), [compliance.md](compliance.md), and relevant files from [personas/](personas/)).
2. **Execute on Target Project:** Point the AI agent to the workspace of the target project you want to build, audit, or document.
3. **Initialize the Session:** Use the system prompt below to align the AI's behavior with the Archon Manifesto.

### 📋 System Prompt (Başlangıç Komutu)

Hedef projeniz üzerinde çalışmaya başlamadan önce, AI agent'a aşağıdaki komutu göndererek Archon kurallarını yükleyin:

```markdown
Sen bir Kıdemli Sistem Mimarı ve Denetçisisin (Archon). Benim için bir proje oluşturacaksın veya mevcut bir projeyi optimize edeceksin. 

Bu süreçte, çalışma alanında yer alan kuralları harfiyen uygulaman gerekiyor. Lütfen sırasıyla şu adımları işlet:

1. `architecture.md` dosyasını oku ve oradaki **Phase 0: Domain Detection & Persona Loading** yönergelerini uygulayarak projenin domain'ini belirleyip `personas/` klasöründen ilgili personayı yükle.
2. Eğer proje birden fazla uzmanlık alanı içeriyorsa, aynı dosyadaki **Phase 0.5: Multi-Persona Orchestration & Collaboration** kurallarını devreye al.
3. Mevcut bir projeyi güncelliyorsak, **Phase 0.6: Maintenance & Incremental Updates** ve büyük projeler için **Phase 0.7: Scope & Depth Control** yönergelerine sadık kal.
4. Mimaride ve güvenlik dokümanlarında standart uyumluluğu sağlamak için `compliance.md` referans tablosunu kullan.
5. İlk adım olarak projemizi analiz et ve `architecture.md` içerisindeki **Step 3 — Discovery Questions** başlığı altındaki soruları (ve seçilen persona dosyasındaki özel soruları) bana yönelterek süreci başlat.
```
