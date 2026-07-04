import os
import sys
from unittest.mock import patch, MagicMock

# Add parent directory to path to import graphify_helper
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import graphify_helper


def test_is_graphify_installed_present():
    with patch("shutil.which", return_value="/usr/local/bin/graphify"):
        assert graphify_helper.is_graphify_installed() is True


def test_is_graphify_installed_missing():
    with patch("shutil.which", return_value=None):
        assert graphify_helper.is_graphify_installed() is False


@patch("subprocess.run")
@patch("shutil.which")
def test_install_graphify_with_uv(mock_which, mock_run):
    # Simulate uv exists, pip fallback not needed
    mock_which.side_effect = lambda cmd: "/usr/bin/uv" if cmd == "uv" else None
    mock_run.return_value = MagicMock(returncode=0)

    success = graphify_helper.install_graphify()
    assert success is True
    mock_run.assert_called_once_with(
        ["uv", "tool", "install", "graphifyy", "--with", "matplotlib"], check=True
    )


@patch("subprocess.run")
@patch("shutil.which")
def test_install_graphify_pip_fallback(mock_which, mock_run):
    # Simulate uv is missing
    mock_which.return_value = None
    mock_run.return_value = MagicMock(returncode=0)

    success = graphify_helper.install_graphify()
    assert success is True
    mock_run.assert_called_once_with(
        [sys.executable, "-m", "pip", "install", "graphifyy", "matplotlib"], check=True
    )


@patch("subprocess.run")
@patch("shutil.which")
@patch("sys.exit")
def test_main_build_command(mock_exit, mock_which, mock_run):
    # Simulate graphify already installed
    mock_which.side_effect = lambda cmd: (
        "/usr/local/bin/graphify" if cmd == "graphify" else None
    )
    mock_run.return_value = MagicMock(returncode=0)

    # Mock command line arguments
    test_args = ["graphify_helper.py", "--path", "/dummy/project", "--build"]
    with patch("sys.argv", test_args):
        graphify_helper.main()

    abs_path = os.path.abspath("/dummy/project")
    # Check that subprocess.run was called with correct extract, cluster, and export commands
    mock_run.assert_any_call(["graphify", abs_path], check=True)
    mock_run.assert_any_call(
        ["graphify", "cluster-only", abs_path, "--no-label"], check=True
    )
    mock_run.assert_any_call(
        [
            "graphify",
            "export",
            "svg",
            "--graph",
            os.path.join(abs_path, "graphify-out", "graph.json"),
        ],
        check=True,
    )


@patch("subprocess.run")
@patch("shutil.which")
@patch("sys.exit")
@patch("os.chdir")
def test_main_query_command(mock_chdir, mock_exit, mock_which, mock_run):
    mock_which.side_effect = lambda cmd: (
        "/usr/local/bin/graphify" if cmd == "graphify" else None
    )
    mock_run.return_value = MagicMock(returncode=0)

    test_args = [
        "graphify_helper.py",
        "--path",
        "/dummy/project",
        "--query",
        "What are the dependencies?",
    ]
    with patch("sys.argv", test_args):
        graphify_helper.main()

    expected_cmd = ["graphify", "query", "What are the dependencies?"]
    mock_run.assert_called_with(expected_cmd, check=True)
