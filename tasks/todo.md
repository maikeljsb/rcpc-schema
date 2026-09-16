# Tasks: product

Plan: `tasks/plan.md`. Spec: `SPEC-product.md`. Each task is one Conventional Commit, with rebuilt `dist/` and `docs/model/` in the same commit as any schema change. `uv run pytest` passes before every commit. The extractor is `examples/ifc_models/extract_product_examples.py`, in the gitignored folder beside the IFC file it reads, run from the repository root as

```
uv run --with ifcopenshell==0.8.5 --with shapely --with numpy python examples/ifc_models/extract_product_examples.py
```

It reads `examples/ifc_models/20260907_1713.ifc` and rewrites the four files under `examples/product/`. `examples/ifc_models/` is gitignored, so neither file is ever added to git.

## Task 1: `Storey`, `Space`, and `RecordSource`, end to end

**Description:** Create `schema/product.yaml` with the header from the spec, the `RecordSource` enum, and the `Storey` and `Space` classes with their slots: `name`, `long_name`, `source`, `contained_in`, `elevation` declared here with the spec's descriptions and ranges, `id` reused from common with the GlobalId pattern set in each class's `slot_usage`. Write the extractor's first version: storeys with `id`, `name`, `long_name` when present, `elevation` in `m`; parsed Spaces with `id`, `name`, `long_name`, `source: ifc`, `contained_in` from the aggregating storey; one derived exterior Space per storey with a minted id, `name: exterior <storey name>`, `source: derived`, `contained_in` that storey. Copy one real Space and one real Storey into the two invalid documents and break them. Add four rows to `EXAMPLES`. Rebuild and commit as `feat(product): add Storey and Space`.

**Acceptance criteria:**
- [x] `uv run linkml-lint schema/product.yaml` reports no problems; `linkml-validate -C Storey` accepts `storeys.yaml` with 4 records and `-C Space` accepts `spaces.yaml` with 25
- [x] `invalid/space_missing_source.yaml` fails naming `source`; `invalid/storey_id_not_global_id.yaml` fails naming `id`
- [x] `dist/product.schema.json` declares draft 2020-12, has `pattern` on `id` in `Storey` and `Space`, and its `$defs` hold those two, `RecordSource`, and common's five

**Verification:**
- [x] Tests pass: `uv run pytest` with four new rows collected
- [x] Build succeeds: `uv run python scripts/build.py` run twice; `git status --porcelain` shows only the intended files
- [x] Manual check: `docs/model/product/index.md` lists both classes, the enum, and the five slots with descriptions; `dist/README.md` lists product; no two file names under `docs/model/product/` match case-insensitively

**Dependencies:** None

**Files likely touched:**
- `schema/product.yaml`
- `examples/product/storeys.yaml`, `examples/product/spaces.yaml`
- `examples/product/invalid/space_missing_source.yaml`, `storey_id_not_global_id.yaml`
- `tests/test_examples.py`
- `dist/product.schema.json`, `dist/README.md`, `docs/model/product/*` (generated)

**Estimated scope:** Medium

**Amendment 2026-09-15:** committed as `a48a84b feat(product): add Storey and Space`. Reopened during Task 2 when every slot in the module became a required key (`SPEC-product.md` decision 2): `name`, `long_name`, `elevation` required, empty when the file has none; `Space.contained_in` required with the plain GlobalId pattern. `storeys.yaml`, `spaces.yaml`, and `storey_id_not_global_id.yaml` regenerated, to land with Task 2's commit.

**Amendment 2026-09-16:** reopened again for `record_type` on every class (`SPEC-product.md` decision 16). `storeys.yaml`, `spaces.yaml`, and both existing Space/Storey invalid documents regenerated; a third invalid document, `space_record_type_mismatch.yaml`, added to pin the guarantee, one more row than Task 1 originally planned. To land with Task 3's commit.

## Checkpoint: Phase 1
- [x] `uv run pytest` passes with four product rows collected
- [x] Generated schema checked as above
- [x] Review with human before Task 2

## Task 2: `BuildingComponent`, `ComponentPermanence`, and its one class rule, end to end

**Description:** Add the `ComponentPermanence` enum and the `BuildingComponent` class as the spec's Code Style shows it, declaring `ifc_type`, `material`, `permanence`, `derived_from`, `part_of`, `target_location`, `supply_location`, `current_location`, `located_in`, and reusing common's `length`, `width`, `height`, `weight`. Grow the extractor: every `IfcBuildingElement` except `IfcDoor` and `IfcStair` becomes a record with every key present: `id`, `ifc_type`, `name`, `material` by the lineage rule, `permanence: permanent`, `source: ifc`, `target_location` as the world bounding-box centre in `m`, `part_of` and `contained_in`/`located_in` from the IFC decomposition and containment relations, the empty value wherever a slot does not apply. Add the derived brick and the derived formwork the same way. Copy one real record into each of the five invalid documents and break it. Add six rows. Rebuild and commit as `feat(product): add BuildingComponent with its required-everywhere shape`.

**Acceptance criteria:**
- [x] `building_components.yaml` validates as `BuildingComponent` and holds: at least one IFC-sourced component with a `material`, one `IfcWindow`, one `permanence: temporary`, one `source: derived` whose `derived_from` names a component in the same file, one `part_of` naming the roof in the same file and ten naming the two stair ids
- [x] The five invalid documents fail naming `permanence`, `id`, `ifc_type`, `derived_from` (key removed), `derived_from` (key emptied) respectively
- [x] `dist/product.schema.json` `BuildingComponent` carries a bare `if`/`then` pair (one rule, not wrapped in `allOf`) and every `Position` and `Quantity` slot as a `$ref`

**Verification:**
- [x] Tests pass: `uv run pytest` with six new rows collected; note the wall time of the `building_components.yaml` row
- [x] Build succeeds: `uv run python scripts/build.py` run twice; `git status --porcelain` shows only the intended files
- [x] Manual check: `docs/model/product/BuildingComponent.md` shows a Rules section with one rule table; every key required on `BuildingComponent` is present on all 143 records

**Dependencies:** Task 1

**Files likely touched:**
- `schema/product.yaml`
- `examples/product/building_components.yaml`
- `examples/product/invalid/building_component_missing_permanence.yaml`, `building_component_id_not_global_id.yaml`, `building_component_ifc_missing_ifc_type.yaml`, `building_component_derived_missing_derived_from.yaml`, `building_component_derived_from_empty.yaml`
- `examples/product/storeys.yaml`, `examples/product/spaces.yaml`, `examples/product/invalid/storey_id_not_global_id.yaml`
- `tests/test_examples.py`
- `SPEC-product.md`
- `dist/product.schema.json`, `docs/model/product/*` (generated)

**Estimated scope:** Medium

**Amendment 2026-09-15:** built as the spec's two-rule design, then redesigned in review before committing: every slot in the module is a required key, `""` or a Position/Quantity with `unit: ""` when unresolved; the `ifc_type` rule retired; the `derived_from` rule narrowed to a pattern check. `SPEC-product.md` decisions 2 and 15 (a split by `source`, considered and declined). A fifth invalid document, `building_component_derived_from_empty.yaml`, pins the remaining rule; the criteria above reworded to match. Real counts against the plan's estimate: 143 records, 11 `part_of`, corrected in `tasks/plan.md`. Commit pending review.

**Amendment 2026-09-16:** reopened for `record_type` on every class (`SPEC-product.md` decision 16, reversing the original Boundaries' Never on `designates_type`). `building_components.yaml` and all five invalid documents regenerated. Commit pending review.

## Task 3: `Connector` and `ConnectorKind`, end to end

**Description:** Add the `ConnectorKind` enum and the `Connector` class, `is_a: BuildingComponent`, with `kind`, `connects`, `clear_width`, `clear_height` declared as the spec's slot table states, every slot required in `slot_usage`. Every inherited `BuildingComponent` slot keeps its required-everywhere treatment (Task 2), so each Connector record also carries `ifc_type`, `material`, `derived_from`, `part_of`, `located_in` as keys, `""` where they don't apply. Grow the extractor: the 14 doors as `kind: door` with the component slots, `clear_width` and `clear_height` from `OverallWidth` and `OverallHeight`, `connects` from space boundaries with the exterior Space as the second end when only one Space bounds the door and the footprint-overlap fallback when three do; the 2 stairs as `kind: stair` with `connects` from the flight's lowest and highest vertex against Level 1 and Level 2 Space footprints, no clearances. Print every door or stair the rule did not decide outright and stop if any remains undecided. Copy one real door into each of the two invalid documents and break it. Add three rows. Rebuild and commit as `feat(product): add Connector`.

**Acceptance criteria:**
- [x] `connectors.yaml` validates as `Connector` and holds 14 doors each with both clearances, 4 of them with an exterior Space in `connects`, and 2 stairs whose two Spaces sit on different storeys
- [x] `invalid/connector_one_space.yaml` fails naming `connects`; `invalid/connector_door_missing_clear_height.yaml` fails naming `clear_height`
- [x] `dist/product.schema.json` `Connector.properties` holds every `BuildingComponent` property plus four; `connects` has `minItems: 2` and `maxItems: 2`; `Connector` carries a bare `if`/`then` pair, the inherited `derived_from` rule

**Verification:**
- [x] Tests pass: `uv run pytest` with four new rows collected, fourteen product rows in all
- [x] Build succeeds: `uv run python scripts/build.py` run twice; `git status --porcelain` shows only the intended files
- [x] Manual check: `docs/model/product/index.md` shows `Connector` indented under `BuildingComponent`; no two file names under `docs/model/product/` match case-insensitively

**Dependencies:** Task 2

**Files likely touched:**
- `schema/product.yaml`
- `examples/product/connectors.yaml`
- `examples/product/invalid/connector_one_space.yaml`, `connector_door_missing_clear_height.yaml`, `space_record_type_mismatch.yaml`
- `examples/product/building_components.yaml`, `storeys.yaml`, `spaces.yaml`, and the five `building_component_*`/`space_missing_source`/`storey_id_not_global_id` invalid documents
- `tests/test_examples.py`
- `SPEC-product.md`
- `dist/product.schema.json`, `docs/model/product/*` (generated)

**Estimated scope:** Medium

**Amendment 2026-09-16:** the clearance rule is retired like `ifc_type`'s, `SPEC-product.md` decision 4: with `clear_width` and `clear_height` required keys it checked nothing, and a rule cannot look inside a Quantity, so a door's real clearance is a tier 3 check. `exact_cardinality: 2` on `connects` is inert on LinkML 1.11.1 (the one-Space document validated), so the bound is `minimum_cardinality` plus `maximum_cardinality`, as decision 5 recorded. The three-Space door and both stair lower ends were undecided by the vertex rule alone and resolved by footprint overlap, the brief's fallback; the extractor prints each such decision. `gen-doc` does not render an inherited rule on the subclass page, so the manual check was reworded.

Also reopened the same day for `record_type` on every class (decision 16): `connectors.yaml` and both invalid documents regenerated; the criteria above corrected in place to fourteen rows, counting `space_record_type_mismatch.yaml` added under Task 1. Commit pending review.

## Checkpoint: Phase 2
- [x] Fourteen product rows pass
- [x] Every id named in `connects`, `located_in`, `contained_in`, `derived_from`, and `part_of` exists in one of the four files; every `id` across the four files is distinct
- [ ] Review with human before Task 4

## Task 4: Verify success criteria, push, confirm CI

**Description:** Walk the seven success criteria in `SPEC-product.md` and record evidence for each in this file under a dated "Checkpoint: Complete" section, as the resource module did. Criterion 5's cross-file id check and criterion 6's lineage read-through are done by a one-off script and by reading, each recorded once. Confirm `git log 732ddaf..HEAD -- schema/common.yaml scripts tests/test_build.py tests/test_lint.py tests/test_dist.py` is empty. Push and confirm the CI run passes. Commit the evidence as `docs(plan): mark product complete with the success-criteria evidence`.

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
- [ ] Common and the toolchain untouched by this module
- [ ] Ready for `SPEC-process.md`
