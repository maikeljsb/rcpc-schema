# Tasks: toolchain

Plan: `tasks/plan.md`. Spec: `SPEC-toolchain.md`. Each task is one Conventional Commit.

## Task 1: Bootstrap the uv project

**Description:** Create the Python project so that `uv sync` on a clean clone produces an environment with LinkML, pytest, jsonschema, and PyYAML, and `uv run pytest` runs. No tests exist yet beyond a conftest fixture, so pytest's "no tests collected" exit is acceptable for this task only.

**Acceptance criteria:**
- [x] `.python-version` says `3.12`; `pyproject.toml` declares `requires-python = ">=3.12"`, dependencies `linkml`, `pytest`, `jsonschema`, `pyyaml`, and `[tool.pytest.ini_options] testpaths = ["tests"]`
- [x] `uv.lock` is committed and `uv sync` completes from a clean checkout
- [x] `uv run linkml-lint --help`, `uv run gen-json-schema --help`, `uv run gen-doc --help`, `uv run linkml-validate --help` all exit 0

**Verification:**
- [x] `uv sync && uv run python -c "import linkml, jsonschema, yaml, pytest"` exits 0
- [x] Manual check: `uv.lock` pins one `linkml` version, 1.11.1 (the spec's "1.9.x" was an assumption about the current release, corrected to "latest 1.x")

**Dependencies:** None

**Files likely touched:**
- `.python-version`
- `pyproject.toml`
- `uv.lock`
- `tests/conftest.py`

**Estimated scope:** Small

## Task 2: Fixture schema, fixture instances, and the example validation test

**Description:** Write the minimal LinkML schema the harness proves itself on, two valid instances and one invalid instance of its top class, and `tests/test_examples.py` with the `EXAMPLE_TARGETS` dictionary mapping each example path to its target class. This is also the early test that `linkml-validate` accepts a top-level YAML list, which the whole example convention depends on.

**Acceptance criteria:**
- [ ] `tests/fixtures/minimal.yaml` lints clean and defines: an identified top class with a required reference slot to a second identified class, an inlined value-object slot to a third class with no identifier, and one enum-ranged slot; every element has a description
- [ ] `tests/fixtures/minimal_instances.yaml` is a top-level list of two instances and validates against the top class; `tests/fixtures/minimal_invalid.yaml` omits a required slot and fails with a message naming that slot
- [ ] `tests/test_examples.py` validates every path in `EXAMPLE_TARGETS`, expects every path under an `invalid/` folder to fail naming the slot, and is written so that domain modules only add rows
- [ ] Validation runs by shelling out to `linkml-validate`, consistent with the build script; the offending slot name is read from the CLI's output. Only if that text proves brittle does the test fall back to `linkml.validator.validate()` from Python, and the fallback is recorded in `tasks/plan.md` under Architecture Decisions

**Verification:**
- [ ] Tests pass: `uv run pytest tests/test_examples.py`
- [ ] Manual check: `uv run linkml-validate -s tests/fixtures/minimal.yaml -C <TopClass> tests/fixtures/minimal_instances.yaml` reports no errors, proving the CLI accepts a list

**Dependencies:** Task 1

**Files likely touched:**
- `tests/fixtures/minimal.yaml`
- `tests/fixtures/minimal_instances.yaml`
- `tests/fixtures/minimal_invalid.yaml`
- `tests/test_examples.py`

**Estimated scope:** Medium

## Checkpoint: Phase 1
- [ ] `uv run pytest` passes
- [ ] `linkml-validate` accepts a top-level list, or the example convention is revised and the spec amended
- [ ] Review with human before Task 3

## Task 3: Write `tests/test_build.py`, failing

**Description:** One test per rule in the spec's build description, written before the script exists, so the script is built to the tests. Each test copies `scripts/build.py` and a chosen `schema/` content into a temporary directory tree and runs the script there via `subprocess`, so the committed `dist/` and `docs/model/` are never touched.

**Acceptance criteria:**
- [ ] Six tests exist and all fail because `scripts/build.py` is absent: 2020-12 declared; meta-schema passes; `docs/model/minimal/index.md` created; `dist/README.md` names `minimal.schema.json` and contains the fixture's description; a pre-seeded `dist/ghost.schema.json` is removed; empty `schema/` exits 0 with a README saying no modules exist and `docs/model/` untouched
- [ ] Tests are plain functions with plain asserts and a shared helper that builds the temp tree

**Verification:**
- [ ] `uv run pytest tests/test_build.py` reports 6 failed, 0 passed, 0 errors in collection

**Dependencies:** Task 2

**Files likely touched:**
- `tests/test_build.py`

**Estimated scope:** Small

## Task 4: Write `scripts/build.py` until the build tests pass

**Description:** Implement the six build rules from the spec: JSON Schema per module with the `$schema` rewrite, docs per module with imports not merged, generated `dist/README.md`, stale-output removal, empty-schema no-op, fail fast with the generator's message. Standard library plus PyYAML, explicit UTF-8 everywhere, under sixty lines. This task also answers the spec's open question about `gen-doc` with imports not merged, by looking at the fixture's rendered docs.

**Acceptance criteria:**
- [ ] `uv run pytest tests/test_build.py` reports 6 passed
- [ ] `wc -l scripts/build.py` is under 60; imports are only `pathlib`, `json`, `shutil`, `subprocess`, `sys`, `yaml`
- [ ] The fixture's `docs/model/minimal/index.md` reads sensibly, or the fallback (merged docs, one folder) is taken and both spec and tests are amended in this same task

**Verification:**
- [ ] Tests pass: `uv run pytest tests/test_build.py`
- [ ] Manual check: open the generated fixture docs and confirm links to the fixture's own classes resolve

**Dependencies:** Task 3

**Files likely touched:**
- `scripts/build.py`
- `SPEC-toolchain.md` (only if the docs fallback is taken)
- `tests/test_build.py` (only if the docs fallback is taken)

**Estimated scope:** Small

## Checkpoint: Phase 2
- [ ] All build tests pass
- [ ] Docs layout decision recorded (per-module as specified, or fallback with spec amended)
- [ ] Review with human before Task 5; go-ahead for the push in Task 6

## Task 5: Domain-module hooks, directory skeleton, and the first real build

**Description:** Add the two tests that domain modules will light up, `test_lint.py` over `schema/*.yaml` and `test_dist.py` comparing committed `dist/` and `docs/model/` to a fresh build and meta-checking every `dist/*.schema.json`; create `schema/`, `examples/`, `docs/model/` with `.gitkeep`; run the real build once so `dist/README.md` exists saying no modules exist; confirm the whole suite passes and the tree is clean after a rebuild.

**Acceptance criteria:**
- [ ] `tests/test_lint.py` and `tests/test_dist.py` parametrise over the real directories and skip cleanly when they are empty
- [ ] `schema/.gitkeep`, `examples/.gitkeep`, `docs/model/.gitkeep` exist; `dist/README.md` is the generated no-modules README
- [ ] `uv run pytest` passes; running `uv run python scripts/build.py` afterwards leaves `git status` clean

**Verification:**
- [ ] Tests pass: `uv run pytest`
- [ ] Build succeeds: `uv run python scripts/build.py && git status --porcelain` prints nothing

**Dependencies:** Task 4

**Files likely touched:**
- `tests/test_lint.py`
- `tests/test_dist.py`
- `schema/.gitkeep`, `examples/.gitkeep`, `docs/model/.gitkeep`
- `dist/README.md`

**Estimated scope:** Medium

## Task 6: CI workflow, push, passing run

**Description:** One GitHub Actions workflow, one job on `ubuntu-latest`: check out, install uv with the official action and caching, `uv sync`, `uv run pytest`. Push the branch after explicit go-ahead and watch the run until it passes.

**Acceptance criteria:**
- [ ] `.github/workflows/ci.yml` triggers on push and pull request, has exactly one job, and runs only `uv sync` and `uv run pytest`
- [ ] The run on the pushed commit passes
- [ ] Every success criterion in `SPEC-toolchain.md` is ticked with evidence

**Verification:**
- [ ] Manual check: `gh run list --limit 1` shows the run as completed, success
- [ ] Manual check: `SPEC-toolchain.md` success criteria 1 to 6 each verified once

**Dependencies:** Task 5, and go-ahead for the push

**Files likely touched:**
- `.github/workflows/ci.yml`

**Estimated scope:** Small

## Checkpoint: Complete
- [ ] All six tasks committed, one commit each
- [ ] CI passes on the last commit
- [ ] `schema/` holds only `.gitkeep`; ready for `SPEC-common.md`
