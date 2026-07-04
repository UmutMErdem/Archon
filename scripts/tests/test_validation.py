import os
import sys

# Add parent directory to path to import validate_manifesto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from validate_manifesto import (
    parse_frontmatter,
    check_frontmatter_body_consistency,
    check_persona_size,
    MIN_PERSONA_LINES,
    MAX_PERSONA_LINES,
)


def test_parse_frontmatter_valid():
    content = """---
domain: "AI / ML"
expert_role: "You are a Senior AI/ML Engineer with expertise in deep learning"
recommended_tools: ["TensorFlow", "PyTorch"]
compliance: ["ISO 42001"]
---
# AI / ML Persona
"""
    meta, error = parse_frontmatter(content)
    assert error is None
    assert meta["domain"] == "AI / ML"
    assert (
        meta["expert_role"]
        == "You are a Senior AI/ML Engineer with expertise in deep learning"
    )
    assert meta["recommended_tools"] == ["TensorFlow", "PyTorch"]
    assert meta["compliance"] == ["ISO 42001"]


def test_parse_frontmatter_invalid():
    # Missing frontmatter start
    content1 = "domain: AI\n---\n"
    meta1, error1 = parse_frontmatter(content1)
    assert meta1 is None
    assert "Missing frontmatter start marker" in error1

    # Missing frontmatter end
    content2 = "---\ndomain: AI\n"
    meta2, error2 = parse_frontmatter(content2)
    assert meta2 is None
    assert "Missing frontmatter end marker" in error2


def test_check_frontmatter_body_consistency_valid(tmp_path):
    persona = tmp_path / "valid_persona.md"
    persona.write_text(
        """---
domain: "Embedded IoT"
expert_role: "You are a Senior Embedded Systems Engineer"
recommended_tools: []
compliance: []
---
# Embedded IoT Persona

## Expert Role
> You are a **Senior Embedded Systems Engineer** with expertise in RTOS...
""",
        encoding="utf-8",
    )

    errors = check_frontmatter_body_consistency(str(persona))
    assert errors == []


def test_check_frontmatter_body_consistency_invalid_role(tmp_path):
    persona = tmp_path / "invalid_role.md"
    # expert_role in frontmatter is "Senior Embedded Systems Engineer"
    # but heading body is "Principal Game Developer"
    persona.write_text(
        """---
domain: "Embedded IoT"
expert_role: "You are a Senior Embedded Systems Engineer"
recommended_tools: []
compliance: []
---
# Embedded IoT Persona

## Expert Role
> You are a **Principal Game Developer** with expertise in Unity...
""",
        encoding="utf-8",
    )

    errors = check_frontmatter_body_consistency(str(persona))
    assert len(errors) > 0
    assert any("does not contain body Expert Role title" in e for e in errors)


def test_check_frontmatter_body_consistency_invalid_domain(tmp_path):
    persona = tmp_path / "invalid_domain.md"
    # domain in frontmatter is "Cybersecurity"
    # but heading is "# Game Development Persona"
    persona.write_text(
        """---
domain: "Cybersecurity"
expert_role: "You are a Security Specialist"
recommended_tools: []
compliance: []
---
# Game Development Persona

## Expert Role
> You are a **Security Specialist**
""",
        encoding="utf-8",
    )

    errors = check_frontmatter_body_consistency(str(persona))
    assert len(errors) > 0
    assert any("does not match heading" in e for e in errors)


def test_check_persona_size(tmp_path):
    # Too short
    short_file = tmp_path / "short.md"
    short_file.write_text("\n" * (MIN_PERSONA_LINES - 5), encoding="utf-8")
    warnings = check_persona_size(str(short_file))
    assert len(warnings) == 1
    assert "Too short" in warnings[0]

    # OK size
    ok_file = tmp_path / "ok.md"
    ok_file.write_text("\n" * (MIN_PERSONA_LINES + 5), encoding="utf-8")
    warnings = check_persona_size(str(ok_file))
    assert len(warnings) == 0

    # Too long
    long_file = tmp_path / "long.md"
    long_file.write_text("\n" * (MAX_PERSONA_LINES + 5), encoding="utf-8")
    warnings = check_persona_size(str(long_file))
    assert len(warnings) == 1
    assert "Too long" in warnings[0]
