# Spec: toolchain

*Module `toolchain` of `CAPABILITY-MAP.md`. Approved 2026-09-10. Depends on nothing; every other module depends on it.*

## Objective

Give the repository one command that a person on another team can run on a clean clone and see every test pass, and one command that turns whatever LinkML modules exist under `schema/` into the artifacts the contract promises: one JSON Schema per module in draft 2020-12 for the schema viewer, and generated documentation per module. Continuous integration runs the same commands on every push.

**Users.** The author, who drops each domain module into this scaffolding. Other project teams, who run `uv run pytest` to confirm their documents validate and read `docs/model/` to learn the contract. The schema viewer, which loads `dist/*.schema.json` self-contained, or `dist/viewer/*.schema.json`, written by default alongside it, where a module's classes reference another module's file instead of duplicating it.

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
uv run python scripts/build.py --no-viewer-schemas
                                 # skip dist/viewer/*.schema.json, the cross-file $ref variant
                                 # for manual upload to a JSON Schema viewer, written by default
                                 # alongside dist/; never committed either way
```

### `scripts/build.py`

Behaviour, fully specified so a domain module never has to think about it:

1. For every `schema/<module>.yaml`, in file-name order: build the JSON Schema in-process with `JsonSchemaGenerator(path, include_null=False).generate()`, imports merged (the default), replace the value of the top-level `$schema` key with `https://json-schema.org/draft/2020-12/schema`, and write the dict with `json.dumps(indent=2)` and no key sorting to `dist/<module>.schema.json`. The contract diverges from what the `gen-json-schema` command emits in exactly three ways, all decided here and all proven by tests in this module: the draft (LinkML hardcodes 2019-09 and offers no option), the absence of `"null"` from every optional slot's type (the generator's `include_null` default, which the command exposes no flag for, hence the in-process call), and key order (the command sorts every key alphabetically, putting `$defs` before `$id` and `$schema`; the dict's natural order opens with `$schema`, `$id`, like the draft 2020-12 meta-schema, and every nested object follows the generator's insertion order; a module with a `tree_root` class gets that class's properties appended after `$defs`).
2. For every `schema/<module>.yaml`: run `gen-doc` with imports not merged and write to `docs/model/<module>/`, so each module's documentation covers its own elements only and a team reads one folder.
3. Write `dist/README.md`: one heading, one sentence saying these files are generated from `schema/` and how to regenerate them, then one line per module: the file name, the draft, and the module's `description` read from its YAML. Written on every build so it can never disagree with the folder.
4. Remove stale outputs: any `dist/*.schema.json` or `docs/model/<dir>/` with no matching module file is deleted, so a renamed module does not leave ghosts. Each module's docs folder is cleared before `gen-doc` writes it, so a removed class, slot, or enum does not leave its old page behind (added 2026-09-11 after the drift test caught exactly that).
5. If `schema/` has no modules, write a `dist/README.md` saying so and exit 0.
6. Exit non-zero on the first generator failure, with the generator's message unaltered.
7. By default, and only when `schema/` has at least one module (skip entirely with `--no-viewer-schemas`, or when there is nothing to link): build one map from every class and enum name to the single `schema/<module>.yaml` that declares it, by reading each module's own `classes:` and `enums:` keys directly (never what it imports). Project rules already forbid two modules declaring the same name, so this map has no collisions to arbitrate. Then, for every module, take the merged JSON Schema already produced in step 1, remove from its `$defs` every entry whose name the map assigns to a different module, and rewrite every `"$ref": "#/$defs/<Name>"` naming a removed entry to `"$ref": "<owning-module>.schema.json#/$defs/<Name>"`. A module with nothing foreign in its `$defs` (`common` today) comes out identical to its `dist/` counterpart. Write the result to `dist/viewer/<module>.schema.json` with the same draft 2020-12 rewrite as step 1, plus `dist/viewer/README.md` stating what these files are, that they reference each other by plain relative filename, and that they are not the canonical `dist/` artifact. `dist/viewer/` is gitignored: a local output, never committed, never checked for drift, regenerated on every build unless suppressed.
8. Before writing step 1's file: for every `$defs` entry `<Name>__identifier_optional` (the generator's copy of a keyed class for use as an inlined dict's values, with the key slot dropped from `required`, because the key carries it) whose plain `<Name>` no `$ref` in the file points at, replace `<Name>`'s body with the copy's body, delete the copy, and rewrite every `"$ref": "#/$defs/<Name>__identifier_optional"` to `"$ref": "#/$defs/<Name>"`. A keyed class written only as dict values then has one definition, the one its values are checked against; a keyed class also written on its own keeps both, because both shapes occur. What the validator checks is unchanged, since `linkml-validate` builds its own JSON Schema from the YAML. Added 2026-09-18 for process's `Parameter` and `Binding`; proven on `tests/fixtures/keyed.yaml`.

No flags besides `--no-viewer-schemas`, no configuration file. Target length: under 130 lines including docstring.

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
  viewer/                      generated by default (skip with --no-viewer-schemas); cross-file
                               $ref variant for manual upload to a schema viewer; gitignored,
                               never committed
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
                              EXAMPLE_TARGETS, or, for a row whose class is "by record_type",
                              each record against the class its record_type names; every
                              examples/invalid/*.yaml fails
  test_dist.py                committed dist/ and docs/model/ equal a fresh build; every
                              dist/*.schema.json passes Draft202012Validator.check_schema
  test_references.py          every value of a reference slot named in REFERENCES resolves to
                              an id in the document it points at; "" only where allowed
                              (added 2026-09-21 by common, SPEC-common.md decision 17)
.github/workflows/ci.yml      install uv, uv sync, uv run pytest
```

`EXAMPLE_TARGETS` is one dictionary in `test_examples.py` mapping an example path to its target class. Domain modules add rows; nothing else changes. One row kind besides a class name, added 2026-09-18 for process: the class value `by record_type` makes the harness group the file's records by their `record_type`, write each group to a temporary file, and validate it with `-C <record_type>`; a record with no `record_type`, or one naming no class, fails the row naming the record. `linkml-validate` itself reads one class per run and never reads a designator.

## Code Style

One excerpt from the build script sets the tone for all Python in this repo.

```python
"""Regenerate dist/ and docs/model/ from every LinkML module under schema/."""
from pathlib import Path
import json
import subprocess
import sys

from linkml.generators.jsonschemagen import JsonSchemaGenerator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA, DIST, DOCS = ROOT / "schema", ROOT / "dist", ROOT / "docs" / "model"
DRAFT = "https://json-schema.org/draft/2020-12/schema"


def json_schema(module: Path) -> None:
    schema = dict(JsonSchemaGenerator(str(module), include_null=False).generate())
    schema["$schema"] = DRAFT
    (DIST / f"{module.stem}.schema.json").write_text(
        json.dumps(schema, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
```

Conventions:

- **Standard library first.** The build script imports the standard library, PyYAML (which LinkML already depends on) to read each module's `description`, and exactly one LinkML class, `JsonSchemaGenerator`, because dropping `"null"` has no command-line switch. Everything else shells out to the LinkML CLIs rather than importing their Python API, so a LinkML internal change cannot break the build silently; the one import fails loudly at start-up if LinkML renames it, and the drift test catches any silent change in its output.
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
| `test_build.py::test_fixture_has_no_null_type` | `include_null=False` took effect | The fixture's optional slot has a plain `"type"` and no `"null"` appears anywhere in the output |
| `test_build.py::test_fixture_key_order` | No key sorting | The output's top-level keys begin `$schema`, `$id` |
| `test_build.py::test_fixture_docs_generated` | Docs per module | `docs/model/minimal/` exists and contains an `index.md` |
| `test_build.py::test_readme_lists_modules` | Rule 3 | `dist/README.md` names `minimal.schema.json` and contains the fixture's description |
| `test_build.py::test_stale_outputs_removed` | Rule 4 | Pre-seed `dist/ghost.schema.json`, a `docs/model/ghost/` folder, and a stale page inside the fixture's own docs folder; after build all three are gone |
| `test_build.py::test_empty_schema_is_noop` | Rule 5 | Empty `schema/`; exit 0; `dist/` holds only a README saying no modules exist; `docs/model/` unchanged |
| `test_examples.py` on the fixture instances | The validation path works | `minimal_instances.yaml` validates; `minimal_invalid.yaml` fails with the missing slot named |
| `test_lint.py`, `test_dist.py` | Domain hooks are wired | Both collect zero files today and pass; they are the tests domain modules will light up |
| `test_build.py::test_viewer_schemas_on_by_default` | Rule 7 runs without any flag | Build a temp tree with two modules, one importing the other, with no flag; both `dist/viewer/*.schema.json` files are created |
| `test_build.py::test_viewer_schemas_opt_out` | `--no-viewer-schemas` suppresses it | Same temp tree, built with `--no-viewer-schemas`; `dist/viewer/` is not created |
| `test_build.py::test_viewer_schemas_splits_defs` | Rule 7's partition | Build the same temp tree with no flag; the importing module's `dist/viewer/*.schema.json` `$defs` hold only the names its own `schema/*.yaml` declares, and a `$ref` to an imported name reads `"<other-module>.schema.json#/$defs/<Name>"` |
| `test_build.py::test_viewer_schemas_resolves_end_to_end` | The cross-file `$ref` is real, not just shaped right | Load both temp-tree `dist/viewer/*.schema.json` files into a `jsonschema` registry keyed by filename and validate a real instance through the `$ref` boundary; it succeeds, and breaking the target class name makes it fail |
| `test_build.py::test_viewer_schemas_noop_module` | The no-foreign-classes case | A module that imports nothing produces a `dist/viewer/<module>.schema.json` identical to its `dist/<module>.schema.json` |
| `test_build.py::test_viewer_schemas_readme_written` | Rule 7's README | `dist/viewer/README.md` exists after a build and states the files are not committed and reference each other by `$ref` |

The build tests operate on a temporary copy so they never touch the committed `dist/` and `docs/model/`. `dist/viewer/` is never committed, so no drift test applies to it. Coverage is not measured; the criterion is that every rule in the build description has a test, which the table shows.

## Boundaries

**Always.** `uv run pytest` passes before every commit. Conventional Commits 1.0.0. LF line endings. Rebuild and commit `dist/` and `docs/model/` in the same commit as any `schema/` change. Standard library, PyYAML and `linkml.generators.jsonschemagen.JsonSchemaGenerator` only in `scripts/`.

**Ask first.** Adding a dependency to `pyproject.toml`. Changing the CI workflow. Changing the Python version. Adding a flag or configuration to `build.py`. Adding a second script.

**Never.** Hand-edit anything under `dist/` or `docs/model/`. Import anything from LinkML's Python API in the build script other than `JsonSchemaGenerator`; docs keep going through `gen-doc`. Delete or skip a failing test. Put domain content in this module: `schema/` stays empty until `common` lands.

## Success Criteria

Checkable by anyone with git and uv:

1. On a clean clone: `uv sync` then `uv run pytest` passes, on Windows and on `ubuntu-latest`.
2. `uv run python scripts/build.py` with an empty `schema/` exits 0 and leaves `dist/` holding only a README saying no modules exist.
3. With `tests/fixtures/minimal.yaml` copied into `schema/`, `build.py` produces `dist/minimal.schema.json` declaring draft 2020-12 that passes `Draft202012Validator.check_schema`, a `dist/README.md` listing it with its description, and `docs/model/minimal/index.md`. Then delete the copy and rebuild: the schema file and docs folder are gone and the README says no modules exist.
4. The GitHub Actions workflow passes on the commit that completes this module.
5. `scripts/build.py` is under 140 lines and imports only the standard library, PyYAML and `JsonSchemaGenerator`.
6. Nothing exists under `schema/` except `.gitkeep`.
7. `uv run python scripts/build.py` with no flag creates `dist/viewer/` by default; `--no-viewer-schemas` suppresses it; an empty `schema/` creates neither `dist/viewer/` nor its README (nothing to link).
8. Built from `tests/fixtures/minimal.yaml` and `tests/fixtures/importer.yaml` (a second fixture, added by this amendment, that imports `minimal` and declares one class referencing one of `minimal`'s), `dist/viewer/importer.schema.json`'s `$defs` hold only `importer`'s own `Crate`, with its reference to `minimal`'s `Dimensions` rewritten to `"minimal.schema.json#/$defs/Dimensions"`; both files, uploaded together to `rcpc-schema-viewer` (`C:\Users\go25qoh\Repos\rcpc-schema-viewer`), resolve with no stub class for `minimal.schema.json`. Chosen over the real `resource`/`common` pair because, at the time of writing, nothing in `resource.yaml` actually produces a live cross-module `$ref` yet (`offers` is a bare id array, not inlined) — the fixture proves the algorithm independent of `resource`'s in-progress state, matching how `test_build.py`'s other tests already avoid depending on any domain module.
9. No optional slot in `dist/*.schema.json` or `dist/viewer/*.schema.json` carries `"null"` in its type, and each file opens with `$schema` then `$id`. Narrowed 2026-09-18: a LinkML `array` slot renders with the generator's lax item type list, which contains the word `"null"` among six type names (linkml issue 2188); process's `ordering` slot is the first such slot, and that rendering is accepted.

## Open Questions

- Resolved 2026-09-11: `gen-doc --no-mergeimports` lists only the module's own classes, slots, and enums in its index, and still writes pages for the imported elements the module references, so every link resolves. Verified on a two-module probe. Per-module folders stand; no fallback needed.
- Resolved 2026-09-12: `gen-json-schema --no-mergeimports` was checked against `--mergeimports` on `schema/resource.yaml` and produced byte-identical `$defs`; LinkML's JSON Schema generator has no built-in unmerged mode, unlike `gen-doc`. Cross-file `$ref` output for the viewer is therefore hand-built as a post-processing step in `build.py` (rule 7), not a generator flag.
- Resolved 2026-09-12: the target viewer, `rcpc-schema-viewer` (`src/extract.mjs`'s `resolveRef`), matches a `$ref`'s file part by plain basename against every uploaded filename, checked before any `$id`/URL resolution, and degrades a `$ref` into a file that wasn't uploaded to one stub class rather than erroring. This is why rule 7 rewrites to a bare relative filename rather than a full `$id`-based URI, and why partial uploads stay safe.
- Resolved 2026-09-14: `"null"` in every optional slot's type and the alphabetical key order both came from the `gen-json-schema` command (the generator's `include_null=True` default, which has no CLI flag, and `sort_keys=True` in its `serialize()`). Fixed by calling the generator in-process, the one permitted LinkML import; the "never import LinkML's Python API" boundary was narrowed accordingly.
- Resolved 2026-09-12: `dist/viewer/` generation flipped from opt-in (`--viewer-schemas`) to on by default, with `--no-viewer-schemas` to skip it, per direct instruction. Still gitignored, never committed, never drift-tested; still skipped entirely when `schema/` has no modules.
