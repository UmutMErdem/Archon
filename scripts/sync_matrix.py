"""Regenerate CROSS_DOMAIN_MATRIX.md from the personas' `## Cross-Domain Interfaces` sections.

This is the only writer of CROSS_DOMAIN_MATRIX.md. `--check` exits 1 if the file is stale.
"""

import argparse
import os
import sys

from archon_core import (
    COMPLETENESS_LEVELS,
    MATRIX_PATH,
    PERSONAS_DIR,
    SIGNALS_PATH,
    completeness,
    display_name,
    iter_interfaces,
    list_persona_files,
    load_registry,
    node_id,
    read_text,
    resolve_domain_to_persona_file,
    setup_utf8,
    write_text,
)

LEVEL_COLORS = {
    "Comprehensive": "#FF6B6B",
    "Thorough": "#FFA94D",
    "Moderate": "#69DB7C",
    "Sparse": "#74C0FC",
}


def collect(personas_dir=PERSONAS_DIR, signals_path=SIGNALS_PATH):
    """Return (rows, levels, registry): rows are (from_file, to_file, description)."""
    registry = load_registry(signals_path)
    rows, levels = [], {}
    for pf in list_persona_files(personas_dir):
        content = read_text(os.path.join(personas_dir, pf))
        levels[pf] = completeness(content)["label"]
        for label, desc in iter_interfaces(content):
            target = resolve_domain_to_persona_file(label, registry)
            if target:
                rows.append((pf, target, desc))
    rows.sort(key=lambda r: (display_name(r[0], registry), display_name(r[1], registry)))
    return rows, levels, registry


def level_legend():
    parts, low = [], 0
    for limit, name in COMPLETENESS_LEVELS:
        bound = f"{low}+" if limit == float("inf") else f"{low}–{limit}"
        parts.append(f"{name} ({bound})")
        low = limit + 1
    return " · ".join(parts)


def render_matrix(rows, levels, registry):
    out = [
        "# Cross-Domain Interface Matrix",
        "",
        "> Generated from `personas/*.md` by `scripts/sync_matrix.py`. Do not edit by hand:",
        "> change the persona's `## Cross-Domain Interfaces` section and re-run the script.",
        "> Each row is a directional interface; `scripts/validate_manifesto.py` enforces that both directions exist.",
        "",
        "---",
        "",
        "## Interface Table",
        "",
        "| From Persona | To Persona | Interface Contract |",
        "|---|---|---|",
    ]
    out += [
        f"| {display_name(a, registry)} | {display_name(b, registry)} | {d} |" for a, b, d in rows
    ]

    out += [
        "",
        "---",
        "",
        "## Relationship Diagram",
        "",
        "> One undirected edge per persona pair. Node color = persona completeness level "
        "(sections + interfaces + compliance bullets, see `scripts/calculate_complexity.py`):",
        "> " + level_legend() + ".",
        "",
        "```mermaid",
        "graph LR",
    ]
    files = sorted(levels)
    out += [f'    {node_id(pf)}["{display_name(pf, registry)}"]' for pf in files]
    out.append("")
    for name, color in LEVEL_COLORS.items():
        ids = [node_id(pf) for pf in files if levels[pf] == name]
        if ids:
            out.append(f"    style {','.join(ids)} fill:{color},stroke:#333,stroke-width:1px")
    out.append("")
    pairs = sorted({tuple(sorted((a, b))) for a, b, _ in rows})
    out += [f"    {node_id(a)} --- {node_id(b)}" for a, b in pairs]
    out += ["```", ""]
    return "\n".join(out)


def main(argv=None):
    setup_utf8()
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--check", action="store_true", help="Exit 1 if CROSS_DOMAIN_MATRIX.md is stale"
    )
    args = parser.parse_args(argv)

    expected = render_matrix(*collect())
    current = read_text(MATRIX_PATH) if os.path.exists(MATRIX_PATH) else ""
    if args.check:
        if current != expected:
            print("❌ CROSS_DOMAIN_MATRIX.md is stale. Run: python scripts/sync_matrix.py")
            return 1
        print("✅ CROSS_DOMAIN_MATRIX.md is up to date.")
        return 0
    if current != expected:
        write_text(MATRIX_PATH, expected)
        print("✅ CROSS_DOMAIN_MATRIX.md regenerated.")
    else:
        print("✅ CROSS_DOMAIN_MATRIX.md already up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
