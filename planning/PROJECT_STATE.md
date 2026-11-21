# PROJECT_STATE.md
> Last updated: 2026-11-21. Source of truth: actual code.

## Version & platform
| Param | Value |
|---|---|
| Version | v0.1.0 (tagged 2026-10-14) |
| Platform | Markdown manifesto + Python 3.10–3.14 scripts (stdlib runtime) |
| Build status | ✅ black, ruff, pytest (~96 % coverage), `sync_matrix.py --check`, `validate_manifesto.py` |

## Architecture
- AI agents read [architecture.md](../architecture.md) → `architecture/00_detection.md` … `rules.md`, then load personas.
- 30 personas (30–400 lines, D-009), each with Hard Rules, Detect/Fix pitfalls, and sourced budget references (D-008). Generic audit rules from the PCB design guide live in the engine (D-010).
- `profiles/` binds personas to an EDA tool, fabricator, or sourcing region with dated, sourced values (D-011); loaded in Phase 0 Step 2b.
- [detection_signals.md](../detection_signals.md) is the persona registry (signals, domain, file, interface label).
- `scripts/archon_core.py` is shared by every script; `validate_manifesto.py` enforces all cross-file contracts.
- `sync_matrix.py` is the only writer of [CROSS_DOMAIN_MATRIX.md](../CROSS_DOMAIN_MATRIX.md).
- `bootstrap_target.py`, `detect_domain.py`, `graphify_helper.py` operate on target projects.

## Open items
- None. All milestones M-001…M-010 are done: [ROADMAP.md](ROADMAP.md)
- All KI-001…KI-040 and F-01…F-17 are closed: [KNOWN_ISSUES.md](KNOWN_ISSUES.md), [OPTIMIZATIONS.md](OPTIMIZATIONS.md)
