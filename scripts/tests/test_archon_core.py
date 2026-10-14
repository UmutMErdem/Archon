import archon_core
from archon_core import (
    completeness,
    display_name,
    extract_section,
    iter_interfaces,
    load_registry,
    parse_frontmatter,
    resolve_domain_to_persona_file,
    section_bullets,
)

PERSONA = """---
domain: "AI / ML"
expert_role: "You are a Senior AI Engineer with expertise in ML."
tags: ["a", 'b']
inherits:
  base: "$primary"
  base_reason: "shared tooling"
  overrides: "model rules"
---
# AI / ML Persona

## Compliance & Standards
- EU AI Act (risk classification)
- IEEE 7000 — ethics

## Cross-Domain Interfaces
- **→ DevOps:** MLOps pipeline
- **→ Data Engineering**: feature store
not a bullet
"""


def test_parse_frontmatter_scalars_lists_and_nested_block():
    meta, err = parse_frontmatter(PERSONA)
    assert err is None
    assert meta["domain"] == "AI / ML"
    assert meta["tags"] == ["a", "b"]
    assert meta["inherits"] == {
        "base": "$primary",
        "base_reason": "shared tooling",
        "overrides": "model rules",
    }


def test_parse_frontmatter_errors():
    assert parse_frontmatter("domain: x\n")[1].startswith("Missing frontmatter start")
    assert parse_frontmatter("---\ndomain: x\n")[1].startswith("Missing frontmatter end")


def test_sections_bullets_and_interfaces():
    assert "EU AI Act" in extract_section(PERSONA, "## Compliance & Standards")
    assert extract_section(PERSONA, "## Missing") is None
    assert section_bullets(PERSONA, "## Compliance & Standards") == [
        "EU AI Act (risk classification)",
        "IEEE 7000 — ethics",
    ]
    assert iter_interfaces(PERSONA) == [
        ("DevOps", "MLOps pipeline"),
        ("Data Engineering", "feature store"),
    ]


def test_completeness_levels():
    s = completeness(PERSONA)
    assert (s["sections"], s["interfaces"], s["compliance"]) == (2, 2, 2)
    assert s["score"] == 6 and s["label"] == "Sparse"


def test_registry_has_unique_labels_for_every_persona():
    registry = load_registry()
    assert set(registry) == set(archon_core.list_persona_files())
    labels = [row["label"] for row in registry.values()]
    assert len(labels) == len(set(labels))


def test_resolver_is_strict_on_real_registry():
    registry = load_registry()
    assert resolve_domain_to_persona_file("FPGA", registry) == "fpga_digital.md"
    assert resolve_domain_to_persona_file("QA/Testing", registry) == "qa_testing.md"
    assert resolve_domain_to_persona_file("Embedded Systems / IoT", registry) == "embedded_iot.md"
    assert resolve_domain_to_persona_file("db_architect", registry) == "db_architect.md"
    for loose in ("Testing", "Security", "Cloud", "Data", "Design", "Compliance"):
        assert resolve_domain_to_persona_file(loose, registry) is None


def test_load_registry_missing_file(tmp_path):
    assert load_registry(str(tmp_path / "none.md")) == {}


def test_display_name_fallback():
    registry = {"ai_ml.md": {"label": "AI/ML"}}
    assert display_name("ai_ml.md", registry) == "AI/ML"
    assert display_name("new_thing.md", registry) == "New Thing"
