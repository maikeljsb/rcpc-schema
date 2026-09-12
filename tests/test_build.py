"""One test per rule of scripts/build.py as specified in SPEC-toolchain.md.

Each test copies the build script and a chosen set of modules into a temporary
tree laid out like the repository, runs the script there, and inspects the
outputs. The committed dist/ and docs/model/ are never touched.
"""
from pathlib import Path
import json
import shutil
import subprocess
import sys

import pytest
from jsonschema import Draft202012Validator

FIXTURE = "tests/fixtures/minimal.yaml"
IMPORTER = "tests/fixtures/importer.yaml"
DRAFT = "https://json-schema.org/draft/2020-12/schema"


def make_tree(tmp_path: Path, root: Path, modules: list[str]) -> Path:
    """Lay out scripts/, schema/, dist/, docs/model/ under tmp_path and return it."""
    (tmp_path / "scripts").mkdir()
    shutil.copy(root / "scripts" / "build.py", tmp_path / "scripts" / "build.py")
    (tmp_path / "schema").mkdir()
    for module in modules:
        shutil.copy(root / module, tmp_path / "schema" / Path(module).name)
    (tmp_path / "dist").mkdir()
    (tmp_path / "docs" / "model").mkdir(parents=True)
    (tmp_path / "docs" / "model" / ".gitkeep").touch()
    return tmp_path


def build(tree: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(tree / "scripts" / "build.py"), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def test_fixture_produces_2020_12(tmp_path: Path, root: Path) -> None:
    tree = make_tree(tmp_path, root, [FIXTURE])
    result = build(tree)
    assert result.returncode == 0, result.stderr
    schema = json.loads((tree / "dist" / "minimal.schema.json").read_text(encoding="utf-8"))
    assert schema["$schema"] == DRAFT


def test_fixture_passes_metaschema(tmp_path: Path, root: Path) -> None:
    tree = make_tree(tmp_path, root, [FIXTURE])
    assert build(tree).returncode == 0
    schema = json.loads((tree / "dist" / "minimal.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)


def test_fixture_docs_generated(tmp_path: Path, root: Path) -> None:
    tree = make_tree(tmp_path, root, [FIXTURE])
    assert build(tree).returncode == 0
    assert (tree / "docs" / "model" / "minimal" / "index.md").is_file()


def test_readme_lists_modules(tmp_path: Path, root: Path) -> None:
    tree = make_tree(tmp_path, root, [FIXTURE])
    assert build(tree).returncode == 0
    readme = (tree / "dist" / "README.md").read_text(encoding="utf-8")
    assert "minimal.schema.json" in readme
    assert "A three-class fixture" in readme
    assert "2020-12" in readme


def test_stale_outputs_removed(tmp_path: Path, root: Path) -> None:
    tree = make_tree(tmp_path, root, [FIXTURE])
    (tree / "dist" / "ghost.schema.json").write_text("{}", encoding="utf-8")
    (tree / "docs" / "model" / "ghost").mkdir()
    (tree / "docs" / "model" / "ghost" / "index.md").write_text("stale", encoding="utf-8")
    (tree / "docs" / "model" / "minimal").mkdir()
    (tree / "docs" / "model" / "minimal" / "removed_slot.md").write_text("stale", encoding="utf-8")
    assert build(tree).returncode == 0
    assert not (tree / "dist" / "ghost.schema.json").exists()
    assert not (tree / "docs" / "model" / "ghost").exists()
    assert not (tree / "docs" / "model" / "minimal" / "removed_slot.md").exists()
    assert (tree / "docs" / "model" / "minimal" / "index.md").is_file()
    assert (tree / "dist" / "minimal.schema.json").is_file()


def test_empty_schema_is_noop(tmp_path: Path, root: Path) -> None:
    tree = make_tree(tmp_path, root, [])
    result = build(tree)
    assert result.returncode == 0, result.stderr
    assert sorted(p.name for p in (tree / "dist").iterdir()) == ["README.md"]
    assert "no modules" in (tree / "dist" / "README.md").read_text(encoding="utf-8").lower()
    assert sorted(p.name for p in (tree / "docs" / "model").iterdir()) == [".gitkeep"]


def test_viewer_schemas_on_by_default(tmp_path: Path, root: Path) -> None:
    tree = make_tree(tmp_path, root, [FIXTURE, IMPORTER])
    assert build(tree).returncode == 0
    assert (tree / "dist" / "viewer" / "minimal.schema.json").is_file()
    assert (tree / "dist" / "viewer" / "importer.schema.json").is_file()


def test_viewer_schemas_opt_out(tmp_path: Path, root: Path) -> None:
    tree = make_tree(tmp_path, root, [FIXTURE, IMPORTER])
    assert build(tree, "--no-viewer-schemas").returncode == 0
    assert not (tree / "dist" / "viewer").exists()


def test_viewer_schemas_splits_defs(tmp_path: Path, root: Path) -> None:
    tree = make_tree(tmp_path, root, [FIXTURE, IMPORTER])
    result = build(tree)
    assert result.returncode == 0, result.stderr
    linked = json.loads((tree / "dist" / "viewer" / "importer.schema.json").read_text(encoding="utf-8"))
    assert set(linked["$defs"]) == {"Crate"}
    dimensions = linked["$defs"]["Crate"]["properties"]["dimensions"]
    ref = next(branch["$ref"] for branch in dimensions["anyOf"] if "$ref" in branch)
    assert ref == "minimal.schema.json#/$defs/Dimensions"


def test_viewer_schemas_noop_module(tmp_path: Path, root: Path) -> None:
    tree = make_tree(tmp_path, root, [FIXTURE, IMPORTER])
    assert build(tree).returncode == 0
    plain = (tree / "dist" / "minimal.schema.json").read_text(encoding="utf-8")
    linked = (tree / "dist" / "viewer" / "minimal.schema.json").read_text(encoding="utf-8")
    assert plain == linked


def test_viewer_schemas_readme_written(tmp_path: Path, root: Path) -> None:
    tree = make_tree(tmp_path, root, [FIXTURE, IMPORTER])
    assert build(tree).returncode == 0
    readme = (tree / "dist" / "viewer" / "README.md").read_text(encoding="utf-8")
    assert "not committed" in readme.lower()
    assert "$ref" in readme


def test_viewer_schemas_resolves_end_to_end(tmp_path: Path, root: Path) -> None:
    from referencing import Registry, Resource

    tree = make_tree(tmp_path, root, [FIXTURE, IMPORTER])
    assert build(tree).returncode == 0
    minimal = json.loads((tree / "dist" / "viewer" / "minimal.schema.json").read_text(encoding="utf-8"))
    importer = json.loads((tree / "dist" / "viewer" / "importer.schema.json").read_text(encoding="utf-8"))

    registry = Registry().with_resources([
        ("minimal.schema.json", Resource.from_contents(minimal)),
        ("importer.schema.json", Resource.from_contents(importer)),
    ])
    validator = Draft202012Validator(schema=importer["$defs"]["Crate"], registry=registry)

    validator.validate({"id": "c1", "dimensions": {"width": 1.0, "height": 2.0}})

    with pytest.raises(Exception):
        validator.validate({"id": "c1", "dimensions": {"width": 1.0}})
