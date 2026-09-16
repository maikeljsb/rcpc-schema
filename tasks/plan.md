# Implementation Plan: product

*Module `product` of `CAPABILITY-MAP.md`, specified in `SPEC-product.md` (approved and committed 2026-09-15, `732ddaf`). Plan drafted and approved 2026-09-15. Tasks in `tasks/todo.md`. The completed `resource` plan is archived under `tasks/archive/`.*

## Overview

Write `schema/product.yaml` in three slices, each from schema to extracted examples to test rows to generated outputs, then verify and push. The order is bottom-up along the reference slots: `Storey` and `Space` first, because `contained_in`, `located_in`, and `connects` point at them; `BuildingComponent` second, the class everything else is or references; `Connector` last, the one subclass, which needs both Spaces and components to exist. Every example record is read from `examples/ifc_models/20260907_1713.ifc` by one throwaway ifcopenshell script that grows with the tasks and is gitignored with the model. The spec fixed the model; this plan fixes only how the examples are extracted and in what order the schema is written.

## The model the examples come from

`examples/ifc_models/20260907_1713.ifc`, in a gitignored folder, is an IFC2X3 export from Revit 2011 of a two-unit apartment building. Probed 2026-09-15:

| What | Count | Notes |
|---|---|---|
| `IfcBuildingStorey` | 4 | `T/FDN` at -1.25, `Level 1` at 0, `Level 2` at 3.1, `Roof` at 6.0 m; `Elevation` set on all, `LongName` on none |
| `IfcSpace` | 21 | 10 on each of Level 1 and 2, one on Roof, none on T/FDN; `Name` is the room number, `LongName` the room name; no `Pset_SpaceCommon.IsExternal` TRUE, no `IfcExternalSpatialElement` |
| `IfcDoor` | 14 | 6 on Level 1, 8 on Level 2; `OverallWidth` and `OverallHeight` set on all; 4 have one bounding Space (the exterior doors), 9 have two, 1 has three |
| `IfcStair` | 2 | Both contained in Level 1, both aggregate one `IfcStairFlight`, two `IfcMember`, two `IfcRailing`; no space boundaries |
| `IfcWindow` | 24 | plain components |
| Other built elements | 106 | 57 walls (56 `IfcWallStandardCase`, 1 `IfcWall`), 20 slabs plus 1 roof slab, 13 coverings, 8 beams, 7 footings, 1 roof aggregating its slab |
| `IfcOpeningElement` without filling | 12 | 10 cut furnishing elements, 2 cut the roof slab; none cuts a wall |
| Material | 92 | 91 `IfcMaterialLayerSetUsage`, 1 `IfcMaterial`; no base quantities on any element |
| Space boundaries | 685 | `IfcRelSpaceBoundary`, IFC2X3 first level |
| Containment | 61 elements in Spaces, 146 in storeys | coverings and furnishing sit in Spaces; walls, slabs, doors, windows in storeys |
| Length unit | METRE | every location and quantity in `m` |

## Dependency Graph

```
schema/product.yaml  (header, RecordSource, Storey, Space)                          (Task 1)
    ├── examples/product/storeys.yaml, spaces.yaml   from the extractor                 (Task 1)
    ├── examples/product/invalid/  space_missing_source, storey_id_not_global_id         (Task 1)
    ├── tests/test_examples.py  four rows                                                (Task 1)
    └── dist/product.schema.json, dist/README.md, docs/model/product/                    (Task 1)
            │
            └── + ComponentPermanence, BuildingComponent, required-everywhere, one rule  (Task 2)
                    ├── examples/product/building_components.yaml   parsed + 2 derived
                    ├── invalid/  five BuildingComponent documents, six rows
                    └── dist/, docs/  rebuilt
                            │
                            └── + ConnectorKind, Connector, its four slots and one rule   (Task 3)
                                    ├── examples/product/connectors.yaml   14 doors, 2 stairs
                                    ├── invalid/  two Connector documents, three rows
                                    └── dist/, docs/  rebuilt
                                            │
                                            └── success criteria verified, push, CI       (Task 4)
```

## Architecture Decisions

- **Reference targets before referrers.** `Storey` and `Space` carry no reference to a component, so they close first; `BuildingComponent` references both; `Connector` references Spaces and, through `part_of` on its parts, is referenced from `building_components.yaml`. Each task's example file names only ids that already exist in a committed file, except Task 2's stair parts, whose `part_of` names the two stair ids that Task 3 writes into `connectors.yaml`; Task 4's cross-file check closes that gap.
- **One extractor, grown per task, gitignored beside the model.** `examples/ifc_models/extract_product_examples.py`, in the gitignored folder beside the IFC file it reads, run from the repository root as `uv run --with ifcopenshell==0.8.5 --with shapely --with numpy python examples/ifc_models/extract_product_examples.py`. `--with` adds the three packages to the run without touching `pyproject.toml` or `uv.lock`, so success criterion 7 holds. It rewrites all four example files on every run; the files are committed, the script is not, and nothing under `scripts/` or `tests/` touches it. Probed 2026-09-15: ifcopenshell 0.8.5 and shapely 2.1.2 install this way and the geometry engine runs.
- **The extractor applies the spec's lineage rules and nothing cleverer.** `id` is the GlobalId; `ifc_type` is the entity name as the file spells it (`IfcWallStandardCase`, `IfcFooting`); `material` follows the rule in the lineage table, which on this file resolves every usage to its layer set and yields the set's name; `contained_in` from `IfcRelContainedInSpatialStructure` and, for Spaces, from `IfcRelAggregates`; `located_in` only where the file itself contains an element in an `IfcSpace`, in which case `contained_in` is that Space's storey; `elevation` from the `Elevation` attribute; clearances from `OverallWidth` and `OverallHeight`. Slots the file gives no value for stay absent: no element carries base quantities, so parsed components have no dimension slots, and nothing fills `supply_location` or `current_location`.
- **`target_location` is the centre of the body's bounding box** in world coordinates, from `ifcopenshell.geom` with `use-world-coords`. The spec says centroid; for the walls, slabs, doors, and windows here the two coincide or nearly so. The true volume centroid is the derivation slice's refinement, not this plan's.
- **Minted ids are deterministic.** A derived record's id is `ifcopenshell.guid.compress(uuid5(NAMESPACE_URL, "https://rcpc.for5672/schema/product/<what>/<source GlobalId>[/<n>]").hex)`, so the same run always writes the same id, as the spec's derivation section requires.
- **Four derived exterior Spaces, one per storey**, named `exterior <storey name>`, `source: derived`, `contained_in` the storey. No storey qualifies for the `IfcExternalSpatialElement` or `IsExternal` rule, so none takes a parsed id.
- **Two derived components, the minimum success criterion 5 asks for.** One brick, `derived_from` the first Level 1 wall whose layer set is `Exterior - Brick on Block`, placed at the wall's lowest corner offset by half a brick along each axis, carrying the brick's own `length`, `width`, `height` (0.24, 0.115, 0.071 m) as the derivation's stated parameter; `material` is the brick layer's `IfcMaterial.Name`. One formwork panel, `permanence: temporary`, `derived_from` the first `IfcFooting` on `T/FDN`, at the footing's bounding-box centre, with no `material`, so the work list has a real row. Everything else in the file is parsed.
- **`building_components.yaml` holds every built element in the model** except doors and stairs, which are Connectors, and furnishing, which is not a built element: 141 parsed components (106 walls, slabs, coverings, beams, and footings; 24 windows; the roof itself; and the stairs' ten parts — two flights, four members, four railings, each `part_of` its stair), plus the 2 derived records, 143 records. Corrected 2026-09-15 during Task 2 against the real count; the drafting estimate of "8 stair parts, about 117 records" undercounted the windows and two of the five parts per stair. One loop with no selection logic is the smallest honest extractor, and a whole model is what the projection component will meet. Parts (the roof's slab and the stairs' ten) carry `part_of` and no `contained_in`, per the spec.
- **Every parsed component is `permanence: permanent`.** The model has no temporary works and IFC has no attribute for the distinction. The one temporary record is the derived formwork.
- **`connects` comes from space boundaries, with geometry as the fallback the brief names.** A door bounded by one Space connects it to the exterior Space of the door's storey. A door bounded by two connects them. The one door bounded by three Spaces is resolved by the brief's fallback: the two Space footprints its own footprint overlaps most; Task 3 records which. A stair has no boundaries, so its lower end is the Level 1 Space whose footprint holds the flight's lowest vertex and its upper end the Level 2 Space holding its highest. `clear_width` and `clear_height` on stairs stay absent; the spec allows it and the file carries neither.
- **No `void` Connector in the examples.** No unfilled opening in this model cuts a wall; the two in the roof slab have no second Space the file can name. `ConnectorKind.void` is declared and documented; its example waits for a model that has one.
- **Invalid documents are one real record each with one edit**, copied from the committed valid file and broken on the slot the row names, so no invalid document carries invented values either.
- **Example files are written by `yaml.safe_dump` with `sort_keys=False`** in the slot order of the spec's class tables, `Position` and `Quantity` in flow style as the spec's examples show. GlobalIds containing `$` or starting with a digit are plain YAML strings; the dumper quotes anything YAML would otherwise misread.

## Task List

### Phase 1: The topology
- [x] Task 1: `Storey`, `Space`, and `RecordSource`, end to end

### Checkpoint: Phase 1
- [x] `uv run pytest` passes with four product rows collected
- [x] `dist/product.schema.json` has the GlobalId pattern on `id` in both classes and common's `$defs` beside them; `dist/README.md` lists product
- [x] Review with human

### Phase 2: Components and passages
- [x] Task 2: `BuildingComponent`, `ComponentPermanence`, and its one class rule, end to end
- [ ] Task 3: `Connector`, `ConnectorKind`, and the clearance rule, end to end

### Checkpoint: Phase 2
- [ ] Thirteen product rows pass; `BuildingComponent` carries a bare `if`/`then` pair (one rule) and `Connector` an `allOf` of two
- [ ] Every id named in `connects`, `located_in`, `contained_in`, `derived_from`, and `part_of` exists in one of the four files
- [ ] Review with human

### Phase 3: Close
- [ ] Task 4: Verify the seven success criteria, push, confirm CI

### Checkpoint: Complete
- [ ] Every success criterion in `SPEC-product.md` verified with evidence
- [ ] `schema/common.yaml`, `scripts/`, and the toolchain tests untouched by this module
- [ ] Ready for `SPEC-process.md`

## Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| The door bounded by three Spaces overlaps two footprints equally, or the stair's end vertex falls in no Space | Medium: `connects` would be a guess | Task 3 prints the candidates and their overlap; if the rule does not decide, the task stops and asks rather than picking |
| A generated doc page name collides case-insensitively with another (`Connector`/`connects`, `Storey`/`storeys`) | Low: names differ by more than case | Task 1 and Task 3 list `docs/model/product/` and check no two names match case-insensitively before committing |
| `linkml-validate` on a 117-record file makes `test_examples.py` slow | Low | Measure in Task 2; if a row exceeds a few seconds, report it, do not trim the file unasked |
| The bounding-box centre misplaces an L-shaped or sloped element | Low: examples only; the derivation slice owns the true centroid | Recorded here and in the `target_location` row of Task 4's evidence |
| The Level 1 `Exterior - Brick on Block` layer set has no layer whose material is a brick by name | Low | Use the outermost layer's material name whatever it is; the brick's `material` is what the file says |
| `uv run --with` resolves a different ifcopenshell on another day | Low: the script is throwaway; committed YAML is the artifact | Pin `--with ifcopenshell==0.8.5` in the run command written in the task |

## Parallelisation

None. Four sequential tasks on one schema file and one extractor.

## Open Questions

None. The ten decisions of the drafting report were accepted on 2026-09-15; the extractor's location moved from a sibling folder into `examples/ifc_models/`, gitignored with the model. During Task 2, `BuildingComponent`'s shape was redesigned to required-everywhere with an empty-string convention, retiring the `ifc_type` rule and narrowing the `derived_from` rule to a pattern check; recorded as `SPEC-product.md` decisions 2 and 15, not repeated here.
