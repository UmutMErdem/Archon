# Compliance & Regulatory Standards Reference

This document serves as a cross-domain reference for compliance standards, certifications, and regulatory frameworks. The AI should check this table when populating the **Compliance & Regulatory** section of ARCHITECTURE.md and SECURITY.md.

> **Last Reviewed:** 2026-07-04 — Standards in rapidly evolving domains (e.g., EU AI Act, MiCA) should be re-verified periodically. Check official sources before citing version numbers.

---

## General / Cross-Domain

| Standard | Full Name | Scope | Applicability |
|---|---|---|---|
| GDPR | General Data Protection Regulation | Personal data privacy (EU) | Any system processing EU citizen data |
| KVKK | Kişisel Verilerin Korunması Kanunu | Personal data privacy (Turkey) | Any system processing Turkish citizen data |
| ISO 27001 | Information Security Management | Information security governance | All domains handling sensitive data |
| ISO 9001 | Quality Management Systems | Quality processes | Manufacturing, services, software |
| RoHS | Restriction of Hazardous Substances | Material restrictions | All physical/electronic products sold in EU |
| REACH | Registration, Evaluation of Chemicals | Chemical safety | Products containing chemicals (EU) |

---

## Embedded Systems / IoT

| Standard | Scope |
|---|---|
| CE Marking (RED, LVD, EMC) | EU market access for electronic devices |
| FCC Part 15 | Radio frequency emissions (USA) |
| UL / IEC 62368-1 | Audio/video and IT equipment safety |
| IEC 60730 | Automatic electrical controls (household) |
| ETSI EN 303 645 | IoT cybersecurity baseline (EU) |

## Hardware Design (PCB)

| Standard | Scope |
|---|---|
| IPC-2221 | Generic PCB design standard |
| IPC-7351 | Component land pattern standard |
| IPC-A-610 | Acceptability of electronic assemblies |
| UL 94 | Flammability of PCB materials |
| JEDEC | Component packaging and handling |

## Industrial Automation

| Standard | Scope |
|---|---|
| IEC 61131-3 | PLC programming languages |
| IEC 61508 | Functional safety (SIL levels) |
| IEC 62061 | Safety of machinery — functional safety |
| ISO 13849 | Safety of machinery — Performance Level |
| ISA-18.2 / IEC 62682 | Alarm management |
| IEC 62443 | Industrial network cybersecurity |
| ATEX / IECEx | Equipment in explosive atmospheres |

## Web / Mobile / Desktop Applications

| Standard | Scope |
|---|---|
| OWASP Top 10 | Web application security risks |
| OWASP ASVS | Application security verification |
| WCAG 2.1 (Level AA) | Web content accessibility |
| PCI-DSS | Payment card data security |
| SOC 2 Type II | Service organization controls |
| HIPAA | Health data protection (USA) |
| COPPA | Children's online privacy (USA) |

## AI / ML

| Standard | Scope |
|---|---|
| EU AI Act | Risk-based AI regulation (EU) |
| IEEE 7000 | Ethical AI design |
| Model Cards (Google) | Model transparency documentation |
| Datasheets for Datasets | Dataset documentation standard |
| NIST AI RMF | AI risk management framework |

## Data Engineering

| Standard | Scope |
|---|---|
| GDPR / CCPA | Data privacy, right to be forgotten, and masking |
| HIPAA | Health insurance portability and protected health info |
| SOC 2 Type II | Operational security, confidentiality, and data privacy |
| DAMA-DMBOK | Data management framework best practices |

## DevOps / Cloud

| Standard | Scope |
|---|---|
| SOC 2 Type II | Cloud service security/availability |
| CIS Benchmarks | Cloud/OS/container hardening |
| NIST 800-53 | Federal security controls |
| ISO 27017 | Cloud-specific security controls |
| CSA STAR | Cloud security certification |

## Robotics

| Standard | Scope |
|---|---|
| ISO 10218-1/2 | Industrial robot safety |
| ISO 15066 | Collaborative robot safety |
| CE Machinery Directive 2006/42/EC | Machine safety (EU) |
| ASTM F3218 | Small UAS (drone) standards |
| ROS REP Standards | ROS coordinate frames and conventions |

## FPGA & Digital Design

| Standard | Scope |
|---|---|
| IEEE 1076 | VHDL language standard |
| IEEE 1364 / 1800 | Verilog / SystemVerilog standards |
| DO-254 | FPGA in airborne systems |
| IEC 61508 | Safety-critical FPGA designs |

## Game Development

| Standard | Scope |
|---|---|
| ESRB / PEGI / USK | Age rating systems |
| Sony TRC / Microsoft XR / Nintendo Lotcheck | Platform certification |
| Apple App Store Guidelines | iOS distribution requirements |
| Google Play Policies | Android distribution requirements |

## AR / VR / XR (Extended Reality)

| Standard | Scope |
|---|---|
| OpenXR | Cross-platform portability standard for XR devices |
| WebXR Device API | Browser accessibility standard for XR hardware |
| W3C XAUR | Accessibility user requirements for XR applications |
| Oculus VRCs / VisionOS HIG | Platform-specific submission guidelines and standards |

## Cybersecurity

| Standard | Scope |
|---|---|
| NIST Cybersecurity Framework | Security risk management |
| MITRE ATT&CK | Threat intelligence framework |
| CIS Controls | Prioritized security actions |
| CVSS | Vulnerability severity scoring |

## Signal Processing / DSP

| Standard | Scope |
|---|---|
| IEEE 754 | Floating-point arithmetic |
| ITU-T / ITU-R | Audio/video codec standards |
| AES Standards | Professional audio engineering |
| IEC 61672 | Sound level measurement |

## Systems Programming

| Standard | Scope |
|---|---|
| POSIX | Portable Operating System Interface standards |
| ISO/IEC C & C++ | C and C++ Programming Language Standards (e.g. C11, C++20) |
| MISRA C / CERT C | Guidelines and standards for safety-critical and secure systems |
| AUTOSAR C++14 | Guidelines for the use of C++14 in critical systems |
| Linux Kernel Coding Style | Coding style guidelines for Linux kernel contributors |

## Mechanical Engineering / CAD

| Standard | Scope |
|---|---|
| ASME Y14.5 | GD&T (geometric tolerancing) |
| ISO 2768 | General linear/angular tolerances |
| ISO 1101 | Geometrical tolerancing |
| ISO 898 | Mechanical properties of fasteners |
| IP Ratings (IEC 60529) | Enclosure ingress protection |

## Blockchain

| Standard | Scope |
|---|---|
| EIP / ERC Standards | Ethereum token and protocol standards |
| OpenZeppelin Standards | Smart contract security libraries |
| MiCA | EU crypto-assets regulation |
| AML / KYC | Anti-money laundering regulations |

## Network / Telecom

| Standard | Scope |
|---|---|
| IEEE 802.1Q / 802.1X / 802.3 | Ethernet, VLAN, NAC |
| IEEE 802.11ax/be | Wi-Fi 6 / Wi-Fi 7 |
| ITU-T | Telecom standards |
| TIA-942 | Data center infrastructure |

---

## QA / Test Automation

| Standard | Scope |
|---|---|
| ISO/IEC 29119 | International standard for software testing |
| IEEE 829 | Standard for software and system test documentation |
| ISTQB Guidelines | Worldwide standard for software testing certification and terminology |
| WCAG 2.1 Level AA | Web content accessibility rules for testing accessibility gates |

---

## Database Architect / DBA

| Standard | Scope |
|---|---|
| ACID | Standards for transactional reliability (Atomicity, Consistency, Isolation, Durability) |
| CAP Theorem | Trade-offs between Consistency, Availability, and Partition tolerance |
| TPC-C / TPC-H | Transaction processing and decision support benchmarks |
| GDPR Art 17 / Art 32 | Right to erasure (scrubbing/deletion) and security of data processing |

---

## Product Management / Business Analysis

| Standard | Scope |
|---|---|
| Scrum Guide | Standard framework for Scrum rules, roles, and events |
| IIBA BABOK | Business Analysis Body of Knowledge standard |
| Agile Alliance Principles | Core principles for agile software development |
| Gherkin BDD | Standardized natural language syntax for behavior-driven development requirements |

---

## Security Compliance / DevSecOps

| Standard | Scope |
|---|---|
| ISO/IEC 27017 / 27018 | Cloud security controls and protection of PII in public clouds |
| SOC 2 Type II | Audit report for operational security, availability, and privacy controls |
| OWASP ASVS | Application Security Verification Standard |
| CIS Controls | Critical security controls checklist for securing systems |

---

## Cloud Architecture

| Standard | Scope |
|---|---|
| AWS Well-Architected Framework | 6-pillar cloud architecture review (Security, Reliability, Cost, etc.) |
| Azure Well-Architected Framework | Microsoft cloud architecture assessment framework |
| GCP Architecture Framework | Google Cloud design and operational best practices |
| SOC 2 Type II | Cloud service security and availability audit |
| ISO 27017 | Cloud-specific information security controls |
| CSA STAR | Cloud Security Alliance trust certification |
| NIST 800-53 | Federal security controls applicable to cloud environments |

---

## API Design & Integration

| Standard | Scope |
|---|---|
| OpenAPI Specification 3.1 | API contract definition standard (formerly Swagger) |
| JSON:API | JSON response format convention for REST APIs |
| RFC 7807 (Problem Details) | Standard error response format for HTTP APIs |
| OAuth 2.0 / OpenID Connect | Authentication and authorization protocol standards |
| gRPC / Protocol Buffers | High-performance RPC service definition standard |

---

## UI/UX Design Engineering

| Standard | Scope |
|---|---|
| WCAG 2.1 Level AA | Web content accessibility guidelines |
| EN 301 549 | European ICT accessibility standard |
| Section 508 | US federal accessibility requirements |
| WAI-ARIA 1.2 | Accessible Rich Internet Applications specification |

---

## Mobile Native Development

| Standard | Scope |
|---|---|
| Apple App Store Review Guidelines | iOS app distribution and compliance requirements |
| Google Play Developer Policy | Android app distribution requirements |
| Apple Human Interface Guidelines | iOS/macOS design and interaction standards |
| Material Design 3 | Android/cross-platform UI design system guidelines |
| App Tracking Transparency (ATT) | iOS user privacy and tracking consent framework |

---

## ERP & Enterprise Systems

| Standard | Scope |
|---|---|
| SOX (Sarbanes-Oxley) | Financial system internal controls and audit compliance |
| GxP (Good Practice) | Pharmaceutical/life sciences ERP validation |
| EDIFACT / X12 | Electronic Data Interchange standards for supply chain |
| GDPR / KVKK | Personal data protection in HR and CRM modules |

---

## Technical Writing & Documentation

| Standard | Scope |
|---|---|
| Diataxis Framework | Documentation content taxonomy (tutorials, how-to, reference, explanation) |
| Google Developer Documentation Style Guide | Technical writing style and formatting standard |
| Microsoft Writing Style Guide | Technical content voice, tone, and formatting rules |
| ASD-STE100 | Simplified Technical English for regulated industries |
