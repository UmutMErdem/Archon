# PROJECT_STATE.md
> Last updated: 2026-10-14. Source of truth: actual code.

## Version & platform
| Param | Value |
|---|---|
| Version | v0.1.0 (unreleased, see M-006) |
| Platform | Markdown manifesto + Python 3.10–3.14 scripts (stdlib runtime) |
| Build status | ✅ black, ruff, pytest (~96 % coverage), `sync_matrix.py --check`, `validate_manifesto.py` |

## Architecture
- AI agents read [architecture.md](../architecture.md) → `architecture/00_detection.md` … `rules.md`, then load personas.
- [detection_signals.md](../detection_signals.md) is the persona registry (signals, domain, file, interface label).
- `scripts/archon_core.py` is shared by every script; `validate_manifesto.py` enforces all cross-file contracts.
- `sync_matrix.py` is the only writer of [CROSS_DOMAIN_MATRIX.md](../CROSS_DOMAIN_MATRIX.md).
- `bootstrap_target.py`, `detect_domain.py`, `graphify_helper.py` operate on target projects.

## Open items
- [M-006](ROADMAP.md) — tag v0.1.0 after merge
- All KI-001…KI-038 and F-01…F-17 are closed: [KNOWN_ISSUES.md](KNOWN_ISSUES.md), [OPTIMIZATIONS.md](OPTIMIZATIONS.md)
