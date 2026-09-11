# Tasks: common

Plan: `tasks/plan.md`. Spec: `SPEC-common.md`. Each task is one Conventional Commit, with rebuilt `dist/` and `docs/model/` in the same commit as any schema change.

## Task 1: `CapabilityType` through the whole pipeline

**Description:** Write `schema/common.yaml` with its header, the shared slots `id`, `label`, `description`, and the `CapabilityType` class; migrate the ten reference capability types into `examples/common/capability_types.yaml` with "element" replaced by "component"; add one invalid example missing its `id`; add the two rows to `EXAMPLES`; run the build; commit YAML, examples, test rows, and generated outputs together.

**Acceptance criteria:**
- [x] `uv run linkml-lint schema/common.yaml` reports no problems
- [x] `examples/common/capability_types.yaml` validates against `CapabilityType`, holds exactly four entries (locomote, grip, lift, align; reduced from ten and renamed to bare verbs on 2026-09-11, vocabulary open for improvement) with `id`, `label`, `description`, and contains no occurrence of the word "element"; `examples/common/invalid/capability_type_missing_id.yaml` fails naming `id`
- [x] After `uv run python scripts/build.py`: `dist/common.schema.json`, `docs/model/common/index.md` exist and `dist/README.md` lists common with its description

**Verification:**
- [x] Tests pass: `uv run pytest` with `test_lint.py` and `test_dist.py` no longer skipped (13 passed, 0 skipped)
- [x] Build succeeds: `uv run python scripts/build.py && git status --porcelain` prints nothing after the commit
- [x] Manual check: `docs/model/common/CapabilityType.md` reads correctly on disk; three slots, cardinality 1 each

**Dependencies:** None

**Files likely touched:**
- `schema/common.yaml`
- `examples/common/capability_types.yaml`
- `examples/common/invalid/capability_type_missing_id.yaml`
- `tests/test_examples.py`
- `dist/common.schema.json`, `dist/README.md`, `docs/model/common/*` (generated)

**Estimated scope:** Medium

## Checkpoint: Phase 1
- [x] `uv run pytest` passes with common's lint, two example rows, drift, and meta-schema tests all collected
- [ ] Review with human before Task 2

## Task 2: Value types, `MaterialName`, and `ParameterKind`

**Description:** Add `Position` (x, y, z float, required), `Quantity` (value float required, unit string required), the `MaterialName` string type, and the `ParameterKind` enum with `position`, `component_reference`, `quantity`, each with descriptions as specified. Rebuild. Inspect the generated schema to confirm on the real module what the probe showed: no root `properties`, `$defs` holding the three classes and the enum, the type inlined.

**Acceptance criteria:**
- [ ] `uv run linkml-lint schema/common.yaml` reports no problems; `schema/common.yaml` contains no `tree_root`
- [ ] `dist/common.schema.json` has no root `properties` key, and its `$defs` keys are exactly `Position`, `Quantity`, `CapabilityType`, `ParameterKind`; `MaterialName` is inlined as a string on the slots that use it
- [ ] `docs/model/common/index.md` lists three classes, eight slots, one enum, and `MaterialName` under types

**Verification:**
- [ ] Tests pass: `uv run pytest`
- [ ] Build succeeds: `uv run python scripts/build.py && git status --porcelain` prints nothing after the commit
- [ ] Manual check: `python -c` over `dist/common.schema.json` prints the `$defs` keys and confirms no root `properties`

**Dependencies:** Task 1

**Files likely touched:**
- `schema/common.yaml`
- `dist/common.schema.json`, `dist/README.md`, `docs/model/common/*` (generated)

**Estimated scope:** Small

## Task 3: Verify success criteria, push, confirm CI

**Description:** Walk the seven success criteria in `SPEC-common.md` and record evidence for each in this file's Checkpoint: Complete. Confirm no commit in this module touched `scripts/`, `tests/test_build.py`, `tests/test_lint.py`, or `tests/test_dist.py`. Push and confirm the CI run passes. Criterion 6, another team's check, is recorded as pending, not blocking.

**Acceptance criteria:**
- [ ] Criteria 1 to 5 and 7 verified with a command and its output noted; criterion 6 marked pending
- [ ] `git log --oneline <first common commit>^..HEAD -- scripts tests/test_build.py tests/test_lint.py tests/test_dist.py` prints nothing
- [ ] CI run on the pushed commit passes

**Verification:**
- [ ] Manual check: `gh run watch <id> --exit-status` exits 0
- [ ] Manual check: evidence recorded under Checkpoint: Complete below

**Dependencies:** Task 2, and the push permission noted in `tasks/plan.md`

**Files likely touched:**
- `tasks/todo.md`, `tasks/plan.md` (bookkeeping)

**Estimated scope:** Small

## Checkpoint: Complete
- [ ] All three tasks committed
- [ ] CI passes on the last commit
- [ ] Toolchain untouched
- [ ] Ready for `SPEC-product.md` and `SPEC-resource.md`
