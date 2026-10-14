# Detection Signals Reference

> Auto-detection heuristics for domain identification. Used by Phase 0 (Step 1) in [architecture.md](architecture.md).
> When signals point to multiple domains, treat the strongest/most-specific signal as the primary domain and invoke Phase 0.5 for the rest.
> **Weak signals** are common outside their domain. They only add weight to a domain that already has a strong signal and never select Tier 1 on their own (see [00_detection.md](architecture/00_detection.md) Tier assignment rules).
> A named file (e.g. `openapi.yaml`) always outranks a bare extension glob (e.g. `*.yaml`).
> **Interface Label** is the canonical name other personas must use in `- **→ <Label>:**` cross-domain bullets.

| Signal Indicators (extensions / config files / folders) | Domain | Persona File | Interface Label | Weak Signals |
|---|---|---|---|---|
| `platformio.ini`, `*.ino`, `sdkconfig`, `Kconfig`, HAL/CMSIS headers | Embedded Systems / IoT | `personas/embedded_iot.md` | Embedded/IoT | `*.hex` / `*.bin` |
| `*.kicad_pcb`, `*.sch`, `*.brd`, `*.SchDoc`, Gerber `*.gbr` | Hardware Design (PCB / Schematics) | `personas/hardware_design.md` | Hardware Design | BOM `*.csv` |
| `*.st` (Structured Text), `*.scl`, `*.L5X`, `*.acd`, TIA Portal / Codesys projects | Industrial Automation (PLC / SCADA) | `personas/automation.md` | Automation | — |
| `package.json`, `*.tsx` / `*.jsx`, `pubspec.yaml`, `build.gradle` | Web / Mobile / Desktop Applications | `personas/web_mobile_apps.md` | Web/Mobile Apps | `index.html` |
| `*.ipynb`, `*.pth` / `*.onnx` / `*.h5` / `*.safetensors` | Data Science / AI / ML | `personas/ai_ml.md` | AI/ML | `requirements.txt` / `pyproject.toml` listing torch / tensorflow / jax |
| `dbt_project.yml`, Airflow `dags/`, `*.parquet`, Spark jobs | Data Engineering / ETL / Pipelines | `personas/data_engineering.md` | Data Engineering | warehouse `*.sql` |
| `Dockerfile`, `*.tf`, `.github/workflows/`, `helm/`, `ansible/` | DevOps / Cloud / IaC | `personas/devops.md` | DevOps | k8s `*.yaml` |
| `package.xml` (ROS), `*.urdf`, `*.launch`, `*.sdf`, catkin `CMakeLists.txt` | Robotics & Mechatronics | `personas/robotics.md` | Robotics | — |
| `*.v`, `*.sv`, `*.vhd`, `*.xdc`, `*.qsf`, `*.bit`, Vivado / Quartus projects | FPGA & Digital Design | `personas/fpga_digital.md` | FPGA | — |
| `*.unity`, `*.uasset`, `*.tscn` / `*.gd` (Godot), `Assets/`, `ProjectSettings/` | Game Development | `personas/game_dev.md` | Game Dev | — |
| OpenXR / visionOS SDK, XR Interaction Toolkit, Meta XR SDK, WebXR (`three.js`/A-Frame) | AR / VR / XR (Extended Reality) | `personas/ar_vr_xr.md` | AR/VR/XR | — |
| `*.nse`, `*.pcap`, exploit/pentest scripts, Metasploit/Nmap configs, CTF folders | Cybersecurity & Penetration Testing | `personas/cybersecurity.md` | Cybersecurity | — |
| `*.slx` (Simulink), `*.mlx` (MATLAB Live), `*.grc` (GNU Radio), FFT/filter DSP code | Signal Processing / DSP | `personas/signal_processing.md` | Signal Processing | `*.m` (MATLAB, also Objective-C) |
| `Cargo.toml`, `*.rs` / `*.zig`, kernel module `*.ko`, `*.S` | Systems Programming / OS / Drivers | `personas/systems_programming.md` | Systems Programming | `Makefile` + `*.c` / `*.cpp` |
| `*.step` / `*.stp`, `*.iges`, `*.sldprt`, `*.f3d`, `*.dwg`, `*.stl` | Mechanical Engineering / CAD | `personas/mechanical_cad.md` | Mechanical/CAD | — |
| `*.sol`, `hardhat.config.js`, `foundry.toml`, `truffle-config.js`, `*.vy` (Vyper) | Blockchain & Smart Contracts | `personas/blockchain.md` | Blockchain | — |
| Cisco/Juniper `*.cfg`, `*.frr`, `netmiko`/`napalm` scripts, GNS3 / `*.pkt` topologies | Network Engineering / Telecom | `personas/network_telecom.md` | Network/Telecom | — |
| `playwright.config.*`, `cypress.config.*`, `jest.config.*`, `vitest.config.*` | QA / Test Automation | `personas/qa_testing.md` | QA/Testing | — |
| `schema.sql`, `*.prisma`, `alembic.ini`, `liquibase.properties`, `flyway.conf` | Database Architect / DBA | `personas/db_architect.md` | Database Architect | — |
| `*PRD*.md`, `user_stories.md`, `*.feature` | Product Management / Business Analysis | `personas/product_management.md` | Product Management | — |
| `snyk.yml`, `.snyk`, `trivy.yaml`, `checkov.yaml`, `.github/workflows/*security*` | Security Compliance / DevSecOps | `personas/security_compliance.md` | Security Compliance | — |
| AWS CDK `cdk.json`, `*.bicep`, `serverless.yml`, Well-Architected templates, multi-region Terraform | Cloud Architecture | `personas/cloud_architecture.md` | Cloud Architecture | — |
| `openapi.yaml`, `*.proto`, `swagger.json`, GraphQL `*.graphql` / `schema.gql`, API gateway configs | API Design & Integration | `personas/api_design.md` | API Design | — |
| Design tokens `tokens.json` / `*.tokens.json`, Storybook `*.stories.*`, `*.figma`, Tailwind `tailwind.config.*` | UI/UX Design Engineering | `personas/ui_ux_design.md` | UI/UX Design | CSS-in-JS themes |
| `*.xcodeproj`, `*.xcworkspace`, `Podfile`, `*.swift`, `*.kt` + `AndroidManifest.xml` | Mobile Native Development | `personas/mobile_native.md` | Mobile Native | `*.gradle.kts` |
| SAP `*.abap`, `*.rdl` (SSRS), Dynamics `*.al`, Oracle Forms `*.fmb` | ERP & Enterprise Systems | `personas/erp_enterprise.md` | ERP/Enterprise | ERP config `*.xml` |
| `mkdocs.yml`, `docusaurus.config.js`, Sphinx `conf.py`, `*.rst` | Technical Writing & Documentation | `personas/technical_writing.md` | Technical Writing | `docs/`, API doc templates |
