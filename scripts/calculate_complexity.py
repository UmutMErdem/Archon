"""Print the completeness score of every persona (sections + interfaces + compliance bullets)."""

import argparse
import os
import sys

from archon_core import (
    PERSONAS_DIR,
    completeness,
    list_persona_files,
    read_text,
    setup_utf8,
)


def scores(personas_dir=PERSONAS_DIR):
    return {
        pf: completeness(read_text(os.path.join(personas_dir, pf)))
        for pf in list_persona_files(personas_dir)
    }


def render_report(results):
    lines = [
        f"{'Persona':<28} {'Sections':>8} {'Interfaces':>10} {'Compliance':>10} {'Score':>6}  Level",
        "-" * 80,
    ]
    for pf, s in results.items():
        lines.append(
            f"{pf:<28} {s['sections']:>8} {s['interfaces']:>10} {s['compliance']:>10} {s['score']:>6}  {s['label']}"
        )
    return "\n".join(lines)


def main(argv=None):
    setup_utf8()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--min-score",
        type=int,
        default=0,
        help="Exit 1 if any persona scores below this value",
    )
    args = parser.parse_args(argv)

    results = scores()
    print(render_report(results))
    low = [pf for pf, s in results.items() if s["score"] < args.min_score]
    if low:
        print(f"\n❌ Below --min-score {args.min_score}: {', '.join(low)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
