import os
import shutil

import pytest

from archon_core import REPO_ROOT


@pytest.fixture
def repo_copy(tmp_path):
    """Copy of the manifesto data files (not scripts) that tests may mutate."""
    root = tmp_path / "archon"
    shutil.copytree(os.path.join(REPO_ROOT, "personas"), root / "personas")
    shutil.copytree(os.path.join(REPO_ROOT, "architecture"), root / "architecture")
    for name in (
        "README.md",
        "detection_signals.md",
        "compliance.md",
        "CROSS_DOMAIN_MATRIX.md",
        "PERSONA_TEMPLATE.md",
    ):
        shutil.copy(os.path.join(REPO_ROOT, name), root / name)
    return root
