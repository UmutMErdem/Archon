import os
import subprocess
import sys
from unittest.mock import MagicMock, patch

import graphify_helper as gh

PIN = gh.GRAPHIFY_REQUIREMENT


def which(*present):
    return lambda cmd: f"/usr/bin/{cmd}" if cmd in present else None


def test_requirement_is_pinned_and_matches_requirements_file():
    assert PIN.startswith("graphifyy==")
    with open(
        os.path.join(os.path.dirname(gh.__file__), "..", "requirements-graphify.txt"),
        encoding="utf-8",
    ) as f:
        req = f.read()
    assert PIN in req


@patch("subprocess.run")
@patch("shutil.which")
def test_install_prefers_uv(mock_which, mock_run):
    mock_which.side_effect = which("uv")
    assert gh.install_graphify() is True
    mock_run.assert_called_once_with(
        ["uv", "tool", "install", PIN, "--with", "matplotlib"], check=True
    )


@patch("subprocess.run")
@patch("shutil.which")
def test_install_falls_back_to_pip(mock_which, mock_run):
    mock_which.side_effect = which("uv")
    mock_run.side_effect = [subprocess.CalledProcessError(1, "uv"), MagicMock()]
    assert gh.install_graphify() is True
    mock_run.assert_called_with(
        [sys.executable, "-m", "pip", "install", PIN, "matplotlib"], check=True
    )


@patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, "pip"))
@patch("shutil.which", return_value=None)
def test_install_failure(mock_which, mock_run):
    assert gh.install_graphify() is False


@patch("subprocess.run")
@patch("shutil.which", return_value=None)
def test_no_auto_install_without_flag(mock_which, mock_run, capsys):
    assert gh.main(["--build"]) == 1
    mock_run.assert_not_called()
    assert "--install" in capsys.readouterr().out


@patch("graphify_helper.install_graphify", return_value=True)
@patch("shutil.which", return_value=None)
def test_install_without_path_entry_fails(mock_which, mock_install, capsys):
    assert gh.main(["--install-only"]) == 1
    assert "still not on PATH" in capsys.readouterr().out


@patch("graphify_helper.install_graphify", return_value=True)
@patch("shutil.which")
def test_install_only(mock_which, mock_install):
    mock_which.side_effect = [None, "/usr/bin/graphify"]
    assert gh.main(["--install-only"]) == 0
    mock_install.assert_called_once()


@patch("subprocess.run")
@patch("shutil.which")
def test_path_only_builds(mock_which, mock_run, tmp_path):
    mock_which.side_effect = which("graphify")
    assert gh.main(["--path", str(tmp_path)]) == 0
    mock_run.assert_any_call(["graphify", str(tmp_path)], check=True, capture_output=False)
    graph_json = os.path.join(str(tmp_path), "graphify-out", "graph.json")
    mock_run.assert_any_call(
        ["graphify", "export", "svg", "--graph", graph_json], check=True, capture_output=False
    )


@patch("subprocess.run")
@patch("shutil.which")
def test_update_flag(mock_which, mock_run, tmp_path):
    mock_which.side_effect = which("graphify")
    assert gh.main(["--path", str(tmp_path), "--update"]) == 0
    mock_run.assert_any_call(
        ["graphify", str(tmp_path), "--update"], check=True, capture_output=False
    )


@patch("subprocess.run")
@patch("shutil.which")
def test_failed_export_step_returns_1(mock_which, mock_run, tmp_path, capsys):
    mock_which.side_effect = which("graphify")

    def run(cmd, **kwargs):
        if cmd[1:3] == ["export", "svg"]:
            raise subprocess.CalledProcessError(1, cmd)
        return MagicMock()

    mock_run.side_effect = run
    assert gh.main(["--path", str(tmp_path)]) == 1
    assert "graphify export svg" in capsys.readouterr().out


@patch("subprocess.run", side_effect=FileNotFoundError("graphify"))
@patch("shutil.which")
def test_failed_extract_returns_1(mock_which, mock_run, tmp_path):
    mock_which.side_effect = which("graphify")
    assert gh.main(["--path", str(tmp_path)]) == 1


@patch("subprocess.run")
@patch("shutil.which")
def test_query_runs_in_target_dir(mock_which, mock_run, tmp_path):
    mock_which.side_effect = which("graphify")
    assert gh.main(["--path", str(tmp_path), "--query", "deps?"]) == 0
    mock_run.assert_called_once_with(["graphify", "query", "deps?"], check=True, cwd=str(tmp_path))


@patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, "q"))
@patch("shutil.which")
def test_query_failure_returns_1(mock_which, mock_run, tmp_path):
    mock_which.side_effect = which("graphify")
    assert gh.main(["--path", str(tmp_path), "--query", "x"]) == 1


@patch("subprocess.run")
@patch("shutil.which")
def test_hooks_exit_code(mock_which, mock_run, tmp_path):
    mock_which.side_effect = which("graphify")
    assert gh.main(["--path", str(tmp_path), "--hooks"]) == 0
    mock_run.side_effect = subprocess.CalledProcessError(1, "hooks")
    assert gh.main(["--path", str(tmp_path), "--hooks"]) == 1
