# OPTIMIZATIONS.md
> Performance/quality findings. Format: F-NN | status.
> F-01…F-17 come from the 2026-10-13 full review.
---
| ID | Category | Finding | Status |
|---|---|---|---|
| F-01 | Dead Code | `resolve_asymmetry.py` was a no-op (16/16 links existed) | IMPLEMENTED 2026-10-14 — deleted |
| F-02 | Dead Code | Unused `.get()` expressions in `sync_matrix.py` / `generate_diagram.py` | IMPLEMENTED 2026-10-14 — files rewritten |
| F-03 | Maintainability | `parse_frontmatter`, headings, interface regex, short names duplicated 2–5× | IMPLEMENTED 2026-10-14 — `scripts/archon_core.py` |
| F-04 | Reliability | Frontmatter lists duplicated body sections | IMPLEMENTED 2026-10-14 — D-004 |
| F-05 | Reliability | Test coverage 30 %, writers at 0 % | IMPLEMENTED 2026-10-14 — ~96 %, `fail_under = 80` |
| F-06 | Reliability | Generated files had no `--check` mode | IMPLEMENTED 2026-10-14 — `sync_matrix.py --check` in CI; complexity is report-only |
| F-07 | Usability | Bootstrap / create_persona were stdin-only | IMPLEMENTED 2026-10-14 — argparse with interactive fallback, explicit Tier 1 choice |
| F-08 | Maintainability | No `pyproject.toml`, `sys.path` hacks, unpinned mixed requirements | IMPLEMENTED 2026-10-14 — D-007 |
| F-09 | Quality | Ruff ran default rules only | IMPLEMENTED 2026-10-14 — `E,F,W,B,UP,SIM,PLW,I` |
| F-10 | Usability | Two diagrams of the same 212 edges | IMPLEMENTED 2026-10-14 — one undirected diagram (106 edges) |
| F-11 | Algorithm | Overrides re-normalized on every resolve call | IMPLEMENTED 2026-10-14 — overrides removed (D-003) |
| F-12 | Missing piece | Archon did not dogfood its own docs | IMPLEMENTED 2026-10-14 — `planning/`, `CHANGELOG.md`, Archon version in snapshots |
| F-13 | Consistency | 36 interface label spellings | IMPLEMENTED 2026-10-14 — registry labels enforced |
| F-14 | Docs | README tool table incomplete, no dev setup / license | IMPLEMENTED 2026-10-14 |
| F-15 | Missing feature | Domain detection was LLM-only | IMPLEMENTED 2026-10-14 — `scripts/detect_domain.py` |
| F-16 | Naming | Completeness column inside the routing table; "tier" overloaded | IMPLEMENTED 2026-10-14 — column removed, "completeness level" in matrix legend |
| F-17 | CI | Old action majors, single Python, unpinned tools | IMPLEMENTED 2026-10-14 — checkout@v4, setup-python@v5, 3.10 + 3.14 |
