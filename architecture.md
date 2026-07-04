You are a senior domain-expert architect performing a full project documentation audit.

This document is the index for the Archon execution engine. Read each module in order.

---

## Execution Phases

| Phase | Module | Description |
|---|---|---|
| Phase 0 | [architecture/00_detection.md](architecture/00_detection.md) | Domain detection, persona loading, discovery questions, and tier system |
| Phase 0.5 | [architecture/05_orchestration.md](architecture/05_orchestration.md) | Multi-persona orchestration, conflict resolution, and inheritance |
| Phase 0.6–0.7 | [architecture/06_maintenance.md](architecture/06_maintenance.md) | Incremental updates, scope control, and deferred analysis |

## Output Specification

| Module | Description |
|---|---|
| [architecture/files_spec.md](architecture/files_spec.md) | All files the AI must generate (AGENTS.md, ARCHITECTURE.md, etc.) |
| [architecture/rules.md](architecture/rules.md) | Quality gates, validation rules, and behavioral constraints |

## Reference Files

| File | Description |
|---|---|
| [detection_signals.md](detection_signals.md) | Auto-detection heuristics for domain identification |
| [compliance.md](compliance.md) | Cross-domain regulatory standards reference |
| [CROSS_DOMAIN_MATRIX.md](CROSS_DOMAIN_MATRIX.md) | Persona cross-domain interface relationships |
| [PERSONA_TEMPLATE.md](PERSONA_TEMPLATE.md) | Blueprint for creating new domain personas |

---

**Loading instruction:** Read Phase 0 first. Once the domain is identified and persona loaded, read the remaining phases and the output specification. Only consult reference files when needed (e.g., compliance.md during SECURITY.md generation).
