import io
import sys
from unittest.mock import MagicMock, patch

import pytest

import create_persona as cp
from archon_core import parse_frontmatter

ARGS = [
    "--domain",
    'Quantum "Computing"',
    "--filename",
    "quantum_computing",
    "--label",
    "Quantum",
    "--role",
    "Senior Quantum Software Engineer",
    "--expertise",
    "circuit design and error mitigation",
    "--signals",
    "`*.qasm`",
    "--interfaces",
    "AI/ML, DevOps",
]


@pytest.fixture
def repo(repo_copy, monkeypatch):
    for name, rel in (
        ("PERSONAS_DIR", "personas"),
        ("SIGNALS_PATH", "detection_signals.md"),
        ("README_PATH", "README.md"),
        ("DETECTION_PATH", "architecture/00_detection.md"),
        ("TEMPLATE_PATH", "PERSONA_TEMPLATE.md"),
    ):
        monkeypatch.setattr(cp, name, str(repo_copy / rel))
    monkeypatch.setattr(cp, "REPO_ROOT", str(repo_copy))
    return repo_copy


@patch("subprocess.run", return_value=MagicMock(returncode=1))
def test_creates_and_registers_persona(mock_run, repo):
    assert cp.main(ARGS) == 1  # the draft still has placeholders, so validation fails
    text = (repo / "personas" / "quantum_computing.md").read_text(encoding="utf-8")
    meta, err = parse_frontmatter(text)
    assert err is None
    assert meta["domain"] == 'Quantum \\"Computing\\"'
    assert '# Quantum "Computing" Persona' in text
    assert "HOW TO USE THIS TEMPLATE" not in text
    assert text.count("with expertise in circuit design") == 2
    assert "- **→ AI/ML:**" in text and "- **→ DevOps:**" in text
    assert "<Interface Label>" not in text

    signals = (repo / "detection_signals.md").read_text(encoding="utf-8")
    assert (
        '| `*.qasm` | Quantum "Computing" | `personas/quantum_computing.md` | Quantum | — |'
        in signals
    )
    readme = (repo / "README.md").read_text(encoding="utf-8")
    assert "[quantum_computing.md](personas/quantum_computing.md)" in readme
    assert "Domain Expert Personas (31 personas)" in readme
    detection = (repo / "architecture" / "00_detection.md").read_text(encoding="utf-8")
    assert 'Medical Devices, Quantum)"' in detection
    assert "#### Detection Signals (auto-detect before asking)\n" in detection
    assert mock_run.call_args[0][0][0] == sys.executable


@patch("subprocess.run", return_value=MagicMock(returncode=0))
def test_second_registration_only_touches_domain_line(mock_run, repo):
    assert cp.main(ARGS) == 0
    detection_path = repo / "architecture" / "00_detection.md"
    before = detection_path.read_text(encoding="utf-8").splitlines()
    second = list(ARGS)
    second[second.index("quantum_computing")] = "bio_informatics"
    second[second.index("Quantum")] = "Bio"
    assert cp.main(second) == 0
    after = detection_path.read_text(encoding="utf-8").splitlines()
    changed = [i for i, (a, b) in enumerate(zip(before, after, strict=True)) if a != b]
    assert len(changed) == 1 and after[changed[0]].endswith('Quantum, Bio)"')


@patch("subprocess.run", return_value=MagicMock(returncode=0))
@pytest.mark.parametrize(
    "flag,value,message",
    [
        ("--filename", "../README.md", "must match"),
        ("--label", "DevOps", "already used"),
        ("--interfaces", "Cloud", "unknown interface labels"),
        ("--signals", "config files", "backticked"),
        ("--role", "", "--role must not be empty"),
    ],
)
def test_rejects_bad_input(mock_run, repo, capsys, flag, value, message):
    args = list(ARGS)
    args[args.index(flag) + 1] = value
    assert cp.main(args) == 2
    assert message in capsys.readouterr().out
    assert not (repo / "README.md.md").exists()
    mock_run.assert_not_called()


@patch("subprocess.run", return_value=MagicMock(returncode=0))
def test_existing_file_needs_force(mock_run, repo, capsys):
    args = list(ARGS)
    args[args.index("quantum_computing")] = "devops"
    assert cp.main(args) == 2
    assert "already exists" in capsys.readouterr().out


def test_registration_is_idempotent_and_reports_missing_anchor():
    md = '> "What is the technical domain of this project? (e.g., A, B)"\n'
    once, changed = cp.register_detection(md, "C")
    assert changed is True and once.endswith('A, B, C)"\n')
    assert cp.register_detection(once, "C") == (once, False)
    assert cp.register_detection("no question here", "C") == ("no question here", None)
    assert cp.register_readme("nothing", "x.md") == ("nothing", None)


@patch("subprocess.run", return_value=MagicMock(returncode=0))
def test_interactive_prompts(mock_run, repo, monkeypatch):
    answers = "Quantum\nquantum.md\nQuantum\nSenior Engineer\nqubits\n`*.qasm`\nAI/ML\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(answers))
    assert cp.main([]) == 0
    assert (repo / "personas" / "quantum.md").exists()


def test_yaml_str_escapes_quotes():
    assert cp.yaml_str('a "b"') == '"a \\"b\\""'
