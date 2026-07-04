import os
import sys

# Add parent directory to path to import domain_utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from domain_utils import (
    load_domain_mappings,
    resolve_domain_to_persona_file,
)


def test_load_domain_mappings_empty_or_missing(tmp_path):
    # Test with non-existent file
    missing_file = tmp_path / "non_existent.md"
    assert load_domain_mappings(str(missing_file)) == {}


def test_load_domain_mappings_parsing(tmp_path):
    # Create a dummy signals file with 4 columns matching detection_signals.md
    signals_file = tmp_path / "detection_signals.md"
    signals_file.write_text(
        """
| Signals | Domain | Persona File | Complexity |
|---|---|---|---|
| `*.ipynb` | AI/ML | `personas/ai_ml.md` | 23 |
| `*.js` | Web / Mobile Apps | `personas/web_mobile_apps.md` | 38 |
| `*.invalid` | Invalid Line | no_ticks | 10 |
""",
        encoding="utf-8",
    )

    mappings = load_domain_mappings(str(signals_file))
    assert mappings == {
        "ai_ml.md": "AI/ML",
        "web_mobile_apps.md": "Web / Mobile Apps",
    }


def test_resolve_domain_to_persona_file_overrides():
    mappings = {}
    # Test canonical override keys
    assert resolve_domain_to_persona_file("ar", mappings) == "ar_vr_xr.md"
    assert resolve_domain_to_persona_file("embedded/iot", mappings) == "embedded_iot.md"
    assert (
        resolve_domain_to_persona_file("cloud architecture", mappings)
        == "cloud_architecture.md"
    )


def test_resolve_domain_to_persona_file_mappings_match():
    mappings = {
        "embedded_iot.md": "Embedded / IoT",
        "ai_ml.md": "AI/ML",
        "systems_programming.md": "Systems Programming",
    }

    # Exact match normalized
    assert resolve_domain_to_persona_file("embedded/iot", mappings) == "embedded_iot.md"
    assert resolve_domain_to_persona_file("AI & ML", mappings) == "ai_ml.md"
    assert (
        resolve_domain_to_persona_file("Systems-Programming", mappings)
        == "systems_programming.md"
    )


def test_resolve_domain_to_persona_file_base_filename():
    mappings = {
        "embedded_iot.md": "Embedded / IoT",
        "systems_programming.md": "Systems Programming",
    }
    # Match by base filename without symbols
    assert (
        resolve_domain_to_persona_file("systems_programming", mappings)
        == "systems_programming.md"
    )
    assert (
        resolve_domain_to_persona_file("systemsprogramming", mappings)
        == "systems_programming.md"
    )


def test_resolve_domain_to_persona_file_parts_match():
    mappings = {
        "qa_testing.md": "QA / Testing / Automation",
    }
    assert resolve_domain_to_persona_file("QA", mappings) == "qa_testing.md"
    assert resolve_domain_to_persona_file("Testing", mappings) == "qa_testing.md"


def test_resolve_domain_to_persona_file_substring_and_fallback():
    mappings = {
        "automation.md": "Industrial Automation",
        "qa_testing.md": "QA / Test Automation",
        "db_architect.md": "Database Architect",
    }
    # Test safety checks
    assert resolve_domain_to_persona_file("automation", mappings) == "automation.md"
    assert resolve_domain_to_persona_file("qa", mappings) == "qa_testing.md"
    assert resolve_domain_to_persona_file("db", mappings) == "db_architect.md"

    # Fallback substring match
    assert resolve_domain_to_persona_file("architect", mappings) == "db_architect.md"
    assert resolve_domain_to_persona_file("unknown", mappings) is None
