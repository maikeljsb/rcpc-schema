# Tasks: resource

Plan: `tasks/plan.md`. Spec: `SPEC-resource.md`. Each task is one Conventional Commit, with rebuilt `dist/` and `docs/model/` in the same commit as any schema change. `uv run pytest` passes before every commit.

## Task 1: Add the four dimension slots to common

**Description:** Declare `length`, `width`, `height`, `weight` in `schema/common.yaml` under `slots:`, each `range: Quantity`, `inlined: true`, with a one-sentence description. No class in common lists them. Rebuild and commit YAML with generated outputs as `feat(common): add the four dimension slots`.

**Acceptance criteria:**
- [x] `uv run linkml-lint schema/common.yaml` reports no problems
- [x] `docs/model/common/index.md` lists eleven slots, the four new ones each with a description
- [x] `dist/common.schema.json` `$defs` are unchanged: `CapabilityType`, `ParameterKind`, `Position`, `Quantity`

**Verification:**
- [x] Tests pass: `uv run pytest`
- [x] Build succeeds: `uv run python scripts/build.py && git status --porcelain` prints nothing after the commit
- [x] Manual check: `docs/model/common/weight.md` exists and reads correctly

**Dependencies:** None

**Files likely touched:**
- `schema/common.yaml`
- `dist/common.schema.json`, `docs/model/common/*` (generated)

**Estimated scope:** Small

**Done:** Committed 2026-09-12 as `317eaf0 feat(common): add the four dimension slots`.

## Task 2: `RobotUnit`, `RobotStatus`, and `Activity` with `offers`, end to end

**Description:** Create `schema/resource.yaml` with the header from the spec, the `RobotStatus` enum, the `RobotUnit` class with `id`, `count`, `status`, and `activity`, and the `Activity` class with `id` and `offers` only. Declare `count`, `status`, `activity`, and `offers` as the spec states them. The other three group slots are declared in the task that adds their class, so no range ever names an undeclared class. Write `examples/resource/robot_units.yaml` with two minimal fictional entries, `mason_m1` with `count: 2` and a mobile inspection robot with `count: 1`, each with an `Activity` holding `id` and `offers` drawn from `examples/common/capability_types.yaml`. Write the three invalid documents that need no other group. Add four rows to `EXAMPLES`. Rebuild and commit as `feat(resource): add RobotUnit, RobotStatus and the Activity group`.

**Acceptance criteria:**
- [x] `uv run linkml-lint schema/resource.yaml` reports no problems, and `linkml-validate -C RobotUnit` accepts `robot_units.yaml`
- [x] The three invalid documents fail naming `activity_group`, `count`, and `offers` respectively
- [x] `dist/resource.schema.json` declares draft 2020-12, has `minimum: 1` on `count`, an array of strings for `offers`, a `$ref` for `activity`, and no root `properties`

**Verification:**
- [x] Tests pass: `uv run pytest` with four new rows collected
- [x] Build succeeds: `uv run python scripts/build.py` run twice; `git status --porcelain` clean after the commit
- [x] Manual check: `docs/model/resource/index.md` lists this module's classes, slots, and enum only; `status.md` shows or states the `idle` default; `dist/README.md` lists resource

**Dependencies:** Task 1

**Files likely touched:**
- `schema/resource.yaml`
- `examples/resource/robot_units.yaml`
- `examples/resource/invalid/robot_unit_missing_activity.yaml`, `robot_unit_zero_count.yaml`, `activity_missing_offers.yaml`
- `tests/test_examples.py`
- `dist/resource.schema.json`, `dist/README.md`, `docs/model/resource/*` (generated)

**Estimated scope:** Medium

**Amendment 2026-09-14:** committed 2026-09-12 as `2312d64 feat(resource): add RobotUnit, RobotStatus and the Activity group`, then broke Linux CI (`test_committed_outputs_match_fresh_build`): `RobotUnit`'s group-pointer slot, named `activity`, collided with the `Activity` class on the case-insensitive filesystem this was built on, silently overwriting one generated doc page with the other. Fixed by renaming the slot to `activity_group` throughout — see `SPEC-resource.md` decision 12.

## Checkpoint: Phase 1
- [x] `uv run pytest` passes with four resource rows collected
- [x] Generated schema checked as above
- [x] Review with human before Task 3

## Task 3: `PhysicalProperty`, `Sensor`, `MountPosition`, and the fifth invalid document

**Description:** Add `MountPosition` (the four common slots, all required), `Sensor` (`id` plus five slots), and `PhysicalProperty` (`id`, the 24 attribute slots in lineage order, `sensors`), plus the `physical_property` slot on `RobotUnit`. Declare the new slots with the ranges and units from the lineage table; `sensors` is multivalued, `inlined: true`, `inlined_as_list: true`. Grow both example entries: `mason_m1` gets a `PhysicalProperty` with dimensions, load capacity, and a sensor with `sensor_mount_position`; the inspection robot gets one with a sensor carrying `sensor_site_position`. Add `invalid/robot_unit_group_missing_id.yaml` and its row. Rebuild and commit as `feat(resource): add PhysicalProperty with Sensor and MountPosition`.

**Acceptance criteria:**
- [ ] Both entries validate; the new invalid document fails naming `id`
- [ ] `dist/resource.schema.json` has `sensors` as an array of `$ref` `Sensor`, and `MountPosition` requires all four of its properties
- [ ] Every Physical Property row of the lineage table except Name has its slot declared, with a description

**Verification:**
- [ ] Tests pass: `uv run pytest` with five resource rows collected
- [ ] Build succeeds: `uv run python scripts/build.py && git status --porcelain` clean after the commit
- [ ] Manual check: `docs/model/resource/Sensor.md` lists six slots; `MountPosition.md` states the robot frame

**Dependencies:** Task 2

**Files likely touched:**
- `schema/resource.yaml`
- `examples/resource/robot_units.yaml`
- `examples/resource/invalid/robot_unit_group_missing_id.yaml`
- `tests/test_examples.py`
- `dist/resource.schema.json`, `docs/model/resource/*` (generated)

**Estimated scope:** Medium

## Task 4: `OperationalRequirement`, `Safety`, and Activity's remaining attributes

**Description:** Add `OperationalRequirement` (`id` plus 8 slots) and `Safety` (`id` plus 6 slots) with their two slots on `RobotUnit`, and the 9 remaining `Activity` attribute slots, in lineage order with descriptions and the attribution clauses the spec names for the four bounds and the three merged quantities. Grow `mason_m1` to hold all four groups so the example file matches success criterion 5. Rebuild and commit as `feat(resource): add OperationalRequirement, Safety and the Activity attributes`.

**Acceptance criteria:**
- [ ] Both entries validate; `mason_m1` has all four groups, `count: 2`, and a mounted sensor; the second entry has `count: 1` and a site-positioned sensor
- [ ] Every row of the lineage table is covered: 51 attribute slots across the four groups and `Sensor`, plus `id` and `offers`
- [ ] Every id in `offers` across both entries appears in `examples/common/capability_types.yaml`

**Verification:**
- [ ] Tests pass: `uv run pytest`
- [ ] Build succeeds: `uv run python scripts/build.py && git status --porcelain` clean after the commit
- [ ] Manual check: read `schema/resource.yaml` top to bottom against the lineage table; every slot in the table order, no extra slot

**Dependencies:** Task 3

**Files likely touched:**
- `schema/resource.yaml`
- `examples/resource/robot_units.yaml`
- `dist/resource.schema.json`, `docs/model/resource/*` (generated)

**Estimated scope:** Medium

## Checkpoint: Phase 2
- [ ] All 56 lineage rows have their slot in `schema/resource.yaml`
- [ ] Example file matches success criterion 5
- [ ] Review with human before Task 5

## Task 5: Verify success criteria, push, confirm CI

**Description:** Walk the seven success criteria in `SPEC-resource.md` and record evidence for each in this file under a dated "Checkpoint: Complete" section, as the common module did. Confirm `git log -- scripts tests/test_build.py tests/test_lint.py tests/test_dist.py` shows no commit from this module and `git log -- schema/common.yaml` shows only Task 1. Push and confirm the CI run passes. Commit the evidence as `docs(plan): mark resource complete with the success-criteria evidence`.

**Acceptance criteria:**
- [ ] Each of the seven criteria has a line of evidence with the command or file it came from
- [ ] CI is green on the pushed head
- [ ] `tasks/plan.md` checkpoints ticked

**Verification:**
- [ ] Tests pass: `uv run pytest`
- [ ] Build succeeds: `uv run python scripts/build.py && git status --porcelain` clean
- [ ] Manual check: the CI run page shows the same passing count as local

**Dependencies:** Task 4

**Files likely touched:**
- `tasks/todo.md`
- `tasks/plan.md`

**Estimated scope:** Small

## Checkpoint: Complete
- [ ] All five tasks committed
- [ ] CI passes on the last commit
- [ ] Common changed only in Task 1; toolchain untouched
- [ ] Ready for `SPEC-product.md`
