# Spec: toolchain

*Module `toolchain` of `CAPABILITY-MAP.md`. Approved 2026-09-10. Depends on nothing; every other module depends on it.*

## Objective

Give the repository one command that a person on another team can run on a clean clone and see every test pass, and one command that turns whatever LinkML modules exist under `schema/` into the artifacts the contract promises: one JSON Schema per module in draft 2020-12 for the schema viewer, and generated documentation per module. Continuous integration runs the same commands on every push.

**Users.** The author, who drops each domain module into this scaffolding. Other project teams, who run `uv run pytest` to confirm their documents validate and read `docs/model/` to learn the contract. The schema viewer, which loads `dist/*.schema.json` self-contained, or, on request, `dist/viewer/*.schema.json` where a module's classes reference another module's file instead of duplicating it.

**Success in one sentence.** A clean clone plus two commands produces a passing test run and, from a fixture schema, a draft 2020-12 JSON Schema that passes its meta-schema and a folder of Markdown documentation, on Windows and on Linux CI alike.

**What this module deliberately is not.** It contains no domain model. `schema/` is empty when this module is complete. It does not implement the tier 2 or tier 3 checks from the brief; those are the step 2 generator.

## Tech Stack

| Concern | Choice | Notes |
|---|---|---|
| Python | 3.12, via `.python-version` | uv installs it if absent |
| Environment, lockfile, runner | uv | `pyproject.toml` + `uv.lock`; every command is `uv run …` |
| Schema toolkit | `linkml` (latest 1.x at lock time; 1.11.1 on 2026-09-11) | provides `linkml-lint`, `linkml-validate`, `gen-json-schema`, `gen-doc` |
| Tests | `pytest` | |
| JSON Schema meta-check | `jsonschema` | `Draft202012Validator.check_schema` |
| CI | GitHub Actions | one workflow, one job, `ubuntu-latest` |

Exact versions are whatever `uv lock` resolves on first run and are then fixed by `uv.lock`. Dependency upgrades are a deliberate commit, never a side effect.

## Commands

```
uv sync                          # create .venv from uv.lock; first run also installs Python 3.12
uv run pytest                    # full acceptance suite
uv run python scripts/build.py   # regenerate dist/ and docs/model/ from schema/
uv run linkml-lint schema/       # lint alone, for quick feedback while editing a module
uv run linkml-validate -s schema/<module>.yaml -C <Class> <file.yaml>
                                 # validate one document by hand
uv run python scripts/build.py --viewer-schemas
                                 # also write dist/viewer/*.schema.json, the cross-file $ref
                                 # variant for manual upload to a JSON Schema viewer; not
                                 # committed, not produced unless this flag is given
```

### `scripts/build.py`

Behaviour, fully specified so a domain module never has to think about it:

1. For every `schema/<module>.yaml`, in file-name order: run `gen-json-schema` with imports merged (the default) and write the result to `dist/<module>.schema.json`. Before writing, replace the value of the top-level `$schema` key with `https://json-schema.org/draft/2020-12/schema`. LinkML hardcodes draft 2019-09 and offers no option to change it; this is the one place the contract diverges from what LinkML emits, and the meta-schema test in this module proves the rewrite is valid on every build.
2. For every `schema/<module>.yaml`: run `gen-doc` with imports not merged and write to `docs/model/<module>/`, so each module's documentation covers its own elements only and a team reads one folder.
3. Write `dist/README.md`: one heading, one sentence saying these files are generated from `schema/` and how to regenerate them, then one line per module: the file name, the draft, and the module's `description` read from its YAML. Written on every build so it can never disagree with the folder.
4. Remove stale outputs: any `dist/*.schema.json` or `docs/model/<dir>/` with no matching module file is deleted, so a renamed module does not leave ghosts. Each module's docs folder is cleared before `gen-doc` writes it, so a removed class, slot, or enum does not leave its old page behind (added 2026-09-11 after the drift test caught exactly that).
5. If `schema/` has no modules, write a `dist/README.md` saying so and exit 0.
6. Exit non-zero on the first generator failure, with the generator's message unaltered.
7. Only with `--viewer-schemas` on the command line: build one map from every class and enum name to the single `schema/<module>.yaml` that declares it, by reading each module's own `classes:` and `enums:` keys directly (never what it imports). Project rules already forbid two modules declaring the same name, so this map has no collisions to arbitrate. Then, for every module, take the merged JSON Schema already produced in step 1, remove from its `$defs` every entry whose name the map assigns to a different module, and rewrite every `"$ref": "#/$defs/<Name>"` naming a removed entry to `"$ref": "<owning-module>.schema.json#/$defs/<Name>"`. A module with nothing foreign in its `$defs` (`common` today) comes out identical to its `dist/` counterpart. Write the result to `dist/viewer/<module>.schema.json` with the same draft 2020-12 rewrite as step 1, plus `dist/viewer/README.md` stating what these files are, that they reference each other by plain relative filename, and that they are not the canonical `dist/` artifact. `dist/viewer/` is gitignored: a local, on-demand output, never committed, never checked for drift.

No flags besides `--viewer-schemas`, no configuration file. Target length: under a hundred lines including docstring.

## Project Structure

```
.python-version               3.12
pyproject.toml                project metadata, dependencies, pytest config
uv.lock                       resolved, committed
CAPABILITY-MAP.md             module index (exists)
SPEC-<module>.md              one per module (this file is the first)
schema/                       LinkML modules; empty until the common module lands
  .gitkeep
examples/                     instance documents, one subfolder per module; empty for now
  .gitkeep
dist/                         generated JSON Schema, one file per module, committed
  README.md                   generated: what each file is and how to regenerate
  viewer/                      generated only with --viewer-schemas; cross-file $ref variant
                               for manual upload to a schema viewer; gitignored, never committed
    README.md                 generated: what these files are and how they differ from dist/
docs/
  model/                      generated Markdown, one folder per module, committed
    .gitkeep
  ideas/ research/            as today
scripts/
  build.py                    the build described above
tests/
  conftest.py                 repo-root path fixture, nothing else
  fixtures/
    minimal.yaml              a three-class LinkML schema exercising: an identifier, a
                              reference slot, an inlined value object, an enum
    minimal_instances.yaml    two valid instances of the fixture's top class
    minimal_invalid.yaml      one instance missing a required slot
  test_build.py               build.py on the fixture: 2020-12 output, meta-schema passes,
                              docs folder created, stale outputs removed, empty schema/ is a no-op
  test_lint.py                every schema/*.yaml lints clean (skips cleanly when none exist)
  test_examples.py            every examples/**/*.yaml validates against the class named in
                              EXAMPLE_TARGETS; every examples/invalid/*.yaml fails
  test_dist.py                committed dist/ and docs/model/ equal a fresh build; every
                              dist/*.schema.json passes Draft202012Validator.check_schema
.github/workflows/ci.yml      install uv, uv sync, uv run pytest
```

`EXAMPLE_TARGETS` is one dictionary in `test_examples.py` mapping an example path to its target class. Domain modules add rows; nothing else changes.

## Code Style

One excerpt from the build script sets the tone for all Python in this repo.

```python
"""Regenerate dist/ and docs/model/ from every LinkML module under schema/."""
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SCHEMA, DIST, DOCS = ROOT / "schema", ROOT / "dist", ROOT / "docs" / "model"
DRAFT = "https://json-schema.org/draft/2020-12/schema"


def json_schema(module: Path) -> None:
    out = subprocess.run(
        ["gen-json-schema", str(module)], check=True, capture_output=True, text=True
    ).stdout
    schema = json.loads(out)
    schema["$schema"] = DRAFT
    (DIST / f"{module.stem}.schema.json").write_text(
        json.dumps(schema, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
```

Conventions:

- **Standard library first.** The build script imports only the standard library plus PyYAML, which LinkML already depends on, to read each module's `description`; it shells out to the LinkML CLIs rather than importing their Python API, so a LinkML internal change cannot break the build silently.
- **Paths are `pathlib`, relative to `ROOT`.** Never `os.getcwd()`, never string concatenation.
- **Files are written with explicit `encoding="utf-8"` and `newline="\n"`.** The `.gitattributes` already pins LF; the code should not rely on it.
- **Tests are plain functions with plain `assert`.** Parametrise over files with `pytest.mark.parametrize`. No test classes, no fixtures beyond the repo root path.
- **Type hints on every function signature.** No `Any`.
- **Ruff defaults, no configuration.** If it is worth arguing about, it is not worth configuring.

## Testing Strategy

There is one thing under test in this module, the build script, and one thing to prove about the harness, that it passes with no domain modules present. Everything runs with `uv run pytest`; there is no other test entry point.

| Test | Proves | How |
|---|---|---|
| `test_build.py::test_fixture_produces_2020_12` | The rewrite works | Run `build.py` against a temp copy of the repo whose `schema/` holds `fixtures/minimal.yaml`; the output declares draft 2020-12 |
| `test_build.py::test_fixture_passes_metaschema` | The rewrite is valid | `Draft202012Validator.check_schema` on the output raises nothing |
| `test_build.py::test_fixture_docs_generated` | Docs per module | `docs/model/minimal/` exists and contains an `index.md` |
| `test_build.py::test_readme_lists_modules` | Rule 3 | `dist/README.md` names `minimal.schema.json` and contains the fixture's description |
| `test_build.py::test_stale_outputs_removed` | Rule 4 | Pre-seed `dist/ghost.schema.json`, a `docs/model/ghost/` folder, and a stale page inside the fixture's own docs folder; after build all three are gone |
| `test_build.py::test_empty_schema_is_noop` | Rule 5 | Empty `schema/`; exit 0; `dist/` holds only a README saying no modules exist; `docs/model/` unchanged |
| `test_examples.py` on the fixture instances | The validation path works | `minimal_instances.yaml` validates; `minimal_invalid.yaml` fails with the missing slot named |
| `test_lint.py`, `test_dist.py` | Domain hooks are wired | Both collect zero files today and pass; they are the tests domain modules will light up |
| `test_build.py::test_viewer_schemas_off_by_default` | Rule 7 is opt-in | Build a temp tree with two modules, one importing the other, without the flag; `dist/viewer/` is not created |
| `test_build.py::test_viewer_schemas_splits_defs` | Rule 7's partition | Build the same temp tree with `--viewer-schemas`; the importing module's `dist/viewer/*.schema.json` `$defs` hold only the names its own `schema/*.yaml` declares, and a `$ref` to an imported name reads `"<other-module>.schema.json#/$defs/<Name>"` |
| `test_build.py::test_viewer_schemas_resolves_end_to_end` | The cross-file `$ref` is real, not just shaped right | Load both temp-tree `dist/viewer/*.schema.json` files into a `jsonschema` registry keyed by filename and validate a real instance through the `$ref` boundary; it succeeds, and breaking the target class name makes it fail |
| `test_build.py::test_viewer_schemas_noop_module` | The no-foreign-classes case | A module that imports nothing produces a `dist/viewer/<module>.schema.json` identical to its `dist/<module>.schema.json` |

The build tests operate on a temporary copy so they never touch the committed `dist/` and `docs/model/`. `dist/viewer/` is never committed, so no drift test applies to it. Coverage is not measured; the criterion is that every rule in the build description has a test, which the table shows.

## Boundaries

**Always.** `uv run pytest` passes before every commit. Conventional Commits 1.0.0. LF line endings. Rebuild and commit `dist/` and `docs/model/` in the same commit as any `schema/` change. Standard library plus PyYAML only in `scripts/`.

**Ask first.** Adding a dependency to `pyproject.toml`. Changing the CI workflow. Changing the Python version. Adding a flag or configuration to `build.py`. Adding a second script.

**Never.** Hand-edit anything under `dist/` or `docs/model/`. Import LinkML's Python API in the build script. Delete or skip a failing test. Put domain content in this module: `schema/` stays empty until `common` lands.

## Success Criteria

Checkable by anyone with git and uv:

1. On a clean clone: `uv sync` then `uv run pytest` passes, on Windows and on `ubuntu-latest`.
2. `uv run python scripts/build.py` with an empty `schema/` exits 0 and leaves `dist/` holding only a README saying no modules exist.
3. With `tests/fixtures/minimal.yaml` copied into `schema/`, `build.py` produces `dist/minimal.schema.json` declaring draft 2020-12 that passes `Draft202012Validator.check_schema`, a `dist/README.md` listing it with its description, and `docs/model/minimal/index.md`. Then delete the copy and rebuild: the schema file and docs folder are gone and the README says no modules exist.
4. The GitHub Actions workflow passes on the commit that completes this module.
5. `scripts/build.py` is under a hundred lines and imports only the standard library and PyYAML.
6. Nothing exists under `schema/` except `.gitkeep`.
7. `uv run python scripts/build.py` with no flag never creates `dist/viewer/`.
8. Built from `tests/fixtures/minimal.yaml` and `tests/fixtures/importer.yaml` (a second fixture, added by this amendment, that imports `minimal` and declares one class referencing one of `minimal`'s), `dist/viewer/importer.schema.json`'s `$defs` hold only `importer`'s own `Crate`, with its reference to `minimal`'s `Dimensions` rewritten to `"minimal.schema.json#/$defs/Dimensions"`; both files, uploaded together to `rcpc-schema-viewer` (`C:\Users\go25qoh\Repos\rcpc-schema-viewer`), resolve with no stub class for `minimal.schema.json`. Chosen over the real `resource`/`common` pair because, at the time of writing, nothing in `resource.yaml` actually produces a live cross-module `$ref` yet (`offers` is a bare id array, not inlined) — the fixture proves the algorithm independent of `resource`'s in-progress state, matching how `test_build.py`'s other tests already avoid depending on any domain module.

## Open Questions

- Resolved 2026-09-11: `gen-doc --no-mergeimports` lists only the module's own classes, slots, and enums in its index, and still writes pages for the imported elements the module references, so every link resolves. Verified on a two-module probe. Per-module folders stand; no fallback needed.
- Resolved 2026-09-12: `gen-json-schema --no-mergeimports` was checked against `--mergeimports` on `schema/resource.yaml` and produced byte-identical `$defs`; LinkML's JSON Schema generator has no built-in unmerged mode, unlike `gen-doc`. Cross-file `$ref` output for the viewer is therefore hand-built as a post-processing step in `build.py` (rule 7), not a generator flag.
- Resolved 2026-09-12: the target viewer, `rcpc-schema-viewer` (`src/extract.mjs`'s `resolveRef`), matches a `$ref`'s file part by plain basename against every uploaded filename, checked before any `$id`/URL resolution, and degrades a `$ref` into a file that wasn't uploaded to one stub class rather than erroring. This is why rule 7 rewrites to a bare relative filename rather than a full `$id`-based URI, and why partial uploads stay safe.
