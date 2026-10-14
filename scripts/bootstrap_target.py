"""Scaffold Archon documentation skeletons into a target project.

Skeletons are derived from architecture/files_spec.md. Existing files are never
overwritten unless --force is given.
"""

import argparse
import datetime
import os
import re
import shutil
import subprocess
import sys

from archon_core import (
    FILES_SPEC_PATH,
    PERSONAS_DIR,
    REPO_ROOT,
    list_persona_files,
    parse_frontmatter,
    read_text,
    setup_utf8,
    write_text,
)

NOT_FOUND = "_Not found in source yet: fill in during the first Archon analysis._"
SCAFFOLD_STATUS = "Status: SCAFFOLDED"

GRAPHIFYIGNORE = """# Default Graphify Ignore File
graphify-out/
.git/
__pycache__/
.pytest_cache/
.ruff_cache/
node_modules/
dist/
build/
.venv/
venv/
"""


def prompt(text):
    sys.stdout.write(text)
    sys.stdout.flush()
    return sys.stdin.readline().strip()


def archon_version():
    try:
        return subprocess.run(
            ["git", "describe", "--tags", "--always", "--dirty"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def parse_files_spec(spec_md):
    """{filename: [spec bullet, ...]} plus the numbered ARCHITECTURE.md section titles."""
    files, current = {}, None
    for line in spec_md.splitlines():
        m = re.match(r"^### (\S+\.md)", line)
        if m:
            current = m.group(1)
            files[current] = []
        elif current and line.startswith("- "):
            files[current].append(line[2:].strip())
    arch_sections = re.findall(r"^\d+\.\s+\*\*(.+?)\*\*", spec_md, re.MULTILINE)
    return files, arch_sections


def spec_block(bullets):
    if not bullets:
        return "> Archon scaffold. Required sections: see `architecture/files_spec.md`."
    lines = ["> Archon scaffold. Required content (see `architecture/files_spec.md`):"]
    lines += [f"> - {b}" for b in bullets]
    return "\n".join(lines)


def persona_line(meta, version):
    return (
        f"- **Domain:** {meta.get('domain')}\n"
        f"- **Role:** {meta.get('expert_role')}\n"
        f"- **Persona:** Archon `personas/{meta['file']}` @ `{version}`"
    )


def render_files(primary, supporting, spec, arch_sections, graphify, version, today):
    files = {}
    for name, bullets in spec.items():
        files[name] = f"# {name}\n\n{spec_block(bullets)}\n"

    agents = files["AGENTS.md"] + "\n## Active Personas\n\n### Tier 1 (Primary)\n"
    agents += persona_line(primary, version) + "\n"
    if supporting:
        agents += "\n### Tier 2 (Supporting)\n"
        agents += "\n\n".join(persona_line(s, version) for s in supporting) + "\n"
    for heading in (
        "Must-follow constraints",
        "Architecture quick-reference",
        "Validation checklist",
        "Repo conventions",
    ):
        agents += f"\n## {heading}\n\n{NOT_FOUND}\n"
    files["AGENTS.md"] = agents

    files["PROJECT_STATE.md"] += (
        f"\n{SCAFFOLD_STATUS}\n\n## Version Snapshot\n\n"
        "| Field | Value |\n|---|---|\n"
        f"| Scaffold date | {today} |\n"
        "| Git commit | N/A |\n| Branch | N/A |\n"
        f"| Archon version | `{version}` |\n"
    )

    arch = files["ARCHITECTURE.md"] + "\n"
    for i, title in enumerate(arch_sections, 1):
        arch += f"\n## {i}. {title}\n\n"
        if title == "System Mapping" and graphify:
            arch += (
                f"{NOT_FOUND}\n\nCodebase graph: run `python scripts/graphify_helper.py --build`, "
                "then open `graphify-out/graph.html`.\n"
            )
        else:
            arch += f"{NOT_FOUND}\n"
    files["ARCHITECTURE.md"] = arch

    if graphify:
        files["ONBOARDING.md"] += (
            "\n## Graphify Knowledge Graph\n\n"
            "- Build: `python scripts/graphify_helper.py --build`\n"
            "- Incremental update: `python scripts/graphify_helper.py --update`\n"
            '- Query: `python scripts/graphify_helper.py --query "your question"`\n'
            "- View: open `graphify-out/graph.html` (git-ignored, rebuild locally)\n"
        )
    return files


def write_new(path, content, force, report):
    if os.path.exists(path) and not force:
        report["skipped"].append(os.path.basename(path))
        return
    write_text(path, content)
    report["written"].append(os.path.basename(path))


def setup_graphify(target_dir, install, force, report):
    scripts_dir = os.path.join(target_dir, "scripts")
    os.makedirs(scripts_dir, exist_ok=True)
    helper_dst = os.path.join(scripts_dir, "graphify_helper.py")
    if os.path.exists(helper_dst) and not force:
        report["skipped"].append("scripts/graphify_helper.py")
    else:
        shutil.copy2(os.path.join(REPO_ROOT, "scripts", "graphify_helper.py"), helper_dst)
        report["written"].append("scripts/graphify_helper.py")

    gitignore = os.path.join(target_dir, ".gitignore")
    existing = read_text(gitignore) if os.path.exists(gitignore) else ""
    if "graphify-out/" not in existing:
        sep = "" if not existing or existing.endswith("\n") else "\n"
        write_text(gitignore, existing + sep + "\n# Graphify Outputs\ngraphify-out/\n")
        report["written"].append(".gitignore (graphify-out/ added)")

    write_new(os.path.join(target_dir, ".graphifyignore"), GRAPHIFYIGNORE, force, report)

    cmd = [sys.executable, helper_dst, "--path", target_dir, "--build"]
    if install:
        cmd.append("--install")
    print("Running Graphify initial build...")
    if subprocess.run(cmd, check=False).returncode != 0:
        report["failed"].append("graphify build")


def load_persona(filename):
    meta, err = parse_frontmatter(read_text(os.path.join(PERSONAS_DIR, filename)))
    if err:
        raise SystemExit(f"personas/{filename}: {err}")
    meta["file"] = filename
    return meta


def interactive_args(files):
    target = prompt("Target project workspace path: ")
    print("\nAvailable personas:")
    for i, f in enumerate(files, 1):
        print(f"  [{i}] {f}")

    def pick(text):
        out = []
        for c in prompt(text).split(","):
            if c.strip().isdigit() and 1 <= int(c) <= len(files):
                out.append(files[int(c) - 1])
        return out

    primary = pick("\nPrimary (Tier 1) persona number: ")[:1]
    supporting = pick("Supporting (Tier 2) persona numbers, comma-separated (blank for none): ")
    graphify = prompt("Set up Graphify? (y/n): ").lower() == "y"
    install = graphify and prompt("Install graphifyy if missing? (y/n): ").lower() == "y"
    argv = ["--target", target]
    if primary:
        argv += ["--primary", primary[0]]
    for s in supporting:
        argv += ["--supporting", s]
    if graphify:
        argv.append("--graphify")
    if install:
        argv.append("--install-graphify")
    return argv


def build_parser(files):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--target", help="Target project directory (prompted if omitted)")
    parser.add_argument("--primary", choices=files, help="Tier 1 persona file")
    parser.add_argument(
        "--supporting",
        action="append",
        default=[],
        choices=files,
        help="Tier 2 persona file (repeatable)",
    )
    parser.add_argument("--graphify", action="store_true", help="Set up Graphify")
    parser.add_argument(
        "--install-graphify", action="store_true", help="Allow installing graphifyy if missing"
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    return parser


def main(argv=None):
    setup_utf8()
    files = list_persona_files()
    parser = build_parser(files)
    if argv is None:
        argv = sys.argv[1:]
    if "--target" not in argv and not any(a.startswith("--target=") for a in argv):
        argv = interactive_args(files) + list(argv)
    args = parser.parse_args(argv)
    if not args.target or not args.primary:
        parser.error("--target and --primary are required")

    target_dir = os.path.abspath(args.target)
    os.makedirs(target_dir, exist_ok=True)
    primary = load_persona(args.primary)
    supporting = [load_persona(f) for f in args.supporting if f != args.primary]

    spec, arch_sections = parse_files_spec(read_text(FILES_SPEC_PATH))
    rendered = render_files(
        primary,
        supporting,
        spec,
        arch_sections,
        args.graphify,
        archon_version(),
        datetime.date.today().isoformat(),
    )

    report = {"written": [], "skipped": [], "failed": []}
    for name, content in rendered.items():
        write_new(os.path.join(target_dir, name), content, args.force, report)
    if args.graphify:
        setup_graphify(target_dir, args.install_graphify, args.force, report)

    print(f"\nTarget: {target_dir}")
    print(f"✅ Written ({len(report['written'])}): {', '.join(report['written']) or '-'}")
    if report["skipped"]:
        print(
            f"⏭️  Skipped, already exist ({len(report['skipped'])}): {', '.join(report['skipped'])}"
            " (use --force to overwrite)"
        )
    if report["failed"]:
        print(f"❌ Failed: {', '.join(report['failed'])}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
