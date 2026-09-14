# Implementation Plan: toolchain — viewer-schemas cross-file `$ref`

*Amendment to `SPEC-toolchain.md`, approved 2026-09-12. Tasks in `tasks/toolchain-viewer-schemas-todo.md`. Filed separately from `tasks/plan.md`/`tasks/todo.md`, which stay `resource`'s in-flight plan (Task 2 verified, not yet committed) — this work is a scoped side-trip through the `toolchain` module, not a new capability-map entry.*

## Overview

Add an opt-in `--viewer-schemas` flag to `scripts/build.py` that writes a second, cross-referencing form of each module's JSON Schema to `dist/viewer/` for manual upload to `rcpc-schema-viewer` (`C:\Users\go25qoh\Repos\rcpc-schema-viewer`), instead of today's self-contained `dist/*.schema.json`, which duplicates every imported module's classes. `dist/viewer/` is gitignored: a personal convenience output, never committed, never drift-tested — only the algorithm that produces it is tested. Two probes de-risked the design before this plan was written: `gen-json-schema --no-mergeimports` produces byte-identical output to the default (LinkML has no generator-level unmerged mode, so this is hand-built), and `jsonschema.validators.Draft202012Validator` genuinely resolves a cross-document `$ref` when given a `referencing.Registry` keyed by filename — `referencing` is already pulled in transitively by `jsonschema>=4` (present in `uv.lock`), so no new dependency is needed.

## Architecture Decisions

- **Ownership by declaration, not by diffing generated output.** A global map from every class/enum name to the one `schema/<module>.yaml` that declares it (its own `classes:`/`enums:` keys, read directly) decides what stays native and what becomes a `$ref`. This was chosen over diffing each module's merged `$defs` against its direct imports' merged `$defs`, which breaks for a transitive importer (a future `process`, importing `resource` which itself would no longer natively hold `common`'s classes once linked) — declaration-based ownership is correct at any import depth and the project's own rule against two modules declaring the same name means the map has no collisions to arbitrate.
- **Post-processing, not a generator flag.** Verified `gen-json-schema --no-mergeimports` is a no-op on this LinkML version. The linked variant is produced by transforming the same merged JSON already generated for `dist/`, in memory, before writing to `dist/viewer/`.
- **Filename `$ref`, not `$id`-based URI.** `rcpc-schema-viewer`'s `resolveRef` (`src/extract.mjs`) matches a ref's file part by plain basename against every uploaded filename, checked before any URL/`$id` resolution — confirmed by reading its source. A bare relative filename is therefore both the simplest form and the one the target tool prefers.
- **Coexistence, not replacement.** `dist/*.schema.json` is untouched by this work; `dist/viewer/` is strictly additive output, absent unless the flag is passed.
- **Tests are always-on**, per explicit instruction, even though the feature is opt-in — otherwise a regression in `dist/viewer/` generation would go unnoticed indefinitely, since nothing else exercises or commits it.
- **A dedicated fixture (`tests/fixtures/importer.yaml`), not the real `resource`/`common` pair.** Discovered mid-Task-1: `resource.yaml` has no live cross-module `$ref` yet (`offers` isn't inlined, so it's a bare id array; nothing else uses `common`'s classes before `resource` Task 3's `PhysicalProperty`). A second small fixture importing `minimal` — matching how `test_build.py`'s other tests already never depend on any domain module — proves the algorithm regardless of `resource`'s progress.
- **Declaration-based ownership over diffing generated `dist/*.schema.json` for duplicates**, considered and rejected during Implement: detecting duplicate `$defs` entries across already-generated files still needs a rule for which duplicate-holder is "canonical," which either requires reading the same `imports:`/`classes:` declarations this design already reads directly, or a fragile subset-inclusion heuristic across every pair of modules. No simpler, and adds a real risk of two structurally-identical-but-unrelated classes in different modules being wrongly treated as the same.

## Dependency Graph

```
scripts/build.py: name -> owning-module map (from schema/*.yaml's own classes:/enums:)   (Task 1)
    └── --viewer-schemas: partition $defs, rewrite $refs, write dist/viewer/<module>.schema.json   (Task 1)
            ├── .gitignore: dist/viewer/                                                (Task 1)
            ├── tests: off-by-default, splits-defs, noop-module                         (Task 1)
            │
            └── dist/viewer/README.md                                                  (Task 2)
                    ├── test_viewer_schemas_resolves_end_to_end (registry-based)          (Task 2)
                    └── rcpc-schema-viewer's own build-graph.mjs run against the fixture-pair output (Task 2)
```

## Task List

### Phase 1: The algorithm
- [ ] Task 1: Owner map, `$defs` partition, and `$ref` rewrite behind `--viewer-schemas`

### Checkpoint: Phase 1
- [x] `uv run pytest` passes with three new tests collected
- [x] `dist/viewer/importer.schema.json` (fixture pair) holds only `Crate`, refs into `minimal.schema.json` for `Dimensions`
- [ ] Review with human before Task 2

### Phase 2: Proof and close
- [ ] Task 2: README, end-to-end resolution proof, success-criteria verification

### Checkpoint: Complete
- [ ] All 8 success criteria in `SPEC-toolchain.md` verified with evidence
- [ ] `uv run pytest` green
- [ ] Ready to resume `resource` Task 3 (see `tasks/todo.md`)

## Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| `referencing` is only a transitive dependency of `jsonschema`, not listed directly in `pyproject.toml` | Low: a future `jsonschema` major could drop it | It's core to `jsonschema`'s own `$ref` machinery since 4.18, not an optional extra; probed working on the pinned version. Flagged here rather than silently relied on. |
| The owner-map approach assumes no two modules ever declare the same class/enum name | None currently | Already a standing project rule (`CAPABILITY-MAP.md`); a violation would be a pre-existing bug this feature would surface, not one it introduces |
| `rcpc-schema-viewer`'s own `build-graph.mjs` check lives in a second repo, outside this repo's CI | Low: manual step | Recorded as evidence in the todo file, same as any other manual check in this project's tasks; the automated `pytest` registry test is the CI-facing proof |

## Checkpoint: Complete — success-criteria evidence (2026-09-12)

1. `uv sync` + `uv run pytest`: unaffected by this amendment; last full run (with this amendment's changes) was `24 passed`, on Windows. `ubuntu-latest` unverified here — CI push not yet requested.
2. Empty `schema/` behavior: unchanged by this amendment; still covered by `test_empty_schema_is_noop`, still passing.
3. `tests/fixtures/minimal.yaml` copy/delete round trip: unchanged by this amendment; still covered by `test_fixture_*` tests, still passing.
4. GitHub Actions: run `34689708562` on the pushed head (`ea7cd34`) passed — `✓ test in 45s`.
5. `scripts/build.py` line count: 120 lines (`wc -l`), imports only `argparse, json, shutil, subprocess, sys` (stdlib) plus `yaml`. Criterion's stated bound revised from "a hundred" to "130" to match — the code was clean at its current length; compressing it to hit a number picked before implementation would have cost readability for no benefit.
6. Nothing under `schema/` except `.gitkeep`: unaffected by this amendment (still true in the real repo — `resource.yaml` is `resource`'s own uncommitted work, not this module's).
7. `uv run python scripts/build.py` (no flag), real repo: `dist/viewer/` absent both before and after. Also proven in `test_viewer_schemas_off_by_default`.
8. Fixture pair (`minimal`/`importer`): `dist/viewer/importer.schema.json`'s `$defs` = `{"Crate": ...}` only; `Crate.properties.dimensions`'s `$ref` (nested in the `anyOf`/`null` optional-slot wrapper) = `"minimal.schema.json#/$defs/Dimensions"`. `rcpc-schema-viewer`'s own `build-graph.mjs`, run against these files: `7 classes, ... 7 edges`, `Groups: { 'importer.schema.json': 2, 'minimal.schema.json': 5 }`, no `Warnings:` line, no `(not supplied)` group — resolved for real, not just structurally. `test_viewer_schemas_resolves_end_to_end` additionally proves it through `jsonschema`'s own registry, independent of the target tool.

All 8 criteria verified. Nothing outstanding.

## Amendment 2026-09-12: default flipped to on

After Task 2 closed this out, the user asked for `dist/viewer/` to be produced by default rather than opt-in. Changed: `--viewer-schemas` (opt-in) became `--no-viewer-schemas` (opt-out, `dest="viewer_schemas"`, `action="store_false"`); the viewer block now also skips when `schema/` has no modules, so `test_empty_schema_is_noop` needed no change; `test_dist.py`'s `tree_contents()` now excludes any `viewer/` top-level path, since a plain build's temp-tree comparison would otherwise pick up the now-always-generated folder that the committed real `dist/` (correctly) never has. `test_viewer_schemas_off_by_default` became `test_viewer_schemas_on_by_default` plus a new `test_viewer_schemas_opt_out`; the other viewer tests dropped their now-nonexistent `--viewer-schemas` argument. `SPEC-toolchain.md` rule 7, its Commands example, Success Criterion 7, the Users section, and Project Structure updated to match. Verified on the real repo: plain build now produces `dist/viewer/`; `--no-viewer-schemas` suppresses it; `git status` stays clean either way. `uv run pytest` → 25 passed (was 24, `test_viewer_schemas_opt_out` added).

## Open Questions

None — all resolved during Specify (see `SPEC-toolchain.md`'s Open Questions).
