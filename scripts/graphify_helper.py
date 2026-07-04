import os
import sys
import subprocess
import argparse
import shutil

# Set system output to UTF-8
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except AttributeError:
    pass


def is_graphify_installed():
    """Check if graphify CLI is available in the environment."""
    return shutil.which("graphify") is not None


def install_graphify():
    """Attempt to install graphifyy package using uv or pip."""
    print("Graphify CLI not found. Attempting automatic installation...")

    # Check if uv is installed
    has_uv = shutil.which("uv") is not None

    if has_uv:
        print(
            "Detected 'uv'. Installing 'graphifyy' tool via uv with matplotlib support..."
        )
        try:
            subprocess.run(
                ["uv", "tool", "install", "graphifyy", "--with", "matplotlib"],
                check=True,
            )
            print("Successfully installed graphifyy using uv!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"uv installation failed: {e}. Trying pip...")

    # Fallback to pip
    print("Installing 'graphifyy' and 'matplotlib' via pip...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "graphifyy", "matplotlib"],
            check=True,
        )
        print("Successfully installed graphifyy using pip!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: Installation via pip failed: {e}")
        print("Please manually run: pip install graphifyy matplotlib")
        return False


def run_command(cmd):
    """Run a system command and return status."""
    try:
        result = subprocess.run(cmd, check=True)
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error running command {' '.join(cmd)}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Graphify Automation and Helper Script"
    )
    parser.add_argument(
        "--path",
        default=".",
        help="Target path to analyze (default: current directory)",
    )
    parser.add_argument(
        "--build", action="store_true", help="Build/rebuild the knowledge graph"
    )
    parser.add_argument(
        "--update", action="store_true", help="Perform incremental update of the graph"
    )
    parser.add_argument(
        "--query", type=str, help="Query/Ask a question to the knowledge graph"
    )
    parser.add_argument(
        "--hooks", action="store_true", help="Install Git hooks for automatic updates"
    )
    parser.add_argument(
        "--install-only", action="store_true", help="Only install graphifyy and exit"
    )

    args = parser.parse_args()

    # Ensure graphify is installed
    if not is_graphify_installed():
        success = install_graphify()
        if not success:
            sys.exit(1)

    if args.install_only:
        print("Graphify is ready.")
        sys.exit(0)

    target_path = os.path.abspath(args.path)

    # Handle hooks installation
    if args.hooks:
        print(f"Installing Git hooks in {target_path}...")
        cmd = ["graphify", target_path, "--install-hooks"]
        if run_command(cmd):
            print("Git hooks installed successfully.")
        else:
            print("Failed to install Git hooks.")
        sys.exit(0)

    # Handle querying
    if args.query:
        print(f"Querying graph in {target_path}: '{args.query}'...")
        cmd = ["graphify", "query", args.query]
        # Query typically runs in the workspace where graphify-out exists
        original_cwd = os.getcwd()
        try:
            os.chdir(target_path)
            run_command(cmd)
        finally:
            os.chdir(original_cwd)
        sys.exit(0)

    # Handle build or update
    if args.build or args.update or len(sys.argv) == 1:
        action_name = "Updating" if args.update else "Building"
        print(f"{action_name} knowledge graph for: {target_path}")

        # 1. Run main extract/build command
        cmd = ["graphify", target_path]
        if args.update:
            cmd.append("--update")

        print(f"Running extract command: {' '.join(cmd)}")
        if not run_command(cmd):
            print("Failed to run Graphify extraction.")
            sys.exit(1)

        # 2. Run cluster-only to generate HTML visualizer and report
        cluster_cmd = ["graphify", "cluster-only", target_path, "--no-label"]
        print(f"Running cluster command: {' '.join(cluster_cmd)}")
        run_command(cluster_cmd)

        # 3. Export SVG diagram
        graph_json_path = os.path.join(target_path, "graphify-out", "graph.json")
        svg_cmd = ["graphify", "export", "svg", "--graph", graph_json_path]
        print(f"Running SVG export command: {' '.join(svg_cmd)}")
        run_command(svg_cmd)

        # 4. Optional Exports (Obsidian and Wiki)
        obsidian_dir = os.path.join(target_path, "graphify-out", "obsidian")
        obsidian_cmd = [
            "graphify",
            "export",
            "obsidian",
            "--graph",
            graph_json_path,
            "--dir",
            obsidian_dir,
        ]
        print(f"Running Obsidian export command: {' '.join(obsidian_cmd)}")
        subprocess.run(
            obsidian_cmd, capture_output=True
        )  # Run silently to avoid cluttering logs on expected minor errors

        wiki_cmd = ["graphify", "export", "wiki", "--graph", graph_json_path]
        print(f"Running Wiki export command: {' '.join(wiki_cmd)}")
        subprocess.run(wiki_cmd, capture_output=True)  # Run silently

        print(f"\n✅ Graphify analysis and exports complete!")
        print(f"Output files generated in: {os.path.join(target_path, 'graphify-out')}")
        print(f"  - Full Graph Data: graphify-out/graph.json")
        print(f"  - Interactive View: graphify-out/graph.html")
        print(f"  - SVG Diagram: graphify-out/graph.svg")
        print(f"  - Obsidian Vault: graphify-out/obsidian/ (optional)")
        print(f"  - Wiki: graphify-out/wiki/ (optional)")


if __name__ == "__main__":
    main()
