import calculate_complexity
import sync_matrix
from archon_core import read_text


def test_matrix_render_is_deterministic_and_current():
    first = sync_matrix.render_matrix(*sync_matrix.collect())
    second = sync_matrix.render_matrix(*sync_matrix.collect())
    assert first == second
    assert first == read_text(sync_matrix.MATRIX_PATH)


def test_matrix_has_one_diagram_with_undirected_edges():
    text = sync_matrix.render_matrix(*sync_matrix.collect())
    assert text.count("```mermaid") == 1
    assert " --> " not in text
    rows = [
        line for line in text.splitlines() if line.startswith("| ") and "From Persona" not in line
    ]
    edges = [line for line in text.splitlines() if " --- " in line]
    assert len(rows) == 2 * len(edges)


def test_check_and_write_modes(tmp_path, monkeypatch, capsys):
    target = tmp_path / "MATRIX.md"
    target.write_text("stale\n", encoding="utf-8")
    monkeypatch.setattr(sync_matrix, "MATRIX_PATH", str(target))
    assert sync_matrix.main(["--check"]) == 1
    assert sync_matrix.main([]) == 0
    assert "regenerated" in capsys.readouterr().out
    assert sync_matrix.main(["--check"]) == 0
    assert sync_matrix.main([]) == 0
    assert "already up to date" in capsys.readouterr().out


def test_level_legend():
    assert sync_matrix.level_legend() == (
        "Sparse (0–22) · Moderate (23–26) · Thorough (27–32) · Comprehensive (33+)"
    )


def test_complexity_report_and_gate(capsys):
    assert calculate_complexity.main([]) == 0
    out = capsys.readouterr().out
    assert "web_mobile_apps.md" in out and "Comprehensive" in out
    assert calculate_complexity.main(["--min-score", "1000"]) == 1
