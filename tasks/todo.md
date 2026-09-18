# Tasks: process

Plan: `tasks/plan.md`. Spec: `SPEC-process.md`. Each task is one Conventional Commit, with rebuilt `dist/` and `docs/model/` in the same commit as any schema change. `uv run pytest` passes before every commit. The plan checkbox commit is always separate from the schema commit. Every example file is written by hand; there is no extractor.

## Task 1: `Task` with `PrimitiveTask` and `CompoundTask`, `Parameter`, and `ParameterKind`, end to end

**Description:** Create `schema/process.yaml` with the header from the spec, the `ParameterKind` enum with `component`, `location`, `robot`, and the classes `Parameter` (`parameter_name` as key, `parameter_kind`, `applies_to`), `Task` (`record_type`, `id` with the name pattern, `description`, `parameters`, all required in `slot_usage`), `PrimitiveTask` (`is_a: Task`, adding `requires` and `duration`, `duration` required), and `CompoundTask` (`is_a: Task`, adding nothing); declare `parameters`, `parameter_name`, `parameter_kind`, `applies_to`, `requires`, and `duration` as the slot table states. Write `examples/process/catalogue.yaml` with the four primitives and two compound tasks as the spec's excerpt shows them: `MoveTo {r, to}` requires `[locomote]`, 120 s; `Attach {r, c, at}` and `Detach {r, c, at}` each require `[grip]`; `Place {r, c, at}` requires `[lift, align]`, 180 s; `Transport {c}` and `ConstructComponent {c}`. Copy one real record into each of the five invalid documents and break it. Add six rows. Rebuild and commit as `feat(process): add PrimitiveTask and CompoundTask`.

**Acceptance criteria:**
- [x] `uv run linkml-lint schema/process.yaml` reports no problems; the `catalogue.yaml` row validates through the split with two groups
- [x] The five invalid documents fail naming `duration`, `requires`, `id`, `parameters`, `record_type` respectively
- [x] `dist/process.schema.json` declares draft 2020-12; `requires` carries `minItems: 1`; `parameters` is an object whose `additionalProperties` is an `anyOf` of the `Parameter` object and its one-line value; `record_type` is an `enum` of one value in `Task` and in each subclass, the subclass's own name; both subclasses list the four inherited slots and the `id` pattern in their properties

**Verification:**
- [x] Tests pass: `uv run pytest` with six new rows collected
- [x] Build succeeds: `uv run python scripts/build.py` run twice; `git status --porcelain` shows only the intended files
- [x] Manual check: `docs/model/process/index.md` lists the four classes with `PrimitiveTask` and `CompoundTask` indented under `Task`, the enum, and the six slots with descriptions; `dist/README.md` lists process

**Dependencies:** None

**Files likely touched:**
- `schema/process.yaml`
- `examples/process/catalogue.yaml`
- `examples/process/invalid/primitive_task_missing_duration.yaml`, `primitive_task_requires_empty.yaml`, `primitive_task_id_not_a_name.yaml`, `primitive_task_parameter_unknown_kind.yaml`, `compound_task_record_type_mismatch.yaml`
- `tests/test_examples.py`
- `dist/process.schema.json`, `dist/README.md`, `docs/model/process/*` (generated)

**Estimated scope:** Medium

## Task 2: `Method` and `Subtask` with its rule, end to end

**Description:** Add `Method` and `Subtask` as the spec's Code Style block shows them, declaring `compound_task`, `primitive_task`, `subtasks`, `ordering`, and `arguments`, and the one class rule on `Subtask` with its precondition on `arguments`. Append `m_transport` and `m_prefab` to `catalogue.yaml` exactly as the spec's excerpt writes them, `m_prefab`'s `c` in the full form with `applies_to: ["Basic Wall:Exterior - Brick on Block"]`. Copy `m_transport` into each of the four invalid documents and break it. Add four rows. Rebuild and commit as `feat(process): add Method with its subtasks and ordering`.

**Acceptance criteria:**
- [ ] `catalogue.yaml` validates through the split with three groups and eight records
- [ ] The four invalid documents fail naming `parameter_kind`, `subtasks`, `subtasks`, `ordering` respectively; the two-task document's message contains `/subtasks/`
- [ ] `dist/process.schema.json` `Subtask` carries a bare `if`/`then`; `subtasks` carries `minItems: 1`; the string `"null"` occurs exactly once, inside `Method.ordering.items.type`

**Verification:**
- [ ] Tests pass: `uv run pytest` with four new rows collected, ten process rows in all
- [ ] Build succeeds: `uv run python scripts/build.py` run twice; `git status --porcelain` shows only the intended files
- [ ] Manual check: `docs/model/process/Subtask.md` shows a Rules table with the rule's description; `Method.md` lists `ordering` with its description

**Dependencies:** Task 1

**Files likely touched:**
- `schema/process.yaml`
- `examples/process/catalogue.yaml`
- `examples/process/invalid/method_parameter_missing_kind.yaml`, `method_subtask_names_two_tasks.yaml`, `method_subtasks_empty.yaml`, `method_ordering_not_a_list.yaml`
- `tests/test_examples.py`
- `dist/process.schema.json`, `docs/model/process/*` (generated)

**Estimated scope:** Medium

## Checkpoint: Phase 1
- [ ] `uv run pytest` passes with ten process rows collected
- [ ] Generated schema checked as above
- [ ] Review with human before Task 3

## Task 3: `TaskInstance` with its two subclasses, `TaskNetwork`, and `Binding`, end to end

**Description:** Add `Binding` (`parameter_name` as key, `bound_to`), `TaskInstance` with `record_type`, `id`, `bindings`, then `CompoundTaskInstance` (`is_a: TaskInstance`, adding `compound_task`, `decomposed_by`, `subtasks`) and `PrimitiveTaskInstance` (`is_a: TaskInstance`, adding `primitive_task`), then `TaskNetwork`; declare `tasks`, `decomposed_by` with its pattern, `bindings`, and `bound_to`, and set `subtasks` on `CompoundTaskInstance` to range `TaskInstance` in `slot_usage`. Every plan-side slot `required: true` in `slot_usage`. Write `examples/process/plan.yaml`: the network `level_1_walls`, the three compound instances with their `subtasks` lists, and the five leaves as the plan's Architecture Decisions fix them, nine records. Copy one real record into each of the two invalid documents and break it. Add three rows. Write the criterion 5 script in the scratchpad and run it against the file before committing. Rebuild and commit as `feat(process): add TaskNetwork and the two instance classes`.

**Acceptance criteria:**
- [ ] `plan.yaml` validates through the split with three groups; it holds one network with two tasks and one ordering pair, a decomposed network task listing two subtasks, a decomposed Transport listing four, an undecomposed network task listing none, and five leaves whose bindings cover all three kinds
- [ ] `invalid/task_network_tasks_empty.yaml` fails naming `tasks`; `invalid/compound_task_instance_missing_subtasks.yaml` fails naming `subtasks`
- [ ] `dist/process.schema.json` `$defs` has 30 entries including `Task`, `TaskInstance`, and `Binding`, none suffixed `__identifier_optional`; both instance classes list `bindings`, `id`, `record_type` in `properties` and `required`, `record_type` an `enum` of the subclass name; `CompoundTaskInstance.subtasks` has string `items`; `tasks` carries `minItems: 1`; `bindings` is an object whose `additionalProperties` is an `anyOf` of the `Binding` object, requiring `bound_to` only, and a string; `"null"` occurs exactly twice

**Verification:**
- [ ] Tests pass: `uv run pytest` with three new rows collected, thirteen process rows in all; note the suite's wall time
- [ ] Build succeeds: `uv run python scripts/build.py` run twice; `git status --porcelain` shows only the intended files
- [ ] Manual check: `docs/model/process/index.md` shows the two instance classes indented under `TaskInstance`; the lowercased names of every class, slot, enum, type, and schema `SchemaView` reports for `schema/process.yaml` with imports are all distinct; the criterion 5 script prints no failing row

**Dependencies:** Task 2

**Files likely touched:**
- `schema/process.yaml`
- `examples/process/plan.yaml`
- `examples/process/invalid/task_network_tasks_empty.yaml`, `compound_task_instance_missing_subtasks.yaml`
- `tests/test_examples.py`
- `dist/process.schema.json`, `docs/model/process/*` (generated)

**Estimated scope:** Medium

## Checkpoint: Phase 2
- [ ] Thirteen process rows pass
- [ ] Every id `plan.yaml` names resolves in `catalogue.yaml`, `plan.yaml`, `examples/product/`, or as `mason_m1_1` or `mason_m1_2`; every instance is listed exactly once, in the network's `tasks` or one compound's `subtasks`
- [ ] Review with human before Task 4

## Task 4: Verify success criteria, push, confirm CI

**Description:** Walk the seven success criteria in `SPEC-process.md` and record evidence for each in this file under a dated "Checkpoint: Complete" section, as product did. Criterion 5 is the script from Task 3, run once more on the committed files; criterion 6 is a read-through of the slot table against `schema/process.yaml`, recorded once. Confirm `git log 689af87..HEAD -- schema/product.yaml schema/resource.yaml tests/test_lint.py tests/test_dist.py` is empty, `git log 689af87..HEAD -- scripts tests/test_build.py` shows only the prerequisite 6 commit, and `git log 689af87..HEAD -- schema/common.yaml examples/resource` shows only the two prerequisite commits. Push and confirm the CI run passes. Commit the evidence as `docs(plan): mark process complete with the success-criteria evidence`.

**Acceptance criteria:**
- [ ] Each of the seven criteria has a line of evidence with the command or file it came from
- [ ] CI is green on the pushed head
- [ ] `tasks/plan.md` checkpoints ticked

**Verification:**
- [ ] Tests pass: `uv run pytest`
- [ ] Build succeeds: `uv run python scripts/build.py && git status --porcelain` prints nothing
- [ ] Manual check: the CI run page shows the same passing count as local

**Dependencies:** Task 3

**Files likely touched:**
- `tasks/todo.md`
- `tasks/plan.md`

**Estimated scope:** Small

## Checkpoint: Complete
- [ ] All four tasks committed
- [ ] CI passes on the last commit
- [ ] Common, product, resource, and the toolchain untouched by this module's four tasks; the toolchain changed by the prerequisite 6 commit only
- [ ] Ready for step 2 of the brief
