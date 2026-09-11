"""Every LinkML module under schema/ lints clean. Skips when no module exists yet."""
from pathlib import Path
import subprocess

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULES = sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / "schema").glob("*.yaml"))


@pytest.mark.parametrize("module", MODULES)
def test_module_lints_clean(root: Path, module: str) -> None:
    result = subprocess.run(
        ["linkml-lint", str(root / module)], capture_output=True, text=True, encoding="utf-8"
    )
    assert result.returncode == 0, result.stdout + result.stderr
