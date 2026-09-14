Clo# Tasks: toolchain — no `"null"`, natural key order

Plan: `tasks/archive/toolchain-null-key-order-plan.md`. Spec: `SPEC-toolchain.md` (changed 2026-09-14). One Conventional Commit for the code plus rebuilt `dist/`, and a separate `docs(plan): ...` commit for this file and the plan, per this project's established pattern. `uv run pytest` passes before every commit.

## Task 1: In-process JSON Schema generation without null, tests, rebuilt `dist/`

**Description:** In `scripts/build.py`, add `from linkml.generators.jsonschemagen import JsonSchemaGenerator` and replace the `run("gen-json-schema", str(module))` plus `json.loads` in `build()` with `dict(JsonSchemaGenerator(str(module), include_null=False).generate())`. Keep the `$schema` rewrite and the `json.dumps(indent=2)` write exactly as they are; no sorting anywhere. Update the module docstring's first line if it names the command. In `tests/test_build.py`, add `test_fixture_has_no_null_type` (build the fixture; the text of `dist/minimal.schema.json` contains no `"null"`, and one optional slot's schema has a plain string `type`) and `test_fixture_key_order` (the parsed top-level keys begin `["$schema", "$id"]`). Change `test_viewer_schemas_splits_defs` to read `dimensions["$ref"]` directly, since the `anyOf` null wrapper no longer exists. Run `uv run python scripts/build.py` on the real repo so `dist/common.schema.json` and `dist/resource.schema.json` are rebuilt; `docs/model/` must come out unchanged.

**Acceptance criteria:**
- [x] `grep -c '"null"' dist/*.schema.json dist/viewer/*.schema.json` reports 0 for every file
- [x] Every `dist/*.schema.json` opens with `$schema` then `$id`
- [x] `scripts/build.py` imports only the standard library, `yaml` and `JsonSchemaGenerator`, and stays under 130 lines
- [x] `git status` shows only `scripts/build.py`, `tests/test_build.py`, `dist/common.schema.json`, `dist/resource.schema.json` changed (plus the spec and these plan files); nothing under `docs/model/`

**Verification:**
- [x] Tests pass: `uv run pytest` → 28 passed (was 26; two added), including `test_dist.py::test_committed_outputs_match_fresh_build` against the rebuilt `dist/`
- [x] Build succeeds: `uv run python scripts/build.py` run twice on the real repo, second run leaves `git status` unchanged
- [x] Manual check: read the head and one optional slot of `dist/resource.schema.json`

**Dependencies:** None

**Files likely touched:**
- `scripts/build.py`
- `tests/test_build.py`
- `dist/common.schema.json`
- `dist/resource.schema.json`

**Estimated scope:** Small

**Evidence:**
- RED first: `test_fixture_has_no_null_type`, `test_fixture_key_order` and the adjusted `test_viewer_schemas_splits_defs` all failed against the old script (`"null"` present, `required` last instead of `$schema` first, `KeyError: '$ref'` because of the `anyOf` wrapper). GREEN after the swap; the key-order test then exposed the false `$defs`-last claim, corrected in the spec (see plan).
- `uv run pytest` → `28 passed in 60.28s`; `--collect-only` shows 28, `test_build.py` has 14 test functions (HEAD had 12).
- `grep -c '"null"'` → 0 for `dist/common.schema.json`, `dist/resource.schema.json`, `dist/viewer/common.schema.json`, `dist/viewer/resource.schema.json` (resource had 50 before).
- Both `dist/*.schema.json` open `{"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": "https://rcpc.for5672/schema/<module>", ...}`; resource's top-level keys are `$schema, $id, metamodel_version, version, title, type, additionalProperties, $defs`.
- `dist/resource.schema.json` `Activity.productivity` (optional) is now `{"$ref": "#/$defs/Quantity", "description": ...}` with no `anyOf`/`null` wrapper.
- `scripts/build.py`: 122 lines (`wc -l`); imports `pathlib, argparse, json, shutil, subprocess, sys`, `yaml`, `JsonSchemaGenerator`.
- Two consecutive real builds: `git status --porcelain` identical after the second; nothing under `docs/model/` changed.
- `git diff --stat`: `dist/resource.schema.json` 890 lines changed, `dist/common.schema.json` 150 (reordering only, it has no optional slots).

## Checkpoint: Complete
- [x] Task 1 committed with the rebuilt `dist/` in the same commit (`9aa182e`; spec `c27513d`; README wording `b2c2dd6`)
- [x] Success criteria 1, 3, 5 and 9 in `SPEC-toolchain.md` verified with evidence, recorded in the plan
- [x] CI run `34853901768` on `b2c2dd6` passed, recorded in the plan
