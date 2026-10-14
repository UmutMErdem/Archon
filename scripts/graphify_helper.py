"""Build, update, and query a Graphify knowledge graph for a project.

Standalone on purpose: bootstrap_target.py copies this file into target projects.
"""

import argparse
import os
import shutil
import subprocess
import sys

# Keep in sync with requirements-graphify.txt.
GRAPHIFY_REQUIREMENT = "graphifyy==0.9.90"

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except AttributeError:
    pass


def is_graphify_installed():
    return shutil.which("graphify") is not None


def install_graphify():
    """Install the pinned graphifyy package with uv (preferred) or pip."""
    if shutil.which("uv"):
        print(f"Installing {GRAPHIFY_REQUIREMENT} with uv...")
        try:
            subprocess.run(
                ["uv", "tool", "install", GRAPHIFY_REQUIREMENT, "--with", "matplotlib"],
                check=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"uv installation failed: {e}. Trying pip...")
        else:
            return True

    print(f"Installing {GRAPHIFY_REQUIREMENT} and matplotlib with pip...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", GRAPHIFY_REQUIREMENT, "matplotlib"],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error: pip installation failed: {e}")
        return False
    return True


def run_command(cmd, quiet=False):
    try:
        subprocess.run(cmd, check=True, capture_output=quiet)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error running command {' '.join(cmd)}: {e}")
        return False
    return True


def ensure_graphify(allow_install):
    if is_graphify_installed():
        return True
    if not allow_install:
        print(
            "Error: the 'graphify' CLI is not on PATH. Install it with\n"
            f"  pip install {GRAPHIFY_REQUIREMENT} matplotlib\n"
            "or re-run this script with --install."
        )
        return False
    if not install_graphify():
        return False
    if not is_graphify_installed():
        print(
            "Error: graphifyy was installed but 'graphify' is still not on PATH. "
            "Add the install location (e.g. `uv tool dir --bin`) to PATH."
        )
        return False
    return True


def build(target_path, update):
    print(f"{'Updating' if update else 'Building'} knowledge graph for: {target_path}")
    cmd = ["graphify", target_path] + (["--update"] if update else [])
    if not run_command(cmd):
        return 1

    graph_json = os.path.join(target_path, "graphify-out", "graph.json")
    steps = [
        (["graphify", "cluster-only", target_path, "--no-label"], False),
        (["graphify", "export", "svg", "--graph", graph_json], False),
        (
            [
                "graphify",
                "export",
                "obsidian",
                "--graph",
                graph_json,
                "--dir",
                os.path.join(target_path, "graphify-out", "obsidian"),
            ],
            True,
        ),
        (["graphify", "export", "wiki", "--graph", graph_json], True),
    ]
    failed = [" ".join(cmd[:3]) for cmd, quiet in steps if not run_command(cmd, quiet)]

    out_dir = os.path.join(target_path, "graphify-out")
    if failed:
        print(f"\n❌ Graph built in {out_dir}, but these steps failed: {', '.join(failed)}")
        return 1
    print(f"\n✅ Graphify analysis and exports complete: {out_dir}")
    print("  - graph.json, graph.html, graph.svg, obsidian/, wiki/")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--path", default=".", help="Project to analyze (default: .)")
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--build", action="store_true", help="Build the graph (default)")
    action.add_argument("--update", action="store_true", help="Incremental update")
    action.add_argument("--query", type=str, help="Ask the graph a question")
    action.add_argument("--hooks", action="store_true", help="Install git hooks")
    action.add_argument(
        "--install-only", action="store_true", help=f"Install {GRAPHIFY_REQUIREMENT} and exit"
    )
    parser.add_argument(
        "--install",
        action="store_true",
        help=f"Install {GRAPHIFY_REQUIREMENT} if the graphify CLI is missing",
    )
    args = parser.parse_args(argv)

    if not ensure_graphify(args.install or args.install_only):
        return 1
    if args.install_only:
        print("Graphify is ready.")
        return 0

    target_path = os.path.abspath(args.path)
    if args.hooks:
        ok = run_command(["graphify", target_path, "--install-hooks"])
        print("Git hooks installed." if ok else "Failed to install git hooks.")
        return 0 if ok else 1
    if args.query:
        print(f"Querying graph in {target_path}: '{args.query}'")
        try:
            subprocess.run(["graphify", "query", args.query], check=True, cwd=target_path)
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Query failed: {e}")
            return 1
        return 0
    return build(target_path, args.update)


if __name__ == "__main__":
    sys.exit(main())
