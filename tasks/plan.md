# Implementation Plan: process

*Module `process` of `CAPABILITY-MAP.md`, specified in `SPEC-process.md` (approved and committed 2026-09-18, `689af87`; its five prerequisites committed the same day, `269bcc4`, `bdfc723`, `a0b19ca`). Plan drafted 2026-09-18; its review the same day turned the plan side top-down and gave both sides a base class, `SPEC-process.md` decisions 6 and 18, and this plan was rewritten to match. Tasks in `tasks/todo.md`. The completed `product` plan is archived under `tasks/archive/`.*

## Overview

Write `schema/process.yaml` in three slices, each from schema to hand-written examples to test rows to generated outputs, then verify and push. The order follows the reference slots: the tasks first, because `Method`, `Subtask`, and both instance classes point at them; `Method` with `Subtask` second, the slice with every new metamodel construct (the class rule in list form, the two-dimensional array slot, the two forms of a keyed map entry); the plan side last, because a `TaskNetwork` and a decomposed compound list instances, an instance names a catalogue task and a method, and a binding is read against a parameter declared on that task. The spec fixed the model and the example content; this plan fixes only the order the schema is written in, which record lands in which task, and the four leaves the spec's plan excerpt left unwritten.

## Dependency Graph

```
schema/process.yaml  (header, ParameterKind, Parameter, Task, PrimitiveTask, CompoundTask)  (Task 1)
    ├── examples/process/catalogue.yaml   MoveTo, Attach, Detach, Place; Transport, ConstructComponent
    ├── examples/process/invalid/  four PrimitiveTask documents, one CompoundTask document
    ├── tests/test_examples.py  six rows, the first under BY_RECORD_TYPE
    └── dist/process.schema.json, dist/README.md, docs/model/process/
            │
            └── + Method, Subtask with its rule, compound_task, primitive_task, subtasks,      (Task 2)
                  ordering, arguments, applies_to
                    ├── catalogue.yaml grows by m_transport, m_prefab: all eight records
                    ├── invalid/  four Method documents
                    └── dist/, docs/  rebuilt
                            │
                            └── + TaskInstance, CompoundTaskInstance, PrimitiveTaskInstance,      (Task 3)
                                  TaskNetwork, Binding, tasks, decomposed_by, bindings, bound_to,
                                  and subtasks ranging TaskInstance on the compound instance
                                    ├── examples/process/plan.yaml   one network, three compounds, five leaves
                                    ├── invalid/  one TaskNetwork, one CompoundTaskInstance document
                                    └── dist/, docs/  rebuilt
                                            │
                                            └── success criteria verified, push, CI            (Task 4)
```

## Architecture Decisions

- **Reference targets before referrers.** `Task` and its two subclasses reference only common's `CapabilityType` and this module's `Parameter`, so they close first, and Task 1 proves `record_type` locking through `is_a` on the catalogue side before Task 3 relies on it for the instances. `Method` and `Subtask` reference both tasks. The plan side references all three catalogue classes. No slot ever names a class that does not yet exist in the file, and every example record names only ids that are already in a committed file, except within one task's own new file.
- **`Method` is its own task, not folded into Task 1.** It carries every construct the other three modules did not exercise: a class rule that must fire inside an `inlined_as_list` entry, an `array` slot of two dimensions, `minimum_cardinality` on an inlined list, and the full form of a keyed map entry beside the one-line form. If the generated schema or docs misrender any of them, it shows with the plan side still unwritten. Task 1 already proves the one-line form and the enum through it, so the two forms are checked on two different days.
- **The catalogue file grows across two tasks.** `catalogue.yaml` is committed in Task 1 with six records and reaches its eight in Task 2. Its `BY_RECORD_TYPE` row validates whatever classes the file holds, so the row is added once and never changes.
- **The plan file lands whole in Task 3.** A plan is one thing a planner hands over; a network without its instances would validate but bind nothing. The nine records are written together and checked once against the tier 2 rows.
- **Slots and classes are written in the spec's table order.** Classes in the order of the Classes table; slots declared under `slots:` in the order of the slot table, each with `inlined: true` when object-valued and `range` alone when a reference. Per-class requirements go in `slot_usage`, as the Code Style block shows, so a reviewer reads the YAML against the spec top to bottom.
- **The four leaves the spec did not write out** follow its one written leaf and its method arguments. `construct_138157_1` (Transport by `m_transport`, `from` the exterior of Level 1 `3It7HtQdTQBQsvQlFr2iGK`, `to` the foyer A101 `0BTBFw6f90Nfh9rP1dlXrr`) lists four subtasks: `MoveTo {r, to: 3It7…}`, `Attach {r, c, at: 3It7…}`, `MoveTo {r, to: 0BTB…}`, `Detach {r, c, at: 0BTB…}`. `construct_138157` lists that Transport and then `Place {r, c, at: 0BTB…}`. Every `r` is `mason_m1_1`, every `c` the wall `2O2Fr$t4X7Zf8NOew3FNqI`. Ids are the listing compound's id with the entry's number appended, as the spec's convention says. Both walls, both Spaces, and the machine's entry were checked to exist in the committed example files, and the whole file validated through the split against a probe schema of the spec's shape, on 2026-09-18.
- **Invalid documents are one real record each with one edit**, copied from the committed catalogue or plan file and broken on the slot the row names.
- **The case-collision check is done on names, not on the folder listing.** On this Windows checkout gen-doc writes two pages that differ only by case into one file, so listing `docs/model/process/` cannot see the collision that Linux CI will. Tasks 3 and 4 instead lowercase every class, slot, enum, type, and schema name that `SchemaView` reports for the module with imports and assert no two coincide. Probed 2026-09-18: the spec's first shape had a `position` slot, whose page overwrote common's `Position.md` here; the current shape has no such pair, checked on the probe schema.
- **Success criterion 5 is a one-off script in the scratchpad**, not committed, as product's criterion 5 was. It reads the catalogue, the plan, and the sibling example files and prints one line per tier 2 row of the spec; the todo records its output once.
- **No dependency, no new test file, one toolchain rule.** `test_examples.py` gains rows only; the `BY_RECORD_TYPE` row kind is already committed. `SPEC-toolchain.md` rule 8 (spec prerequisite 6, decided in Task 1 on 2026-09-18) gives a keyed class written only as dict values one JSON Schema definition; it lands in its own commit before Task 1's, as the other prerequisites did.

## Task List

### Phase 1: The catalogue
- [x] Task 1: `Task` with `PrimitiveTask` and `CompoundTask`, `Parameter`, and `ParameterKind`, end to end
- [ ] Task 2: `Method` and `Subtask` with its rule, end to end

### Checkpoint: Phase 1
- [ ] `uv run pytest` passes with ten process rows collected
- [ ] `dist/process.schema.json` has `minItems: 1` on `requires` and `Method.subtasks`, a bare `if`/`then` on `Subtask`, and `"null"` exactly once, in `Method.ordering.items.type`
- [ ] Review with human

### Phase 2: The plan side
- [ ] Task 3: `TaskNetwork`, `CompoundTaskInstance`, `PrimitiveTaskInstance`, and `Binding`, end to end

### Checkpoint: Phase 2
- [ ] Thirteen process rows pass; `plan.yaml` validates through the split, `record_type` locking to each subclass
- [ ] Every id `plan.yaml` names resolves in `catalogue.yaml`, `plan.yaml`, `examples/product/`, or as a machine of `mason_m1`; every instance is listed exactly once
- [ ] Review with human

### Phase 3: Close
- [ ] Task 4: Verify the seven success criteria, push, confirm CI

### Checkpoint: Complete
- [ ] Every success criterion in `SPEC-process.md` verified with evidence
- [ ] `schema/common.yaml`, `schema/product.yaml`, `schema/resource.yaml`, `tests/test_lint.py`, and `tests/test_dist.py` untouched by Tasks 1 to 4; `scripts/build.py` and `tests/test_build.py` changed by the prerequisite 6 commit only
- [ ] Ready for step 2 of the brief, the generator

## Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| A process name collides case-insensitively with an imported one in the generated docs; Windows hides it, Linux CI fails the drift test | High if it happens: CI red on the commit | The name scan in Tasks 3 and 4; the current names were scanned on 2026-09-18 and are clear |
| The `Subtask` rule or the `ordering` array renders differently in `build.py`'s in-process generator than in the spec's probe | Medium: criterion 2 fails | Task 2 checks the three JSON Schema facts in the Phase 1 checkpoint before its commit |
| The one-line `Parameter` form fails under `linkml-validate` when the file holds mixed forms | Low: probed in the spec | Task 1 writes `MoveTo` one-line and Task 2 writes `m_prefab`'s `c` in full form, so both forms sit in one file from Task 2 on |
| Thirteen rows, two of them split into three validator runs each, push the suite well past its current 80 s | Low | Measure in Task 3; report, do not trim |
| A tier 2 row fails on the hand-written plan file, for example a subtask list shorter than its method or a binding that disagrees with the compound's | Low: the spec walked the tree | The criterion 5 script is written in Task 3, not Task 4, so a mismatch is fixed with the file it is in |

## Parallelisation

None. Four sequential tasks on one schema file.

## Open Questions

None. The plan review of 2026-09-18 settled two: the spec's `position` slot collided with common's `Position` class in the generated docs, resolved by decision 6, which dropped the slot with the shape it belonged to; and the catalogue tasks share a base `Task` as the instances share `TaskInstance`, decision 18, with `primitive_task`, `compound_task`, and the `Subtask` rule unchanged.
