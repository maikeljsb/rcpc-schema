# Tasks: toolchain — viewer-schemas cross-file `$ref`

Plan: `tasks/toolchain-viewer-schemas-plan.md`. Spec: `SPEC-toolchain.md` (amended 2026-09-12). Each task is one Conventional Commit for the code, and a separate `docs(plan): mark ... task N done` commit for this file and the plan, per this project's established pattern. `uv run pytest` passes before every commit.

## Task 1: Owner map, `$defs` partition, and `$ref` rewrite behind `--viewer-schemas`

**Description:** Add `argparse` handling to `scripts/build.py` for a `--viewer-schemas` boolean flag (default off, no other flags). Build one map from every class/enum name to the `schema/<module>.yaml` that declares it, by reading each module's own `classes:`/`enums:` top-level keys directly (already-loaded YAML, same read used for `description`) — never what a module imports. When the flag is set, for every module: take the already-generated merged JSON Schema dict, walk it to rewrite every `"$ref": "#/$defs/<Name>"` where `<Name>`'s owner isn't this module to `"$ref": "<owner>.schema.json#/$defs/<Name>"`, then drop every `$defs` entry not owned by this module. Write the result to `dist/viewer/<module>.schema.json` with the same draft 2020-12 rewrite already applied to `dist/`. Add `dist/viewer/` to `.gitignore`. Add `tests/fixtures/importer.yaml`, a second fixture importing `minimal` with one class (`Crate`) referencing one of `minimal`'s (`Dimensions`) — added because, at the time of writing, `resource.yaml` has no live cross-module `$ref` yet (`offers` isn't inlined), so the real `common`/`resource` pair can't exercise the rewrite; the fixture proves the algorithm independent of `resource`'s in-progress state, same as every other `test_build.py` test.

**Acceptance criteria:**
- [x] `uv run python scripts/build.py` (no flag) leaves `dist/viewer/` absent
- [x] `uv run python scripts/build.py --viewer-schemas` on a temp tree built from `tests/fixtures/minimal.yaml` + `tests/fixtures/importer.yaml` produces `dist/viewer/minimal.schema.json` byte-identical to `dist/minimal.schema.json` (nothing foreign to strip)
- [x] The same run produces `dist/viewer/importer.schema.json` whose `$defs` hold only `Crate`, with its `$ref` to `Dimensions` rewritten to `"minimal.schema.json#/$defs/Dimensions"`
- [x] `git status --porcelain` never lists anything under `dist/viewer/` in the real repo

**Verification:**
- [x] Tests pass: `uv run pytest` with three new tests collected (`test_viewer_schemas_off_by_default`, `test_viewer_schemas_splits_defs`, `test_viewer_schemas_noop_module`) — 22 collected total, all passing
- [x] Build succeeds: ran `scripts/build.py` with and without the flag against the real repo by hand, then via the temp-tree tests
- [x] Manual check: read `dist/viewer/importer.schema.json` end to end against the acceptance criteria above (see evidence below)

**Dependencies:** None (independent of `resource`'s remaining tasks)

**Files likely touched:**
- `scripts/build.py`
- `.gitignore`
- `tests/test_build.py`
- `tests/fixtures/importer.yaml`

**Estimated scope:** Medium

**Evidence:**
- `uv run pytest` → `22 passed` (`tests\test_build.py .........` — 9 collected there, was 6)
- `dist/viewer/importer.schema.json`'s `$defs`: `{"Crate": ...}` only; `Crate.properties.dimensions.anyOf` contains `{"$ref": "minimal.schema.json#/$defs/Dimensions"}`
- Manually ran `uv run python scripts/build.py` (no flag) then `--viewer-schemas` against the real repo: plain build leaves `dist/viewer/` absent/untouched; flagged build creates `dist/viewer/common.schema.json` (byte-identical to `dist/common.schema.json`) and `dist/viewer/resource.schema.json`; `git status --porcelain` showed nothing under `dist/viewer/` either time

## Checkpoint: Phase 1
- [x] `uv run pytest` passes with three new tests collected
- [x] `dist/viewer/importer.schema.json` (fixture pair) verified by hand against acceptance criteria
- [ ] Review with human before Task 2

## Task 2: README, end-to-end resolution proof, success-criteria verification

**Description:** Write `dist/viewer/README.md` on every `--viewer-schemas` run: what these files are, that they reference each other by relative filename, and that they are not the canonical `dist/` artifact. Add `test_viewer_schemas_resolves_end_to_end` in `tests/test_build.py`: build the `minimal`/`importer` fixture pair with `--viewer-schemas` into a temp tree, load both `dist/viewer/*.schema.json` files into a `referencing.Registry` keyed by filename, validate a `Crate` instance against `importer.schema.json`'s `Crate` through the cross-file `$ref` boundary with `jsonschema.validators.Draft202012Validator(schema=..., registry=...)`, and confirm it both accepts a valid `dimensions` value and rejects one missing `Dimensions`' required `width`/`height`. Then, from `C:\Users\go25qoh\Repos\rcpc-schema-viewer`, run its own dev CLI (`node src/build-graph.mjs <path-to-dist/viewer/importer.schema.json> <path-to-dist/viewer/minimal.schema.json>`) against the freshly built fixture files and record its output. Record all eight `SPEC-toolchain.md` success criteria with evidence in `tasks/toolchain-viewer-schemas-plan.md`. As an optional bonus (not a criterion — `resource` has no live cross-ref yet), also run `build-graph.mjs` against the real `dist/viewer/resource.schema.json` + `dist/viewer/common.schema.json` and note what it shows.

**Acceptance criteria:**
- [ ] `dist/viewer/README.md` exists after a `--viewer-schemas` build and states what the folder is
- [ ] `test_viewer_schemas_resolves_end_to_end` passes, and a deliberately broken target name in the test makes it fail (proving the check isn't a false positive)
- [ ] `rcpc-schema-viewer`'s `build-graph.mjs`, run against the fixture-pair generated files, reports `Crate` (from `importer.schema.json`) and `Dimensions` (from `minimal.schema.json`) linked with no "not supplied" stub for `minimal.schema.json`

**Verification:**
- [ ] Tests pass: `uv run pytest` with the new resolution test collected
- [ ] Build succeeds: `uv run python scripts/build.py --viewer-schemas` run twice, byte-identical output both times
- [ ] Manual check: the `node src/build-graph.mjs ...` output, pasted into this file as evidence

**Dependencies:** Task 1

**Files likely touched:**
- `scripts/build.py`
- `tests/test_build.py`

**Estimated scope:** Medium

## Checkpoint: Complete
- [ ] Both tasks committed
- [ ] All 8 success criteria in `SPEC-toolchain.md` verified with evidence, recorded in the plan
- [ ] `resource`'s `tasks/plan.md`/`tasks/todo.md` untouched throughout; ready to resume its Task 3
