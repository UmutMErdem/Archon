"""Propose Tier 1 / Tier 2 personas for a target workspace from detection_signals.md.

Applies the tier assignment rules of architecture/00_detection.md: only strong signals
select a tier, the domain with the most matching files is Tier 1, and at most 3 other
domains with strong signals become Tier 2 (ties broken by interface bullets with Tier 1).
"""

import argparse
import fnmatch
import os
import re
import sys

from archon_core import (
    PERSONAS_DIR,
    iter_interfaces,
    load_registry,
    read_text,
    resolve_domain_to_persona_file,
    setup_utf8,
)

SKIP_DIRS = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    "graphify-out",
    "dist",
    "build",
}
MAX_TIER2 = 3


def patterns(cell):
    out = []
    for token in re.findall(r"`([^`]+)`", cell):
        out += [p.strip() for p in re.split(r",\s*", token) if p.strip()]
    return out


def workspace_paths(root):
    files, dirs = [], []
    for current, subdirs, names in os.walk(root):
        subdirs[:] = [d for d in subdirs if d not in SKIP_DIRS]
        rel = os.path.relpath(current, root).replace(os.sep, "/")
        rel = "" if rel == "." else rel + "/"
        dirs += [rel + d + "/" for d in subdirs]
        files += [rel + n for n in names]
    return files, dirs


def match_count(pattern, files, dirs):
    if pattern.endswith("/"):
        return sum(1 for d in dirs if d == pattern or d.endswith("/" + pattern))
    if "/" in pattern:
        return sum(
            1
            for f in files
            if fnmatch.fnmatchcase(f, pattern) or fnmatch.fnmatchcase(f, "*/" + pattern)
        )
    return sum(1 for f in files if fnmatch.fnmatchcase(f.rsplit("/", 1)[-1], pattern))


def score(root, registry):
    files, dirs = workspace_paths(root)
    results = {}
    for pf, row in registry.items():
        strong = {p: match_count(p, files, dirs) for p in patterns(row["signals"])}
        weak = {p: match_count(p, files, dirs) for p in patterns(row["weak"])}
        results[pf] = {
            "strong": sum(strong.values()),
            "weak": sum(weak.values()),
            "hits": sorted(p for p, n in {**strong, **weak}.items() if n),
        }
    return results


def interface_links(a, b, registry, personas_dir=PERSONAS_DIR):
    n = 0
    for src, dst in ((a, b), (b, a)):
        content = read_text(os.path.join(personas_dir, src))
        n += sum(
            1
            for label, _ in iter_interfaces(content)
            if resolve_domain_to_persona_file(label, registry) == dst
        )
    return n


def assign_tiers(results, registry, personas_dir=PERSONAS_DIR):
    strong = [pf for pf, r in results.items() if r["strong"]]
    if not strong:
        return None, [], []
    strong.sort(key=lambda pf: (-results[pf]["strong"], pf))
    tier1 = strong[0]
    if len(strong) > 1 and results[strong[1]]["strong"] == results[tier1]["strong"]:
        tied = [pf for pf in strong if results[pf]["strong"] == results[tier1]["strong"]]
        return None, tied, []
    candidates = sorted(
        strong[1:],
        key=lambda pf: (
            -results[pf]["strong"],
            -interface_links(tier1, pf, registry, personas_dir),
            pf,
        ),
    )
    return tier1, candidates[:MAX_TIER2], candidates[MAX_TIER2:]


def main(argv=None):
    setup_utf8()
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("target", help="Target project directory")
    args = parser.parse_args(argv)

    root = os.path.abspath(args.target)
    if not os.path.isdir(root):
        print(f"❌ Not a directory: {root}")
        return 2
    registry = load_registry()
    results = score(root, registry)
    tier1, tier2, rest = assign_tiers(results, registry)

    print(f"{'Persona':<28} {'Strong':>6} {'Weak':>5}  Matched signals")
    for pf, r in sorted(results.items(), key=lambda x: (-x[1]["strong"], -x[1]["weak"], x[0])):
        if r["strong"] or r["weak"]:
            print(f"{pf:<28} {r['strong']:>6} {r['weak']:>5}  {', '.join(r['hits'])}")

    if tier1 is None and tier2:
        print(f"\n⚖️  Tie for Tier 1 between {', '.join(tier2)}: ask the user to choose.")
    elif tier1 is None:
        print("\n❓ No strong signal matched: ask the user the Step 1 domain question.")
    else:
        print(f"\nTier 1: {tier1}")
        print(f"Tier 2: {', '.join(tier2) or '-'}")
        if rest:
            print(f"Tier 3 (strong signals beyond the Tier 2 limit): {', '.join(rest)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
