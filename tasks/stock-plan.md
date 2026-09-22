# Implementation Plan: stock

*Extension of module `resource`, specified in `SPEC-stock.md` (Phase 1 decided 2026-09-21). Plan drafted 2026-09-21. Tasks in `tasks/stock-todo.md`. Starts after process Task 5 has recorded its evidence, because process criterion 7 reads the git log of `schema/common.yaml` and `schema/product.yaml`, and this plan changes both.*

## Overview

A quick demo in five commits: the four module specs record the decisions, `ComponentPermanence` and `permanence` move to common, resource gains `Resource` and `Stock` with its stock file, process gains `uses` on `Method` with the in-situ method and the two slab tasks, then verify and push. One module per commit, in import order, so that no slot ever names a class that does not yet exist in the merged schema. Tests and example rows are written before each schema change and fail first.

## Dependency Graph

```
SPEC-common 18, SPEC-product 18, SPEC-resource 14, SPEC-process 20   (Task 1, docs)
    │
common.yaml  ComponentPermanence, permanence   <-  product.yaml loses both   (Task 2)
    │
resource.yaml  Resource, RobotUnit is_a Resource, Stock; stocks.yaml           (Task 3)
    │
process.yaml  uses on Method; catalogue m_insitu; plan two slabs;
              capability_types shutter, tie, pour; robot_units concreter_k1     (Task 4)
    │
verify criteria, push, CI                                                       (Task 5)
```

## Architecture Decisions

- **Specs before schema, as one docs commit.** The four decision entries land first, the pattern of `cafb89e` before `4278422`, so every later commit implements recorded text. `SPEC-process.md`'s plan example is rewritten in place for the network's new name and four tasks.
- **RED before each schema change.** Task 3's two example rows fail with `No such class: Stock`; Task 4's `catalogue.yaml` row fails on the unknown key `uses` before the slot exists, and the reference row is proven RED with a planted unknown stock, then restored.
- **The stock file validates with `-C Stock`, no `record_type`.** Resource files hold one class each, so the split by `record_type` that process needs is not needed here, and `record_type` stays product's and process's.
- **Cross-module example edits ride with process.** `shutter`, `tie`, `pour` in `capability_types.yaml` and `concreter_k1` in `robot_units.yaml` exist only for the in-situ primitives, so they land in Task 4's commit, as `locomote` landed with process prerequisite 2. The schemas of common and resource do not change in that commit.
- **Counts that move.** `dist/common.schema.json` `$defs` 5 to 6; `dist/resource.schema.json` 12 to 13 in Task 2 and 15 in Task 3; `dist/process.schema.json` 32 to 34 in Task 3, unchanged in Task 4; `dist/product.schema.json` unchanged as a set. Test rows: 38 example rows to 40 in Task 3; 12 reference rows to 13 in Task 4.

## Task List

### Phase 1: Record and move
- [x] Task 1: Record the stock decisions in the four module specs
- [x] Task 2: Move `ComponentPermanence` and `permanence` from product to common

### Phase 2: Resource
- [ ] Task 3: `Resource`, `Stock`, and `stocks.yaml`, end to end

### Checkpoint: Resource
- [ ] `uv run pytest` passes with two new rows; `docs/model/resource/index.md` indents `RobotUnit` and `Stock` under `Resource`
- [ ] Review with human before Task 4

### Phase 3: Process
- [ ] Task 4: `uses` on `Method`, the in-situ method, and the two slab tasks

### Phase 4: Close
- [ ] Task 5: Verify the five success criteria, push, confirm CI

### Checkpoint: Complete
- [ ] Every success criterion in `SPEC-stock.md` verified with evidence in `tasks/stock-todo.md`
- [ ] `scripts/` and the toolchain tests untouched; `schema/product.yaml` changed by Task 2 only
- [ ] CI green on the pushed head

## Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| A new name collides case-insensitively with an existing one in the generated docs; Windows hides it, Linux CI fails | High if it happens | Names fixed in the spec: `Resource`, `Stock`, `uses`; the SchemaView scan of process Task 4 rerun in Tasks 3 and 4 |
| `RobotUnit` gaining `is_a: Resource` changes its JSON Schema or docs beyond the index indent | Medium: resource criterion 2 of `SPEC-resource.md` names its `$defs` | Task 3 diffs `RobotUnit` in `dist/resource.schema.json` before and after; only `$defs` entries may differ |
| `uses` as a slot name means something to LinkML | Low: lint would say so | `linkml-lint` in Task 4 before the build |
| Moving `permanence` changes product's JSON Schema in content | Low | Task 2 diffs `dist/product.schema.json` against HEAD and expects no change |

## Open Questions

None. Decision 8 of `SPEC-stock.md` keeps product and resource separate.
