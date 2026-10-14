import io
from unittest.mock import MagicMock, patch

import bootstrap_target as bt
from archon_core import read_text

SPEC_FILES = 12


def run(tmp_path, *extra):
    return bt.main(["--target", str(tmp_path), "--primary", "embedded_iot.md", *extra])


def test_parse_files_spec_matches_spec():
    spec, sections = bt.parse_files_spec(read_text(bt.FILES_SPEC_PATH))
    assert len(spec) == SPEC_FILES
    assert "KNOWN_ISSUES.md" in spec and "ARCHITECTURE.md" in spec
    assert len(sections) == 13
    assert sections[0] == "Main Idea & Project Recap" and sections[4] == "Build, Deploy & Run"


def test_scaffold_creates_spec_files_without_machine_links(tmp_path, capsys):
    assert run(tmp_path, "--supporting", "hardware_design.md") == 0
    created = sorted(p.name for p in tmp_path.iterdir())
    assert len(created) == SPEC_FILES
    for p in tmp_path.iterdir():
        text = p.read_text(encoding="utf-8")
        assert "file:///" not in text
        assert "[Document" not in text
    agents = (tmp_path / "AGENTS.md").read_text(encoding="utf-8")
    assert "Tier 1 (Primary)" in agents and "personas/embedded_iot.md" in agents
    assert "Tier 2 (Supporting)" in agents and "personas/hardware_design.md" in agents
    state = (tmp_path / "PROJECT_STATE.md").read_text(encoding="utf-8")
    assert bt.SCAFFOLD_STATUS in state and "Archon version" in state
    arch = (tmp_path / "ARCHITECTURE.md").read_text(encoding="utf-8")
    assert "## 5. Build, Deploy & Run" in arch and "## 13. Known Problems & TODO" in arch
    assert "KI-NNN" in (tmp_path / "KNOWN_ISSUES.md").read_text(encoding="utf-8")
    assert f"Written ({SPEC_FILES})" in capsys.readouterr().out


def test_existing_files_preserved(tmp_path, capsys):
    (tmp_path / "AGENTS.md").write_text("hand written\n", encoding="utf-8")
    assert run(tmp_path) == 0
    assert (tmp_path / "AGENTS.md").read_text(encoding="utf-8") == "hand written\n"
    assert "Skipped, already exist (1): AGENTS.md" in capsys.readouterr().out

    assert run(tmp_path, "--force") == 0
    assert "hand written" not in (tmp_path / "AGENTS.md").read_text(encoding="utf-8")


@patch("subprocess.run")
def test_graphify_setup(mock_run, tmp_path):
    mock_run.return_value = MagicMock(returncode=0)
    (tmp_path / ".gitignore").write_text("node_modules/", encoding="utf-8")
    assert run(tmp_path, "--graphify", "--install-graphify") == 0
    assert (tmp_path / "scripts" / "graphify_helper.py").exists()
    assert (tmp_path / ".gitignore").read_text(encoding="utf-8") == (
        "node_modules/\n\n# Graphify Outputs\ngraphify-out/\n"
    )
    assert (tmp_path / ".graphifyignore").exists()
    cmd = mock_run.call_args[0][0]
    assert cmd[-2:] == ["--build", "--install"]
    arch = (tmp_path / "ARCHITECTURE.md").read_text(encoding="utf-8")
    assert "graphify-out/graph.html" in arch and "graph.svg" not in arch
    assert "Graphify Knowledge Graph" in (tmp_path / "ONBOARDING.md").read_text(encoding="utf-8")


@patch("subprocess.run")
def test_graphify_failure_and_rerun_skips(mock_run, tmp_path, capsys):
    mock_run.return_value = MagicMock(returncode=1)
    assert run(tmp_path, "--graphify") == 1
    assert "--install" not in mock_run.call_args[0][0]
    assert "Failed: graphify build" in capsys.readouterr().out
    assert run(tmp_path, "--graphify") == 1
    assert "scripts/graphify_helper.py" in capsys.readouterr().out


def test_interactive_mode(tmp_path, monkeypatch):
    files = bt.list_persona_files()
    primary = files.index("devops.md") + 1
    support = files.index("cloud_architecture.md") + 1
    answers = f"{tmp_path}\n{primary}\n{support},999,x\nn\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(answers))
    assert bt.main([]) == 0
    agents = (tmp_path / "AGENTS.md").read_text(encoding="utf-8")
    assert "personas/devops.md" in agents and "personas/cloud_architecture.md" in agents


def test_missing_primary_is_an_error(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO(f"{tmp_path}\n\n\nn\n"))
    try:
        bt.main([])
    except SystemExit as e:
        assert e.code == 2
    assert "--target and --primary are required" in capsys.readouterr().err


def test_archon_version_fallback(monkeypatch):
    def boom(*a, **k):
        raise OSError

    monkeypatch.setattr(bt.subprocess, "run", boom)
    assert bt.archon_version() == "unknown"
