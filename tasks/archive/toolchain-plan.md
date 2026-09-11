# Implementation Plan: toolchain

*Module `toolchain` of `CAPABILITY-MAP.md`, specified in `SPEC-toolchain.md`. Plan drafted 2026-09-10, approved 2026-09-11, completed 2026-09-11. Tasks in `tasks/todo.md`.*

## Overview

Stand up the uv project, a fixture LinkML schema that stands in for the domain modules, the build script that turns modules into draft 2020-12 JSON Schema plus per-module docs plus a generated `dist/README.md`, the pytest harness that proves all of that on the fixture and passes with `schema/` empty, and one CI job. When this plan is done, `schema/` contains only `.gitkeep`, and the `common` module can be dropped in with nothing else to build.

## Dependency Graph

```
pyproject.toml + uv.lock + .python-version          (Task 1)
    │
    ├── tests/fixtures/minimal*.yaml                  (Task 2)
    │       │
    │       ├── tests/test_examples.py                (Task 2)  proves linkml-validate on a YAML list
    │       │
    │       └── tests/test_build.py  (failing)        (Task 3)
    │               │
    │               └── scripts/build.py (tests pass) (Task 4)
    │                       │
    │                       ├── tests/test_lint.py, tests/test_dist.py, dir skeleton, real build  (Task 5)
    │                       │
    │                       └── .github/workflows/ci.yml, push, passing run                        (Task 6)
```

Order is bottom-up along the graph. Task 2 sits before the build script on purpose: it is the cheapest place to discover that `linkml-validate` does not accept a top-level YAML list, which would change the example-file convention for every domain module.

## Architecture Decisions

- **Shell out to the LinkML CLIs, never import their API.** A LinkML internal change then breaks the build loudly at the CLI boundary, not silently inside our code. Decided in the spec for the build script; extended here to `tests/test_examples.py`, which calls `linkml-validate` and reads the offending slot from its output. The Python validator API is the fallback only if that output proves brittle, and taking it is recorded here.
- **Subprocess I/O is explicitly UTF-8.** `subprocess.run(..., text=True, encoding="utf-8")` and every `write_text(..., encoding="utf-8", newline="\n")`. Windows defaults to cp1252 and would mangle any non-ASCII character in a description. Not in the spec; added here because the author develops on Windows.
- **PyYAML is declared as a direct dependency** in `pyproject.toml` even though LinkML already pulls it in. We import it, so we declare it. The lockfile is unchanged by this.
- **Build tests run against a temporary copy of the repo layout**, never against the committed `dist/` and `docs/model/`. The build script takes its root from `__file__`, so the tests invoke it through a small indirection: they copy `scripts/build.py` into the temp tree alongside a fake `schema/`. This keeps the script flag-free as the spec requires.
- **Empty parametrisations skip, they do not fail.** `test_lint.py` and `test_dist.py` parametrise over `schema/*.yaml` and `dist/*.schema.json`. With no files, pytest reports them as skipped, and the suite as a whole still has passing tests from `test_build.py` and `test_examples.py`, so the exit code is 0.
- **The fixture schema is a real, small LinkML module.** Three classes: an identified top class with a reference slot to a second identified class and an inlined value-object slot to a third, plus one enum. It exercises every projection-relevant construct the domain modules will use, so if the toolchain handles it, it handles them.

## Task List

### Phase 1: Project boots and validates
- [x] Task 1: Bootstrap the uv project
- [x] Task 2: Fixture schema, fixture instances, and the example validation test

### Checkpoint: Phase 1
- [x] `uv sync` from clean; `uv run pytest` passes
- [x] `linkml-validate` confirmed to accept a top-level YAML list of instances
- [x] Review with human (reviewed in session, 2026-09-11)

### Phase 2: The build
- [x] Task 3: Write `tests/test_build.py`, one failing test per build rule
- [x] Task 4: Write `scripts/build.py` until the build tests pass, under sixty lines

### Checkpoint: Phase 2
- [x] All six build tests pass
- [x] `gen-doc` with imports not merged renders the fixture module sensibly; verified on a two-module probe
- [x] Review with human (reviewed in session, 2026-09-11)

### Phase 3: Domain hooks and CI
- [x] Task 5: Domain-module hooks, directory skeleton, and the first real build
- [x] Task 6: CI workflow, push, passing run

### Checkpoint: Complete
- [x] Every success criterion in `SPEC-toolchain.md` verified and ticked (evidence in `tasks/todo.md`)
- [x] `schema/` holds only `.gitkeep`
- [x] Ready for the `common` module

## Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| `linkml-validate` rejects a top-level YAML list and wants a single object | High: changes the example convention for every domain module | Task 2 tests this first, before any build code. If it fails, the fallback is one instance per file or a thin container class, decided at the Phase 1 checkpoint |
| `gen-doc --no-mergeimports` leaves dangling links to imported classes | Medium: per-module docs read badly | Spec open question; checked in Task 4 on the fixture. Fallback: merged docs in one folder, spec amended |
| Windows console encoding mangles generator output | Medium: corrupt `dist/` files | Explicit UTF-8 on every subprocess and file write; the meta-schema test would also catch invalid JSON |
| `gen-json-schema` output uses a construct that changed between drafts 2019-09 and 2020-12 | Medium: rewritten file fails the meta-schema | That is exactly what `test_fixture_passes_metaschema` detects; if it fires, the fix is a targeted transform in the build, and the spec is amended |
| LinkML install is slow in CI | Low: minutes, not failure | uv caching via the official `setup-uv` action |
| `pytest` exits 5 when it collects zero tests | Low, but would fail CI | Skipped parametrisations plus the always-present build and example tests keep the count above zero |

## Parallelisation

None worth taking. The chain is short and each task is under an hour. Tasks 5 and 6 could be split across sessions but gain nothing from it.

## Open Questions

- Pushing to `github.com/maikeljsb/rcpc-schema` is outward-facing. Task 6 pushes only after explicit go-ahead at the Phase 2 checkpoint.
- Should the CI workflow also run on a schedule to catch upstream LinkML changes? Defaulting to no; push and pull request only, as the spec says.
