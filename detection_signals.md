# Detection Signals Reference

> Auto-detection heuristics for domain identification. Used by Phase 0 (Step 1) in [architecture.md](architecture.md).
> When signals point to multiple domains, treat the strongest/most-specific signal as the primary domain and invoke Phase 0.5 for the rest.

| Signal Indicators (extensions / config files / folders) | Domain | Persona File | Complexity Completeness |
|---|---|---|---|
| `platformio.ini`, `*.ino`, `sdkconfig`, `Kconfig`, HAL/CMSIS headers, `*.hex` / `*.bin` | Embedded Systems / IoT | `personas/embedded_iot.md` | 28 (Thorough) |
| `*.kicad_pcb`, `*.sch`, `*.brd`, `*.SchDoc`, Gerber `*.gbr`, BOM `*.csv` | Hardware Design (PCB / Schematics) | `personas/hardware_design.md` | 24 (Moderate) |
| `*.st` (Structured Text), `*.scl`, `*.L5X`, `*.acd`, TIA Portal / Codesys projects | Industrial Automation (PLC / SCADA) | `personas/automation.md` | 24 (Moderate) |
| `package.json`, `*.tsx` / `*.jsx`, `pubspec.yaml`, `*.swift`, `build.gradle`, `index.html` | Web / Mobile / Desktop Applications | `personas/web_mobile_apps.md` | 38 (Comprehensive) |
| `*.ipynb`, `requirements.txt` w/ torch/tensorflow, `*.pth` / `*.onnx` / `*.h5` | Data Science / AI / ML | `personas/ai_ml.md` | 23 (Moderate) |
| `dbt_project.yml`, Airflow `dags/`, `*.parquet`, Spark jobs, warehouse `*.sql` | Data Engineering / ETL / Pipelines | `personas/data_engineering.md` | 26 (Moderate) |
| `Dockerfile`, `*.tf`, k8s `*.yaml`, `.github/workflows/`, `helm/`, `ansible/` | DevOps / Cloud / IaC | `personas/devops.md` | 36 (Comprehensive) |
| `package.xml` (ROS), `*.urdf`, `*.launch`, `*.sdf`, catkin `CMakeLists.txt` | Robotics & Mechatronics | `personas/robotics.md` | 22 (Sparse) |
| `*.v`, `*.sv`, `*.vhd`, `*.xdc`, `*.qsf`, `*.bit`, Vivado / Quartus projects | FPGA & Digital Design | `personas/fpga_digital.md` | 22 (Sparse) |
| `*.unity`, `*.uasset`, `*.tscn` / `*.gd` (Godot), `Assets/`, `ProjectSettings/` | Game Development | `personas/game_dev.md` | 22 (Sparse) |
| OpenXR / visionOS SDK, XR Interaction Toolkit, Meta XR SDK, WebXR (`three.js`/A-Frame) | AR / VR / XR (Extended Reality) | `personas/ar_vr_xr.md` | 21 (Sparse) |
| `*.nse`, `*.pcap`, exploit/pentest scripts, Metasploit/Nmap configs, CTF folders | Cybersecurity & Penetration Testing | `personas/cybersecurity.md` | 34 (Comprehensive) |
| `*.m` (MATLAB), `*.slx` (Simulink), `*.grc` (GNU Radio), FFT/filter DSP code | Signal Processing / DSP | `personas/signal_processing.md` | 23 (Moderate) |
| `Cargo.toml`, `*.rs` / `*.zig`, kernel module `*.ko`, `Makefile` + `*.c`/`*.cpp`, `*.S` | Systems Programming / OS / Drivers | `personas/systems_programming.md` | 22 (Sparse) |
| `*.step` / `*.stp`, `*.iges`, `*.sldprt`, `*.f3d`, `*.dwg`, `*.stl` | Mechanical Engineering / CAD | `personas/mechanical_cad.md` | 23 (Moderate) |
| `*.sol`, `hardhat.config.js`, `foundry.toml`, `truffle-config.js`, `*.vy` (Vyper) | Blockchain & Smart Contracts | `personas/blockchain.md` | 21 (Sparse) |
| Cisco/Juniper `*.cfg`, `*.frr`, `netmiko`/`napalm` scripts, GNS3 / `*.pkt` topologies | Network Engineering / Telecom | `personas/network_telecom.md` | 24 (Moderate) |
| `playwright.config.*`, `cypress.config.*`, `jest.config.*`, `vitest.config.*` | QA / Test Automation | `personas/qa_testing.md` | 26 (Moderate) |
| `schema.sql`, `*.prisma`, `alembic.ini`, `liquibase.properties`, `flyway.conf` | Database Architect / DBA | `personas/db_architect.md` | 27 (Thorough) |
| `*requirements*.txt` (no ML), `*PRD*.md`, `user_stories.md`, `*.feature` | Product Management / Business Analysis | `personas/product_management.md` | 23 (Moderate) |
| `snyk.yml`, `.snyk`, `trivy.yaml`, `checkov.yaml`, `.github/workflows/*security*` | Security Compliance / DevSecOps | `personas/security_compliance.md` | 26 (Moderate) |
| AWS CDK `cdk.json`, `*.bicep`, `serverless.yml`, Well-Architected templates, multi-region Terraform | Cloud Architecture | `personas/cloud_architecture.md` | 21 (Sparse) |
| `openapi.yaml`, `*.proto`, `swagger.json`, GraphQL `*.graphql` / `schema.gql`, API gateway configs | API Design & Integration | `personas/api_design.md` | 24 (Moderate) |
| Design tokens `*.json`, Storybook `*.stories.*`, `*.figma`, Tailwind `tailwind.config.*`, CSS-in-JS themes | UI/UX Design Engineering | `personas/ui_ux_design.md` | 21 (Sparse) |
| `*.xcodeproj`, `*.xcworkspace`, `Podfile`, `*.kt` + `AndroidManifest.xml`, `*.gradle.kts` (mobile) | Mobile Native Development | `personas/mobile_native.md` | 22 (Sparse) |
| SAP `*.abap`, `*.rdl` (SSRS), Dynamics `*.al`, Oracle Forms `*.fmb`, ERP config `*.xml` | ERP & Enterprise Systems | `personas/erp_enterprise.md` | 23 (Moderate) |
| `docs/`, `mkdocs.yml`, `docusaurus.config.js`, Sphinx `conf.py`, `*.rst`, API doc templates | Technical Writing & Documentation | `personas/technical_writing.md` | 21 (Sparse) |
