# Implementation Plan: toolchain — no `"null"`, natural key order

*Change to `SPEC-toolchain.md`, approved 2026-09-14 (rule 1, Code Style, Boundaries, success criteria 5 and 9, testing table). Tasks in `tasks/archive/toolchain-null-key-order-todo.md`. A scoped side-trip through the `toolchain` module, not a new capability-map entry; `resource` is complete and nothing else is in flight.*

## Overview

Every optional slot in `dist/*.schema.json` carries `"null"` in its type (50 occurrences in `resource.schema.json`, none in `common.schema.json`, which has no optional slots), and every file opens with `$defs` and buries `$schema` and `$id` at the bottom. Both come from the `gen-json-schema` command: the generator class defaults `include_null=True`, for which the command has no flag, and its `serialize()` dumps with `sort_keys=True`. The fix is one swap in `scripts/build.py`: call `JsonSchemaGenerator(path, include_null=False).generate()` in-process instead of shelling out, and dump the returned dict with `json.dumps(indent=2)` as today, which already does no sorting. Probed 2026-09-14 on `schema/resource.yaml`: zero `"null"`, top-level keys `$schema, $id, metamodel_version, version, title, type, additionalProperties, $defs`, meta-schema passes.

## Architecture Decisions

- **In-process generator, not JSON post-processing.** Stripping `"null"` after the fact would re-implement the generator's three branches (scalar type lists, `anyOf [$ref, null]` wrappers, optional arrays). One constructor argument does it correctly. This costs the spec's "never import LinkML's Python API" boundary, which was narrowed in the spec to permit exactly this class; `gen-doc` still runs as a command.
- **Natural order, nothing pinned.** Per direct instruction, the smallest change wins: no explicit key order in the script. The order is whatever the generator inserts, at every depth. Inside class definitions that is `type, additionalProperties, description, properties, required, title`; a property is `type, description`. The drift test would surface any reordering by a future LinkML upgrade, which is the intended place to notice it.
- **`dict(...)` of the generator's result.** `generate()` returns a `JsonSchema`, a `dict` subclass. Assigning `$schema` on it keeps the key's position because the key already exists. The viewer step's `json.loads(json.dumps(...))` copy already yields a plain dict, so `link()` needs no change.
- **Test the fixture, not the domain modules.** Both new tests run on `tests/fixtures/minimal.yaml`, like every other `test_build.py` test. The fixture's `Crate`/`dimensions` slot in `importer.yaml` is optional, so the existing `test_viewer_schemas_splits_defs` and `test_viewer_schemas_resolves_end_to_end` already cover an optional `$ref` slot without the null wrapper once adjusted.

## Dependency Graph

```
scripts/build.py: import JsonSchemaGenerator; build() calls generate() with include_null=False   (Task 1)
    ├── tests/test_build.py: test_fixture_has_no_null_type, test_fixture_key_order                (Task 1)
    ├── tests/test_build.py: test_viewer_schemas_splits_defs reads $ref directly, no anyOf        (Task 1)
    └── dist/common.schema.json, dist/resource.schema.json rebuilt (drift test)                  (Task 1)
            └── Checkpoint: success criteria 1, 3, 5, 9 with evidence; CI green after push       (Complete)
```

## Task List

### Phase 1: The swap
- [x] Task 1: In-process JSON Schema generation without null, tests, rebuilt `dist/` (verified 2026-09-14, evidence in `tasks/todo.md`; not yet committed)

### Checkpoint: Complete
- [x] `uv run pytest` green, 28 collected (was 26; two added)
- [x] `dist/*.schema.json` and `dist/viewer/*.schema.json` contain no `"null"`, open with `$schema`, `$id`
- Corrected during Implement: the spec briefly claimed every file also ends with `$defs`. False for a module with a `tree_root` class (the fixture's `Widget`), whose properties the generator appends after `$defs`. The requirement was only the opening; the claim was dropped from rule 1, criterion 9 and the test.
- [x] `docs/model/` byte-identical to before (docs path untouched)
- [x] Success criteria 1, 3, 5 and 9 of `SPEC-toolchain.md` verified with evidence (below)
- [x] CI run `34853901768` on the pushed head `b2c2dd6` passed (`ubuntu-latest`)

## Checkpoint: Complete — success-criteria evidence (2026-09-14)

1. `uv run pytest` → `28 passed in 60.28s` on Windows; `ubuntu-latest` green in CI run `34853901768`.
2. Empty `schema/`: unchanged by this change; `test_empty_schema_is_noop` still passes.
3. Fixture round trip: `test_fixture_produces_2020_12`, `test_fixture_passes_metaschema`, `test_fixture_docs_generated`, `test_readme_lists_modules`, `test_stale_outputs_removed` all pass against the in-process generator.
4. GitHub Actions: run `34853901768` on `b2c2dd6` (the head after the `dist/viewer/README.md` wording fix) passed.
5. `scripts/build.py`: 122 lines (`wc -l`); imports `pathlib`, `argparse, json, shutil, subprocess, sys`, `yaml`, `JsonSchemaGenerator`. Nothing else.
6. Unaffected.
7. `dist/viewer/` still produced by default and suppressed by `--no-viewer-schemas`; `test_viewer_schemas_on_by_default`, `test_viewer_schemas_opt_out` pass.
8. Fixture pair: `test_viewer_schemas_splits_defs` now reads `Crate.properties.dimensions.$ref` directly (no `anyOf` wrapper) and finds `"minimal.schema.json#/$defs/Dimensions"`; `test_viewer_schemas_resolves_end_to_end` passes unchanged.
9. `grep -c '"null"'` → 0 in `dist/common.schema.json`, `dist/resource.schema.json`, `dist/viewer/common.schema.json`, `dist/viewer/resource.schema.json`; each opens `{"$schema": ..., "$id": ...}`.

Decided the same day, outside this change: the root `type: object` and `additionalProperties: true` LinkML emits stay; the stray "(document root)" box they cause in rcpc-schema-viewer is a viewer-side fix (`hasRootStructure`), done the same day in rcpc-schema-viewer.

## Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| A future LinkML upgrade renames `JsonSchemaGenerator`, `include_null` or `generate()` | Build fails at import or call time | Loud failure, not silent; versions are locked in `uv.lock`, so this only happens on a deliberate upgrade commit |
| A future LinkML upgrade changes insertion order or default output | `dist/` drifts from a fresh build | `test_dist.py` already fails on any byte difference; rebuild and review in the upgrade commit |
| Importing the generator in-process is slower to start than the command | None that matters | One process import instead of N subprocess spawns; the build gets faster, not slower |
| `dist/viewer/README.md` text in `build.py` still says `--viewer-schemas`, the pre-flip flag name | Cosmetic, pre-existing, outside this change's scope | Noted here for the user to decide; not touched by Task 1 unless asked |

## Open Questions

None. All resolved during Specify (see `SPEC-toolchain.md`'s Open Questions, entry dated 2026-09-14).
