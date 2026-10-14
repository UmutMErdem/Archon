import detect_domain as dd
from archon_core import load_registry


def make(root, *paths):
    for p in paths:
        target = root / p
        if p.endswith("/"):
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("", encoding="utf-8")


def test_patterns():
    assert dd.patterns("`a.ini`, `*.ino`, HAL headers, `*.hex` / `*.bin`") == [
        "a.ini",
        "*.ino",
        "*.hex",
        "*.bin",
    ]


def test_embedded_project_with_supporting_domains(tmp_path, capsys):
    make(
        tmp_path,
        "platformio.ini",
        "src/main.ino",
        "src/util.ino",
        "hw/board.kicad_pcb",
        "Dockerfile",
        ".github/workflows/ci.yml",
        "firmware.hex",
        "node_modules/package.json",
    )
    assert dd.main([str(tmp_path)]) == 0
    out = capsys.readouterr().out
    assert "Tier 1: embedded_iot.md" in out
    assert "devops.md" in out.split("Tier 2:")[1]
    assert "hardware_design.md" in out.split("Tier 2:")[1]
    assert "web_mobile_apps.md" not in out


def test_weak_signals_never_select_tier1(tmp_path, capsys):
    make(tmp_path, "requirements.txt", "docs/", "data.csv")
    assert dd.main([str(tmp_path)]) == 0
    assert "No strong signal matched" in capsys.readouterr().out


def test_tie_asks_user(tmp_path, capsys):
    make(tmp_path, "contract.sol", "main.rs")
    dd.main([str(tmp_path)])
    assert "Tie for Tier 1" in capsys.readouterr().out


def test_tier2_limit_and_case_sensitivity(tmp_path):
    make(
        tmp_path,
        "a.ino",
        "b.ino",
        "c.ino",
        "x.kicad_pcb",
        "Dockerfile",
        "net.frr",
        "main.rs",
        "model.ipynb",
        "assets/",
    )
    registry = load_registry()
    tier1, tier2, rest = dd.assign_tiers(dd.score(str(tmp_path), registry), registry)
    assert tier1 == "embedded_iot.md"
    assert len(tier2) == 3 and len(rest) == 2
    assert "game_dev.md" not in tier2 + rest


def test_not_a_directory(tmp_path, capsys):
    assert dd.main([str(tmp_path / "missing")]) == 2
