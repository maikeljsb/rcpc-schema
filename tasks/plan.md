# Implementation Plan: resource

*Module `resource` of `CAPABILITY-MAP.md`, specified in `SPEC-resource.md`. Plan drafted and approved 2026-09-12. Tasks in `tasks/todo.md`. The completed `common` plan is archived under `tasks/archive/`.*

## Overview

Write `schema/resource.yaml` in four slices after one prerequisite change to common. First common gains the four dimension slots, committed on its own so resource never builds against an uncommitted common. Then the entry and its one required group, `RobotUnit`, `RobotStatus`, and `Activity` with `offers`, go end to end from schema to examples to test rows to generated outputs, because that is the path the process module and the projection component depend on. Then `PhysicalProperty` with `Sensor` and `MountPosition`, the shape with the most new metamodel usage. Then the two remaining groups and Activity's other attributes, which only add optional slots. A final task verifies the seven success criteria and pushes.

## Dependency Graph

```
schema/common.yaml  (+ length, width, height, weight)                         (Task 1)
    └── dist/common.schema.json, docs/model/common/  rebuilt                   (Task 1)
            │
            └── schema/resource.yaml  (header, RobotStatus, RobotUnit, Activity + offers)   (Task 2)
                    ├── examples/resource/robot_units.yaml  two minimal entries              (Task 2)
                    ├── examples/resource/invalid/  missing_activity, zero_count, missing_offers  (Task 2)
                    ├── tests/test_examples.py  four rows                                    (Task 2)
                    └── dist/resource.schema.json, dist/README.md, docs/model/resource/       (Task 2)
                            │
                            └── + PhysicalProperty, Sensor, MountPosition                     (Task 3)
                                    ├── examples grow: physical groups, both sensor positions
                                    ├── invalid/robot_unit_group_missing_id.yaml, fifth row
                                    └── dist/, docs/  rebuilt
                                            │
                                            └── + OperationalRequirement, Safety, Activity attributes   (Task 4)
                                                    ├── examples grow to their final shape
                                                    └── dist/, docs/  rebuilt
                                                            │
                                                            └── success criteria verified, push, CI    (Task 5)
```

## Architecture Decisions

- **Common changes first, in its own commit.** `test_dist.py` compares committed outputs with a fresh build, and resource's generated schema embeds common's definitions. Committing the four slots before any resource file exists keeps every later diff about resource alone.
- **Each group slot on `RobotUnit` arrives with its class.** Task 2 declares only `activity`; `physical_property` comes in Task 3 and the other two in Task 4, so no slot range ever names a class that does not exist yet.
- **Entry plus required group is the first slice.** It exercises every construct the module depends on that common did not: `minimum_value`, `ifabsent` on an enum, a mandatory `inlined: true` on an identified range, and a non-inlined multivalued reference. Three of the four invalid documents belong to this slice, so the harness's slot-name check is proven early.
- **`Sensor` and `MountPosition` before the plain groups.** They are the only new shapes, an inlined list of identified objects and a second coordinate class reusing common's slots. If either misbehaves in the generated docs or schema, it shows in Task 3 with two plain groups still to write, not at the end.
- **Slots are declared in lineage-table order within each group**, and descriptions are the paper's definitions cut to one plain sentence. Attribution clauses appear only on the slots the spec names: `id`, `offers`, the three merged quantities, the four bounds, and the two sensor positions. This lets a reviewer read the YAML against the table top to bottom.
- **Every object-valued slot states `inlined: true`**, including those over `Quantity` and `Position` where LinkML would infer it, so the document shape is visible without knowing the inference rule.
- **The example file keeps two entries throughout** and grows in place across Tasks 2 to 4 until it matches success criterion 5: one entry with `count: 2`, all four groups, and a mounted sensor; the other with `count: 1` and a site-positioned sensor. Robots are fictional.
- **The unlinked common pages under `docs/model/resource/` are accepted**, as the spec records. The build script clears the folder before regenerating, so the drift test stays deterministic.

## Task List

### Phase 1: Prerequisite and the entry
- [ ] Task 1: Add the four dimension slots to common
- [ ] Task 2: `RobotUnit`, `RobotStatus`, and `Activity` with `offers`, end to end

### Checkpoint: Phase 1
- [ ] `uv run pytest` passes with four resource rows collected
- [ ] `dist/resource.schema.json` shows `minimum: 1` on `count`, `offers` as an array of strings, `activity` as a `$ref`
- [ ] Review with human

### Phase 2: The groups
- [ ] Task 3: `PhysicalProperty`, `Sensor`, `MountPosition`, and the fifth invalid document
- [ ] Task 4: `OperationalRequirement`, `Safety`, and Activity's remaining attributes

### Checkpoint: Phase 2
- [ ] All 56 lineage rows have their slot in `schema/resource.yaml`
- [ ] Example file matches success criterion 5
- [ ] Review with human

### Phase 3: Close
- [ ] Task 5: Verify the seven success criteria, push, confirm CI

### Checkpoint: Complete
- [ ] Every success criterion in `SPEC-resource.md` verified with evidence
- [ ] `schema/common.yaml` changed only in Task 1; no commit touched `scripts/` or the toolchain tests
- [ ] Ready for `SPEC-product.md`

## Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| `gen-doc` renders `ifabsent: RobotStatus(idle)` oddly or not at all on the `status` page | Low: docs only | Task 2 reads the generated `status.md`; if the default is missing, the slot description states it in words |
| A resource attribute slot name later collides with one product or process wants with a different meaning (`speed`, `precision`, `manufacturer`) | Medium: slots are global in the merged schema | The lineage table is the register; `SPEC-product.md` and `SPEC-process.md` check it before declaring a slot, per the never-rule pattern already in SPEC-common |
| The linter's `recommended` rule fires on a permissible value or the schema header without a description | Low | Every element gets a description in the same edit; lint runs first in every task |
| The drift test fails on the unlinked common pages in `docs/model/resource/` | Low: build clears the folder first | Task 2 runs the build twice and confirms `git status` is clean after the second run |
| Free-string units in the examples (`Cel`, `deg`, `brick/h`) read as wrong to a reviewer | Low: not enforced | Spec says UCUM recommended, not enforced; examples use UCUM case-sensitive codes where one exists |

## Parallelisation

None. Five sequential tasks on one schema file and one example file.

## Open Questions

- Resolved 2026-09-12: the agent pushes at Task 5.
