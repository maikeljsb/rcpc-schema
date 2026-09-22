# Tasks: stock

Plan: `tasks/stock-plan.md`. Spec: `SPEC-stock.md`. Each task is one Conventional Commit, with rebuilt `dist/` and `docs/model/` in the same commit as any schema change. `uv run pytest` passes before every commit. The plan checkbox commit is always separate. Starts after process Task 5.

## Task 1: Record the stock decisions in the four module specs

**Description:** Write, in place, `SPEC-common.md` decision 18 (`ComponentPermanence` and `permanence` arrive from product), `SPEC-product.md` decision 18 (they leave; `BuildingComponent` keeps `permanence` required), `SPEC-resource.md` decision 14 (`ResourceEntry` base with `id` and `count`, `RobotUnit` is_a it, `Stock` with `permanence`; class table and project structure updated), and `SPEC-process.md` decision 20 (`uses` on `Method`, range `Stock`, optional; slot table row; the plan example's network renamed `level_1` with four tasks; the catalogue example's third method). Each entry points at `SPEC-stock.md`. Commit as `docs(spec): record the stock extension in the four module specs`.

**Acceptance criteria:**
- [x] Each of the four specs has its new numbered decision, and its class or slot table shows the new element
- [x] `SPEC-process.md`'s plan example reads `level_1` and lists four tasks with `ordering: [[1, 2]]`
- [x] No amendment notes: existing text rewritten where it changes

**Verification:**
- [x] Manual check: `grep -n "SPEC-stock" SPEC-*.md` shows the four pointers

**Dependencies:** process Task 5 recorded

**Files likely touched:**
- `SPEC-common.md`, `SPEC-product.md`, `SPEC-resource.md`, `SPEC-process.md`

**Estimated scope:** Small

## Task 2: Move `ComponentPermanence` and `permanence` from product to common

**Description:** Add the enum and the slot to `schema/common.yaml`, wording unchanged; remove both from `schema/product.yaml`, keeping `permanence` in `BuildingComponent`'s slot list and `slot_usage` with `required: true`. No example changes. Rebuild and commit as `refactor(common): move ComponentPermanence and permanence from product`.

**Acceptance criteria:**
- [x] `dist/common.schema.json` `$defs` has 6 entries including `ComponentPermanence`; `dist/resource.schema.json` has 13; `dist/product.schema.json` `$defs` is the same set as at HEAD and `BuildingComponent.required` still lists `permanence`
- [x] `git diff HEAD -- dist/product.schema.json` shows no change in content (two enum definitions swap order inside `$defs`)

**Verification:**
- [x] Tests pass: `uv run pytest`, same count as before
- [x] Build succeeds: `uv run python scripts/build.py` run twice; `git status --porcelain` shows only the intended files
- [x] Manual check: `docs/model/common/index.md` lists `ComponentPermanence` and `permanence`

**Dependencies:** Task 1

**Files likely touched:**
- `schema/common.yaml`, `schema/product.yaml`
- `dist/*.schema.json`, `docs/model/*` (generated)

**Estimated scope:** Small

## Task 3: `ResourceEntry`, `Stock`, and `stocks.yaml`, end to end

**Description:** Write `examples/resource/stocks.yaml` with `formwork_panels` (count 8, temporary) and `rebar` (count 10, permanent), and `invalid/stock_missing_permanence.yaml`, a copy of one record without its `permanence`. Add two rows to `tests/test_examples.py` and run them: RED with `No such class: Stock`. Then in `schema/resource.yaml`: `ResourceEntry` with `id` and `count`, `count` moved off `RobotUnit` into the base; `RobotUnit` gains `is_a: Resource` and drops `id` and `count` from its own list; `Stock` is_a `ResourceEntry` with `permanence` required and the `id` pattern, descriptions from the spec. Rebuild and commit as `feat(resource): add Resource as the base and Stock beside RobotUnit`.

**Acceptance criteria:**
- [x] `stocks.yaml` validates with `-C Stock`; the invalid document fails naming `permanence`
- [x] `dist/resource.schema.json` `$defs` has 15 entries including `ResourceEntry` and `Stock`; `Stock.required` is `count`, `id`, `permanence`; `RobotUnit.properties` and `RobotUnit.required` are unchanged from HEAD; `dist/process.schema.json` `$defs` has 34
- [x] `docs/model/resource/index.md` indents `RobotUnit` and `Stock` under `ResourceEntry`

**Verification:**
- [x] Tests pass: `uv run pytest` with two new rows, 40 example rows
- [x] Build succeeds: `uv run python scripts/build.py` run twice; `git status --porcelain` shows only the intended files
- [x] Manual check: the lowercased names `SchemaView` reports for `schema/process.yaml` with imports are all distinct

**Dependencies:** Task 2

**Files likely touched:**
- `schema/resource.yaml`
- `examples/resource/stocks.yaml`, `examples/resource/invalid/stock_missing_permanence.yaml`
- `tests/test_examples.py`
- `dist/*.schema.json`, `docs/model/*` (generated)

**Estimated scope:** Medium

Amendment 2026-09-22: the base is `ResourceEntry`, because `Resource` collides case-insensitively with the schema page `resource.md`; see `SPEC-stock.md` decision 4.

## Checkpoint: Resource
- [x] 40 example rows pass
- [x] Review with human before Task 4

## Task 4: `uses` on `Method`, the in-situ method, and the two slab tasks

**Description:** Add `shutter`, `tie`, `pour` to `examples/common/capability_types.yaml` and `concreter_k1` (count 1, `activity_group` offering `locomote`, `shutter`, `tie`, `pour`) to `examples/resource/robot_units.yaml`. Add to `examples/process/catalogue.yaml` the primitives `Formwork`, `Reinforce`, `Concrete` (`{r: robot, c: component, at: location}`, one requirement each, durations 14400, 10800, 7200 s) and `m_insitu` as the spec writes it, with `uses: [formwork_panels, rebar]`. In `plan.yaml` rename the network `level_1`, append the slabs `2O2Fr$t4X7Zf8NOew3FK4F` and `2O2Fr$t4X7Zf8NOew3FKcz` as tasks 3 and 4, `ordering` unchanged, and add their two undecomposed `CompoundTaskInstance` records. Add the reference row `catalogue.yaml` `uses` to `stocks.yaml`; plant an unknown stock, see it fail naming the value, restore. Run the catalogue row: RED on the unknown key `uses`. Then in `schema/process.yaml`: `uses` declared with range `Stock`, multivalued, added to `Method`'s slot list, optional. Rebuild and commit as `feat(process): add uses on Method with the in-situ concreting example`.

**Acceptance criteria:**
- [ ] `catalogue.yaml` holds 12 records and `plan.yaml` 11, both validating through the split; every `uses`, `requires`, `offers`, `compound_task`, and `applies_to` resolves
- [ ] `dist/process.schema.json` `$defs` still has 34 entries; `Method.properties.uses` is an array of strings and `Method.required` does not list it; `"null"` occurs exactly twice
- [ ] `concreter_k1` offers every word `Formwork`, `Reinforce`, and `Concrete` require, checked by a one-line script

**Verification:**
- [ ] Tests pass: `uv run pytest` with 13 reference rows
- [ ] Build succeeds: `uv run python scripts/build.py` run twice; `git status --porcelain` shows only the intended files
- [ ] Manual check: `uv run linkml-lint schema/process.yaml` clean; the SchemaView name scan clean; `docs/model/process/Method.md` lists `uses`

**Dependencies:** Task 3

**Files likely touched:**
- `schema/process.yaml`
- `examples/process/catalogue.yaml`, `examples/process/plan.yaml`
- `examples/common/capability_types.yaml`, `examples/resource/robot_units.yaml`
- `tests/test_references.py`
- `dist/process.schema.json`, `docs/model/process/*` (generated)

**Estimated scope:** Medium

## Task 5: Verify success criteria, push, confirm CI

**Description:** Walk the five success criteria in `SPEC-stock.md` and record one line of evidence each under a dated "Checkpoint: Complete" here. Push and confirm the CI run passes. Commit as `docs(plan): mark the stock extension complete with its evidence`.

**Acceptance criteria:**
- [ ] Each criterion has a line of evidence with the command or file it came from
- [ ] CI is green on the pushed head
- [ ] `tasks/stock-plan.md` checkpoints ticked

**Verification:**
- [ ] Tests pass: `uv run pytest`
- [ ] Build succeeds: `uv run python scripts/build.py && git status --porcelain` prints nothing
- [ ] Manual check: the CI run page shows the same passing count as local

**Dependencies:** Task 4

**Files likely touched:**
- `tasks/stock-todo.md`, `tasks/stock-plan.md`

**Estimated scope:** Small

## Checkpoint: Complete
- [ ] All five tasks committed
- [ ] CI passes on the last commit
- [ ] `scripts/` and the toolchain tests untouched; `schema/product.yaml` changed by Task 2 only
