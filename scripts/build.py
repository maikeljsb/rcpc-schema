"""Regenerate dist/ and docs/model/ from every LinkML module under schema/.

Rules in SPEC-toolchain.md: one draft 2020-12 JSON Schema per module, docs per module,
a generated dist/README.md, stale outputs removed, empty schema/ is a no-op, fail fast.
"""
from pathlib import Path
import json, shutil, subprocess, sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCHEMA, DIST, DOCS = ROOT / "schema", ROOT / "dist", ROOT / "docs" / "model"
DRAFT = "https://json-schema.org/draft/2020-12/schema"


def run(*args: str) -> str:
    return subprocess.run(args, check=True, capture_output=True, text=True, encoding="utf-8").stdout


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def build(module: Path) -> str:
    """Emit the module's JSON Schema and docs; return its description for the README."""
    schema = json.loads(run("gen-json-schema", str(module)))
    schema["$schema"] = DRAFT
    write(DIST / f"{module.stem}.schema.json", json.dumps(schema, indent=2) + "\n")
    shutil.rmtree(DOCS / module.stem, ignore_errors=True)
    run("gen-doc", "--no-mergeimports", "-d", str(DOCS / module.stem), str(module))
    return str(yaml.safe_load(module.read_text(encoding="utf-8")).get("description", "")).strip()


def remove_stale(keep: set[str]) -> None:
    for stale in DIST.glob("*.schema.json"):
        if stale.name.removesuffix(".schema.json") not in keep:
            stale.unlink()
    for stale in (d for d in DOCS.iterdir() if d.is_dir() and d.name not in keep):
        shutil.rmtree(stale)


def main() -> int:
    modules = sorted(SCHEMA.glob("*.yaml"))
    DIST.mkdir(exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    lines = ["# Generated schemas", "", "Generated from `schema/` by `uv run python scripts/build.py`. Do not edit.", ""]
    lines += [f"- `{m.stem}.schema.json` (JSON Schema draft 2020-12): {build(m)}" for m in modules]
    lines += ["No modules exist under `schema/` yet."] if not modules else []
    remove_stale({m.stem for m in modules})
    write(DIST / "README.md", "\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except subprocess.CalledProcessError as failure:
        sys.stderr.write(failure.stderr or failure.stdout)
        sys.exit(failure.returncode or 1)
