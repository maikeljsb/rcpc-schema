# Implementation Plan: common

*Module `common` of `CAPABILITY-MAP.md`, specified in `SPEC-common.md`. Plan drafted and approved 2026-09-11. Tasks in `tasks/todo.md`. The completed `toolchain` plan is archived under `tasks/archive/`.*

## Overview

Write `schema/common.yaml` as the first real module through the toolchain, in two vertical slices: first the one document class, `CapabilityType`, end to end from schema to example to test to generated outputs; then the value types, `Position`, `Quantity`, `MaterialName`, and the `ParameterKind` enum, which have no documents of their own and are proven by lint, build, and the generated schema's contents. A third task verifies the spec's seven success criteria, pushes, and confirms CI. The toolchain is not touched.

## Dependency Graph

```
schema/common.yaml  (header + shared slots + CapabilityType)      (Task 1)
    ├── examples/common/capability_types.yaml                       (Task 1)
    ├── examples/common/invalid/capability_type_missing_id.yaml     (Task 1)
    ├── tests/test_examples.py  two rows                            (Task 1)
    └── dist/common.schema.json, dist/README.md, docs/model/common/ (Task 1, rebuilt)
            │
            └── schema/common.yaml  (+ Position, Quantity, MaterialName, ParameterKind)   (Task 2)
                    └── dist/, docs/model/common/  rebuilt; no-tree_root check           (Task 2)
                            │
                            └── success criteria verified, push, CI                       (Task 3)
```

Slice 1 comes first because it is the only path that exercises every toolchain hook at once: lint, example validation, invalid-example failure, drift, meta-schema. If anything in the pipeline misbehaves on a real module, it shows here with the smallest possible schema. Slice 2 adds definitions with no documents, so its only new evidence is what the generated JSON Schema and docs contain.

## Architecture Decisions

- **Every schema change is committed with its rebuilt outputs.** `SPEC-toolchain.md` requires it and `test_dist.py` enforces it. Tasks 1 and 2 each end with `uv run python scripts/build.py` and commit `dist/` and `docs/model/common/` alongside the YAML.
- **`CapabilityType` first, value types second.** Vertical slice over a horizontal one: the document class runs the whole pipeline; the value types only add to the generated outputs.
- **The no-`tree_root` decision is re-checked on the real generated file.** Already confirmed on a probe; Task 2 asserts the same on `dist/common.schema.json` so the evidence is about the real module.
- **LinkML inlines types by default, and that is what we want.** Verified on a probe 2026-09-11 and confirmed by the generator docs: a `MaterialName` slot renders as a plain string, `$defs` holds only classes and enums, and a schema with no `tree_root` has no root `properties`. The spec's criterion 2 says so; `MaterialName` is verified through the docs index.
- **Capability descriptions are migrated by script, not retyped.** The ten entries come from `docs/reference-schemas/capabilities.json` with "element" replaced by "component" and the one mojibake dash in the `gripper` description replaced by a plain comma. Nothing else changes.
- **Example files are top-level YAML lists**, as proven in the toolchain module.

## Task List

### Phase 1: The document class, end to end
- [x] Task 1: `CapabilityType` through the whole pipeline

### Checkpoint: Phase 1
- [x] `uv run pytest` passes with lint, example, drift, and meta-schema tests collected for common
- [ ] Review with human

### Phase 2: Value types and enum
- [ ] Task 2: `Position`, `Quantity`, `MaterialName`, `ParameterKind`, rebuilt outputs, generated-schema check

### Phase 3: Close
- [ ] Task 3: Verify the seven success criteria, push, confirm CI

### Checkpoint: Complete
- [ ] Every success criterion in `SPEC-common.md` verified with evidence
- [ ] No commit in this module touched `scripts/` or the toolchain tests
- [ ] Ready for `SPEC-product.md` and `SPEC-resource.md`

## Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| `gen-json-schema` puts a tree-root-less schema's root in a shape the viewer cannot load | Medium: viewer is a stated consumer | Task 2 inspects the root; the spec's open question covers it; fix would be in the toolchain build, as a separate module change |
| `linkml-lint` rejects a slot named `description` or a type without `uri` | Low: fixture already used a `description` slot; types may need a `base` or `typeof` | Task 1 and 2 run lint first; fix in the YAML |
| The reference `gripper` description carries mojibake for a dash | Low | Replaced by a comma during migration, recorded in the task |
| Drift test fails because docs contain a timestamp or non-deterministic content | Medium: would fail on every run | Toolchain module already proved the fixture docs are deterministic; if common differs, it is a toolchain finding |

## Parallelisation

None. Three short sequential tasks.

## Open Questions

- Resolved 2026-09-11: push permission from the toolchain module carries over to this module. Task 3 pushes without a fresh go-ahead.
