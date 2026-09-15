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
- [x] Tests pass: `uv run pytest` with four new rows collected (34 passed)
- [x] Build succeeds: `uv run python scripts/build.py` run twice; `git status --porcelain` shows only the intended files
- [x] Manual check: `docs/model/product/index.md` lists both classes, the enum, and the five slots with descriptions; `dist/README.md` lists product; no two file names under `docs/model/product/` match case-insensitively

**Evidence, 2026-09-15:**
- `uv run linkml-lint schema/product.yaml` → "✓ No problems found"
- `linkml-validate -C Storey examples/product/storeys.yaml` → "No issues found" (4 records); `-C Space examples/product/spaces.yaml` → "No issues found" (25 records: 4 derived exterior + 21 parsed)
- `invalid/space_missing_source.yaml` → `'source' is a required property in /`; `invalid/storey_id_not_global_id.yaml` → `'level-1' does not match '^[0-3][0-9A-Za-z_$]{21}$' in /id`
- `dist/product.schema.json`: `$schema` is the 2020-12 URI; `$defs` = `CapabilityType, Interval, ParameterKind, Position, Quantity, RecordSource, Space, Storey` (common's five plus `RecordSource`, `Space`, `Storey`); both `Storey.properties.id` and `Space.properties.id` carry the GlobalId `pattern`
- `uv run pytest` → 34 passed (four new: `storeys.yaml`, `spaces.yaml`, the two invalid documents)
- `uv run python scripts/build.py` run twice → identical `git status --porcelain` both times (no drift)
- `docs/model/product/index.md` lists `Space` and `Storey` with descriptions, the `RecordSource` enum, and the module's five slots (`contained_in`, `elevation`, `long_name`, `name`, `source`); `dist/README.md` lists `product.schema.json`; the 31 file names under `docs/model/product/` are pairwise distinct case-insensitively

**Dependencies:** None

**Files likely touched:**
- `schema/product.yaml`
- `examples/product/storeys.yaml`, `examples/product/spaces.yaml`
- `examples/product/invalid/space_missing_source.yaml`, `storey_id_not_global_id.yaml`
- `tests/test_examples.py`
- `dist/product.schema.json`, `dist/README.md`, `docs/model/product/*` (generated)

**Estimated scope:** Medium

## Checkpoint: Phase 1
- [x] `uv run pytest` passes with four product rows collected
- [x] Generated schema checked as above
- [x] Review with human before Task 2

Task 1 reviewed and committed 2026-09-15 as `feat(product): add Storey and Space`.

## Task 2: `BuildingComponent`, `ComponentPermanence`, and the two class rules, end to end

**Description:** Add the `ComponentPermanence` enum and the `BuildingComponent` class as the spec's Code Style shows it, declaring `ifc_type`, `material`, `permanence`, `derived_from`, `part_of`, `target_location`, `supply_location`, `current_location`, `located_in`, and reusing common's `length`, `width`, `height`, `weight`. Grow the extractor: every `IfcBuildingElement` except `IfcDoor` and `IfcStair` becomes a record with `id`, `ifc_type`, `name`, `material` by the lineage rule, `permanence: permanent`, `source: ifc`, `target_location` as the world bounding-box centre in `m`, `contained_in` its storey, `located_in` and `contained_in` when the file contains it in a Space; the roof's slab and the stairs' flights, members, and railings carry `part_of` and no `contained_in`. Add the derived brick and the derived formwork as the plan describes. Copy one real record into each of the four invalid documents and break it. Add five rows. Rebuild and commit as `feat(product): add BuildingComponent with its two rules`.

**Acceptance criteria:**
- [ ] `building_components.yaml` validates as `BuildingComponent` and holds: at least one IFC-sourced component with a `material`, one `IfcWindow`, one `permanence: temporary`, one `source: derived` whose `derived_from` names a component in the same file, one `part_of` naming the roof in the same file and eight naming the two stair ids
- [ ] The four invalid documents fail naming `permanence`, `id`, `ifc_type`, `derived_from` respectively
- [ ] `dist/product.schema.json` `BuildingComponent` carries an `allOf` of two `if`/`then` blocks and every `Position` and `Quantity` slot as a `$ref`

**Verification:**
- [ ] Tests pass: `uv run pytest` with five new rows collected; note the wall time of the `building_components.yaml` row
- [ ] Build succeeds: `uv run python scripts/build.py` run twice; `git status --porcelain` shows only the intended files
- [ ] Manual check: `docs/model/product/BuildingComponent.md` shows a Rules table with two rows; every `contained_in` in the file names an id in `storeys.yaml` and every `located_in` one in `spaces.yaml`

**Dependencies:** Task 1

**Files likely touched:**
- `schema/product.yaml`
- `examples/product/building_components.yaml`
- `examples/product/invalid/building_component_missing_permanence.yaml`, `building_component_id_not_global_id.yaml`, `building_component_ifc_missing_ifc_type.yaml`, `building_component_derived_missing_derived_from.yaml`
- `tests/test_examples.py`
- `dist/product.schema.json`, `docs/model/product/*` (generated)

**Estimated scope:** Medium

## Task 3: `Connector`, `ConnectorKind`, and the clearance rule, end to end

**Description:** Add the `ConnectorKind` enum and the `Connector` class, `is_a: BuildingComponent`, with `kind`, `connects`, `clear_width`, `clear_height` declared as the spec's slot table states, `kind` and `connects` required in `slot_usage`, and the one rule with `any_of` over `door`, `void`. Grow the extractor: the 14 doors as `kind: door` with the component slots, `clear_width` and `clear_height` from `OverallWidth` and `OverallHeight`, `connects` from space boundaries with the exterior Space as the second end when only one Space bounds the door and the footprint-overlap fallback when three do; the 2 stairs as `kind: stair` with `connects` from the flight's lowest and highest vertex against Level 1 and Level 2 Space footprints, no clearances. Print every door or stair the rule did not decide outright and stop if any remains undecided. Copy one real door into each of the two invalid documents and break it. Add three rows. Rebuild and commit as `feat(product): add Connector`.

**Acceptance criteria:**
- [ ] `connectors.yaml` validates as `Connector` and holds 14 doors each with both clearances, 4 of them with an exterior Space in `connects`, and 2 stairs whose two Spaces sit on different storeys
- [ ] `invalid/connector_one_space.yaml` fails naming `connects`; `invalid/connector_door_missing_clear_height.yaml` fails naming `clear_height`
- [ ] `dist/product.schema.json` `Connector.properties` holds every `BuildingComponent` property plus four; `connects` has `minItems: 2` and `maxItems: 2`; `Connector` carries an `allOf` of three blocks

**Verification:**
- [ ] Tests pass: `uv run pytest` with three new rows collected, twelve product rows in all
- [ ] Build succeeds: `uv run python scripts/build.py` run twice; `git status --porcelain` shows only the intended files
- [ ] Manual check: `docs/model/product/index.md` shows `Connector` indented under `BuildingComponent`; `Connector.md` shows a Rules table with three rows; no two file names under `docs/model/product/` match case-insensitively

**Dependencies:** Task 2

**Files likely touched:**
- `schema/product.yaml`
- `examples/product/connectors.yaml`
- `examples/product/invalid/connector_one_space.yaml`, `connector_door_missing_clear_height.yaml`
- `tests/test_examples.py`
- `dist/product.schema.json`, `docs/model/product/*` (generated)

**Estimated scope:** Medium

## Checkpoint: Phase 2
- [ ] Twelve product rows pass
- [ ] Every id named in `connects`, `located_in`, `contained_in`, `derived_from`, and `part_of` exists in one of the four files; every `id` across the four files is distinct
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
