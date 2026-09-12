"""Committed dist/ and docs/model/ equal a fresh build, and every schema passes the meta-schema.

The drift test catches a schema edited without rebuilding, or a generated file edited by hand.
The meta-schema test is skipped until the first module produces a dist/*.schema.json.
"""
from pathlib import Path
import json

import pytest
from jsonschema import Draft202012Validator

from test_build import build, make_tree

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = sorted(p.name for p in (ROOT / "dist").glob("*.schema.json"))


def tree_contents(folder: Path) -> dict[str, str]:
    """Committed-equivalent files only: dist/viewer/ is gitignored and never drift-tested."""
    return {
        p.relative_to(folder).as_posix(): p.read_text(encoding="utf-8")
        for p in folder.rglob("*")
        if p.is_file() and p.name != ".gitkeep" and p.relative_to(folder).parts[0] != "viewer"
    }


def test_committed_outputs_match_fresh_build(tmp_path: Path, root: Path) -> None:
    modules = [p.relative_to(root).as_posix() for p in sorted((root / "schema").glob("*.yaml"))]
    tree = make_tree(tmp_path, root, modules)
    result = build(tree)
    assert result.returncode == 0, result.stderr
    assert tree_contents(root / "dist") == tree_contents(tree / "dist")
    assert tree_contents(root / "docs" / "model") == tree_contents(tree / "docs" / "model")


@pytest.mark.parametrize("schema", SCHEMAS)
def test_schema_passes_metaschema(root: Path, schema: str) -> None:
    Draft202012Validator.check_schema(
        json.loads((root / "dist" / schema).read_text(encoding="utf-8"))
    )
