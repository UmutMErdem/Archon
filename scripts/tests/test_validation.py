import os

import validate_manifesto as vm
from archon_core import load_registry

GOOD_PERSONA = """---
domain: "Embedded IoT"
expert_role: "You are a Senior Embedded Systems Engineer with expertise in RTOS."
inherits: "none"
---
# Embedded IoT Persona

## Expert Role
> You are a **Senior Embedded Systems Engineer** with expertise in RTOS.
"""


def test_real_repository_is_clean():
    errors, _ = vm.run()
    assert errors == []
    assert vm.main([]) == 0


def test_compliance_key_and_ids():
    assert vm.compliance_key("ISO/IEC 27001 (security) x") == "ISO/IEC 27001"
    assert vm.compliance_key("IEEE 7000 — ethics") == "IEEE 7000"
    assert vm.split_ids("ISO/IEC 27001 / ISO/IEC 27002") == ["ISO/IEC 27001", "ISO/IEC 27002"]
    ids = vm.canonical_compliance_ids(
        "| Standard | Scope |\n|---|---|\n| NIST SP 800-53 | x |\n| SOX (Sarbanes-Oxley) | y |\n| GDPR / CCPA | z |\n"
    )
    assert {"NIST SP 800-53", "SOX", "GDPR", "CCPA", "GDPR / CCPA"} <= ids
    assert "Standard" not in ids


def test_check_compliance_ids_flags_name_drift():
    ids = {"NIST SP 800-53", "CIS Benchmarks"}
    content = "## Compliance & Standards\n- NIST 800-53 (controls)\n- NIST SP 800-53 / CIS Benchmarks (ok)\n"
    assert vm.check_compliance_ids(content, ids) == [
        "Compliance ID 'NIST 800-53' not found in compliance.md column 1"
    ]


def test_template_integrity():
    errors = vm.check_template_integrity(GOOD_PERSONA)
    assert "Missing required heading: '## Cross-Domain Interfaces'" in errors
    assert not any("Frontmatter" in e for e in errors)
    assert vm.check_template_integrity("no frontmatter") == [
        "Frontmatter error: Missing frontmatter start marker '---'"
    ]
    empty = GOOD_PERSONA.replace('domain: "Embedded IoT"', 'domain: ""')
    assert "Frontmatter key 'domain' is empty" in vm.check_template_integrity(empty)


def test_check_inherits():
    files = ["web.md"]
    block = '---\ninherits:\n  base: "{}"\n  base_reason: "r"\n  overrides: "{}"\n---\n'
    assert vm.check_inherits(block.format("web.md", "o"), files) == []
    assert vm.check_inherits(block.format("$primary", "o"), files) == []
    assert vm.check_inherits(block.format("gone.md", "o"), files) == [
        "inherits.base 'gone.md' does not exist in personas/"
    ]
    assert vm.check_inherits(block.format("web.md", ""), files) == [
        "inherits.overrides is missing or empty"
    ]
    assert vm.check_inherits('---\ninherits: "maybe"\n---\n', files)
    assert vm.check_inherits(GOOD_PERSONA, files) == []


def test_check_placeholders():
    assert vm.check_placeholders("- **→ <Other Domain>:** x\n- latency < 200 ms") == [
        "Unfilled placeholder '<Other Domain>'"
    ]


def test_frontmatter_body_consistency():
    assert vm.check_frontmatter_body_consistency(GOOD_PERSONA) == []
    bad_role = GOOD_PERSONA.replace("**Senior Embedded Systems Engineer**", "**Game Developer**")
    assert any(
        "does not contain body Expert Role title" in e
        for e in vm.check_frontmatter_body_consistency(bad_role)
    )
    bad_domain = GOOD_PERSONA.replace("# Embedded IoT Persona", "# Game Development Persona")
    assert any(
        "does not match heading" in e for e in vm.check_frontmatter_body_consistency(bad_domain)
    )


def test_check_persona_size(tmp_path):
    short = tmp_path / "short.md"
    short.write_text("\n" * (vm.MIN_PERSONA_LINES - 5), encoding="utf-8")
    long = tmp_path / "long.md"
    long.write_text("\n" * (vm.MAX_PERSONA_LINES + 5), encoding="utf-8")
    ok = tmp_path / "ok.md"
    ok.write_text("\n" * (vm.MIN_PERSONA_LINES + 5), encoding="utf-8")
    assert "Too short" in vm.check_persona_size(str(short))[0]
    assert "Too long" in vm.check_persona_size(str(long))[0]
    assert vm.check_persona_size(str(ok)) == []


def _registry(**labels):
    return {
        f: {"label": lab, "domain": lab, "signals": "", "weak": ""} for f, lab in labels.items()
    }


def test_check_interfaces_label_symmetry_duplicates_self():
    registry = _registry(**{"a.md": "Alpha", "b.md": "Beta", "c.md": "Gamma"})
    contents = {
        "a.md": "## Cross-Domain Interfaces\n- **→ Beta:** x\n- **→ b:** dup\n- **→ Alpha:** me\n- **→ Nope:** ?\n",
        "b.md": "## Cross-Domain Interfaces\n- **→ Gamma:** y\n",
        "c.md": "## Cross-Domain Interfaces\n- **→ Beta:** z\n",
    }
    errors = vm.check_interfaces(contents, registry)
    assert "UNRESOLVED: a.md: interface target 'Nope' matches no persona" in errors
    assert "LABEL: a.md: 'b' is not canonical, use 'Beta'" in errors
    assert "SELF: a.md: interface points to itself" in errors
    assert "DUPLICATE: a.md: 2 bullets point to b.md, merge them" in errors
    assert any(e.startswith("ASYMMETRY: a.md → b.md") for e in errors)
    assert not any("b.md → c.md" in e for e in errors)


def test_signal_collisions():
    registry = {
        "x.md": {"signals": "`openapi.yaml`, `*.proto`", "weak": "—"},
        "y.md": {"signals": "k8s `*.yaml`", "weak": "`*.proto`"},
        "z.md": {"signals": "`.github/workflows/*sec*`", "weak": "—"},
        "w.md": {"signals": "`.github/workflows/sec.yml`", "weak": "—"},
    }
    errors = vm.check_signal_collisions(registry)
    assert "Signal '*.proto' (personas/x.md) overlaps '*.proto' (personas/y.md)" in errors
    assert any("sec.yml" in e for e in errors)
    assert not any("openapi.yaml" in e for e in errors)


def test_check_registry_detects_unregistered_and_drift(repo_copy, monkeypatch):
    monkeypatch.setattr(vm, "README_PATH", str(repo_copy / "README.md"))
    monkeypatch.setattr(vm, "DETECTION_PATH", str(repo_copy / "architecture" / "00_detection.md"))
    registry = load_registry(str(repo_copy / "detection_signals.md"))
    files = sorted(registry)
    assert vm.check_registry(registry, files) == []

    errors = vm.check_registry(registry, files + ["quantum.md"])
    assert "personas/quantum.md is not registered in detection_signals.md" in errors
    assert "personas/quantum.md is not listed in README.md" in errors
    assert "README.md persona count is not '(28 personas)'" in errors

    registry["ai_ml.md"]["label"] = "DevOps"
    errors = vm.check_registry(registry, files)
    assert "detection_signals.md: interface label 'DevOps' is used by 2 personas" in errors


def test_matrix_sync_detects_stale_file(tmp_path, monkeypatch):
    stale = tmp_path / "MATRIX.md"
    stale.write_text("# old\n", encoding="utf-8")
    monkeypatch.setattr(vm, "MATRIX_PATH", str(stale))
    assert vm.check_matrix_sync() == [
        "CROSS_DOMAIN_MATRIX.md is stale. Run: python scripts/sync_matrix.py"
    ]


def test_heading_slugs_match_github():
    md = "# Title\n## Step 3 — Discovery Questions\n## Dup\n## Dup\n```\n# not a heading\n```\n"
    assert vm.heading_slugs(md) == {"title", "step-3--discovery-questions", "dup", "dup-1"}


def test_broken_links(tmp_path):
    (tmp_path / "b.md").write_text("# Real Heading\n", encoding="utf-8")
    a = tmp_path / "a.md"
    a.write_text(
        "[ok](b.md) [anchor](b.md#real-heading) [bad anchor](b.md#nope) [gone](c.md)\n"
        "[web](https://example.com) [local](file:///D:/x.md) `[code](ignored.md)`\n"
        "```\n[fenced](ignored.md)\n```\n[self](#missing)\n",
        encoding="utf-8",
    )
    errors = vm.check_broken_links([str(a)])
    assert len(errors) == 4
    assert any("broken anchor 'b.md#nope'" in e for e in errors)
    assert any("broken link 'c.md'" in e for e in errors)
    assert any("machine-specific link" in e for e in errors)
    assert any("broken anchor '#missing'" in e for e in errors)


def test_markdown_files_skip_generated_dirs():
    files = [os.path.relpath(f, vm.REPO_ROOT).replace(os.sep, "/") for f in vm._markdown_files()]
    assert "README.md" in files
    assert not any(f.startswith(("graphify-out/", ".arena/")) for f in files)


def test_main_reports_errors(monkeypatch, capsys):
    monkeypatch.setattr(vm, "run", lambda: ([("LINK", "x.md: broken link 'y'")], [("SIZE", "w")]))
    assert vm.main([]) == 1
    out = capsys.readouterr().out
    assert "LINK=1" in out and "SIZE: w" in out
