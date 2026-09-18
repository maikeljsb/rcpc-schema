# Spec: product

*Module `product` of `CAPABILITY-MAP.md`. Drafted, reviewed, and approved 2026-09-15 (`732ddaf`); the required-everywhere redesign in decision 2 and decision 15 followed during Task 2's implementation. Depends on `common`. Imported by `process`. Direction fixed by the brief's Product Side and its dated decisions; IFC lineage from `docs/research/ifc43-for-product.md`; derivation limits from `docs/research/topologicpy-for-product.md`; metamodel usage follows `docs/research/linkml-metamodel-conformance-and-inheritance.md`.*

## Objective

Give the process side something to build: a building component identified by an IFC GlobalId, parsed or minted, with the material string a method matches on, the point a placement task binds to, and the light spatial topology that says where it is and what a robot passes through to reach it. Deliver it as `schema/product.yaml`, with example documents taken from a real model, generated JSON Schema, and generated documentation.

**Users.** The IFC parser and the derivation, later, which fill BuildingComponents, Spaces, Storeys, and Connectors from a model. The person resolving a parsed model, who adds derived components such as bricks and fills missing materials. The process module, whose methods match `material` and whose primitives reference components by id. The projection component, which turns `derived_from`, `part_of`, `located_in`, `contained_in`, and `connects` into edges. Other project teams, who read `docs/model/product/`.

**Success in one sentence.** `schema/product.yaml` lints clean, the four example documents from the real model validate and the ten invalid documents fail naming their slot, the toolchain produces its JSON Schema and docs unchanged, and every row of the lineage table below names the IFC construct it borrows or adapts.

**What this module deliberately is not.** It carries no geometry, no IFC element hierarchy, no property sets, no material taxonomy, no Building or Site class, and no runtime state beyond `current_location`. It does not derive its own instances: the parser and the topology derivation are later slices, and this spec records only what they must deliver.

## Tech Stack

Inherited from `SPEC-toolchain.md` unchanged. This module adds no dependency.

## Commands

```
uv run linkml-lint schema/product.yaml
uv run linkml-validate -s schema/product.yaml -C BuildingComponent examples/product/building_components.yaml
uv run linkml-validate -s schema/product.yaml -C Connector examples/product/connectors.yaml
uv run linkml-validate -s schema/product.yaml -C Space examples/product/spaces.yaml
uv run linkml-validate -s schema/product.yaml -C Storey examples/product/storeys.yaml
uv run python scripts/build.py          # produces dist/product.schema.json, dist/README.md, docs/model/product/
uv run pytest
```

## Project Structure

Files this module adds.

```
schema/
  product.yaml                                          the module
examples/
  product/
    building_components.yaml                            components from the real model, plus derived ones
    connectors.yaml                                     doors, voids, and a stair from the same model
    spaces.yaml                                         its spaces, including one exterior Space per storey
    storeys.yaml                                        its storeys
    invalid/
      building_component_missing_permanence.yaml        no permanence
      building_component_id_not_global_id.yaml          id is a readable slug, not a GlobalId
      building_component_ifc_missing_ifc_type.yaml      no ifc_type key at all
      building_component_derived_missing_derived_from.yaml   source derived, no derived_from key at all
      building_component_derived_from_empty.yaml        source derived, derived_from is "" not a real id
      connector_one_space.yaml                          connects lists one Space
      connector_door_missing_clear_height.yaml          kind door, no clear_height
      space_missing_source.yaml                         a Space without source
      space_record_type_mismatch.yaml                   a Space document whose record_type says Storey
      storey_id_not_global_id.yaml                      a Storey whose id is not a GlobalId
dist/
  product.schema.json                                   generated
  README.md                                             regenerated, now lists product
docs/
  model/
    product/                                            generated, one page per element
tests/
  test_examples.py                                      fourteen rows added to EXAMPLES, nothing else
```

The example documents are supplied by the author from a real model, not invented. This spec names the files and says what each must contain; the author fills them.

## Prerequisite change to common

None. `MaterialName`, `Position` with its unit, and the four dimension slots already exist in common.

## The Model

### Schema header

```yaml
id: https://rcpc.for5672/schema/product
name: product
version: 0.1.0
description: >-
  Building components as planning targets. BuildingComponent identified by its IFC
  GlobalId, with lifetime and provenance; Connector for what a robot passes through;
  Space and Storey as the topology they sit in.
prefixes:
  rcpc: https://rcpc.for5672/schema/
  linkml: https://w3id.org/linkml/
default_prefix: rcpc
default_range: string
imports:
  - linkml:types
  - common
```

### Identity

Every record's `id` is an IFC GlobalId, the 22-character compressed form, and the pattern `^[0-3][0-9A-Za-z_$]{21}$` is set on `id` in every class through `slot_usage`. For a parsed record it is the GlobalId of the IFC entity. For a derived record the derivation mints one in the same format. There is no separate `ifc_global_id` slot; `name` carries the readable label, and every reference slot holds an id.

### Classes

| Class | Slots | Notes |
|---|---|---|
| `BuildingComponent` | `record_type`, `id`, `ifc_type`, `name`, `material`, `permanence`, `source`, `derived_from`, `part_of`, `target_location`, `supply_location`, `current_location`, `located_in`, `contained_in`, `length`, `width`, `height`, `weight` | One thing a task acts on. Every slot is `required: true`: the document shape is the same for every component. `ifc_type`, `material`, `derived_from`, `part_of`, `located_in`, `contained_in` hold `""` where they do not apply or are not yet resolved; `supply_location`, `current_location`, `length`, `width`, `height`, `weight` hold the unresolved sentinel, a real Position or Quantity object with `unit: ""`. One class rule: when `source` is `derived`, `derived_from` must additionally match the GlobalId pattern, not just be present. |
| `Connector` | the BuildingComponent slots plus `kind`, `connects`, `clear_width`, `clear_height` | `is_a BuildingComponent`, the model's one subclass. A door, an unfilled opening, or a stair as one node: the component a task installs and the passage a robot fits through. Every slot is `required: true`: `kind`, `connects` with exactly two Spaces, and `clear_width`, `clear_height`, which hold the unresolved sentinel on a stair until a later slice reads them from geometry. No rule of its own; it inherits `BuildingComponent`'s one, so its schema carries a bare `if`/`then` pair. |
| `Space` | `record_type`, `id`, `name`, `long_name`, `source`, `contained_in` | A room, or the exterior region of one storey. Parsed from `IfcSpace`, or derived: rooms cut from wall footprints when the file has no spaces, and one exterior Space per storey so that an exterior door and a roof stair have two ends. Every slot but `elevation`-typed ones (none here) is `required: true`: `name` and `long_name` hold `""` when the IFC file has none; `contained_in` always holds a real Storey id, never `""`, because a Space always has one by construction. |
| `Storey` | `record_type`, `id`, `name`, `long_name`, `elevation` | A building storey. Always parsed. Every slot is `required: true`; `name`/`long_name` hold `""` when the IFC file has none, `elevation` the unresolved sentinel `{value: 0.0, unit: ""}` (see decision 2). |

All four classes carry an identifier and project to nodes. `derived_from`, `part_of`, `located_in`, `contained_in`, and `connects` are reference slots and project to edges. `Position` and `Quantity` have no identifier and flatten into the node that holds them.

Every class also carries `record_type`, a LinkML type designator (`designates_type: true`) that names the class itself: `"Storey"`, `"Space"`, `"BuildingComponent"`, `"Connector"`. Declared once as a plain string slot and reused by all four the way `id` is; `Connector` inherits it from `BuildingComponent` without redeclaring it, and its own generated schema independently locks it to `"Connector"`, not `"BuildingComponent"` (LinkML resolves the designated value from the class actually being generated, not the class that declares the slot). A record therefore always says what it is, on its own terms, independent of which file holds it; a document validated against the wrong class fails on `record_type` even where the two classes' other slots would otherwise overlap.

### Enums

| Enum | Values | Notes |
|---|---|---|
| `ComponentPermanence` | `permanent`, `temporary` | Whether the component stays in the building. Reinforcement is permanent, formwork temporary. No default. |
| `RecordSource` | `ifc`, `derived` | Where a component or Space came from: parsed from the IFC model, or produced by the derivation. No default. |
| `ConnectorKind` | `door`, `void`, `stair` | What kind of passage a Connector is. `void` is an `IfcOpeningElement` with no filling. Windows are not passages and are plain BuildingComponents. |

Enums are named after what they qualify, following `RobotStatus`, because an enum named `Permanence` beside a slot `permanence` would write the same generated doc page on a case-insensitive filesystem. Probed 2026-09-15: `ComponentPermanence.md` and `permanence.md` coexist.

### Slots declared in this module

| Slot | Range | Notes |
|---|---|---|
| `record_type` | string, `designates_type: true` | Which class the record is: `Storey`, `Space`, `BuildingComponent`, or `Connector`. Required on all four; the value is fixed by the class, not authored. |
| `ifc_type` | string | The bare IFC entity name, such as `IfcWall`. No PredefinedType, no ObjectType. Required on every BuildingComponent; `""` on a derived record, which has none. |
| `name` | string | The IFC Name. Required on every class that carries it; `""` when the IFC file has none. |
| `long_name` | string | The IFC LongName of a Space or Storey. Required on both; `""` when the IFC file has none. |
| `material` | `MaterialName` | The one material string the parser derives, exactly as the IFC spells it. Required on every BuildingComponent; `""` when unresolved, still a tier 3 work item. |
| `permanence` | `ComponentPermanence` | Required, no default. |
| `source` | `RecordSource` | Required on BuildingComponent and Space, no default. |
| `derived_from` | `BuildingComponent`, not inlined | The IFC-sourced component this one was generated from. Required on every BuildingComponent; `""` except when `source` is `derived`, when a rule requires it to match the GlobalId pattern, not `""`. |
| `part_of` | `BuildingComponent`, not inlined | The assembly this component is a part of, IFC's aggregation from the part's side. A stair flight is `part_of` its stair. Required on every BuildingComponent, `""` when it is not part of one; single-valued because an IFC element decomposes at most one whole. |
| `target_location` | `Position`, `inlined: true` | The centroid of the component's body in the IFC project frame, in the project length unit. Where the design puts it and what a placement task binds to. Required. |
| `supply_location` | `Position`, `inlined: true` | Where the component is delivered or staged. Required; the unresolved sentinel `{x_coord: 0.0, y_coord: 0.0, z_coord: 0.0, unit: ""}` when not yet known. |
| `current_location` | `Position`, `inlined: true` | Where the component is now. Written by execution; the model's second runtime slot after `status`. Required; the same unresolved sentinel until execution writes a real one. |
| `located_in` | `Space`, not inlined | The Space the component's point lies in. Required on every BuildingComponent; `""` for walls and slabs, or wherever the point is not known to lie in a Space. |
| `contained_in` | `Storey`, not inlined | IFC's containment relation under its own name. On a BuildingComponent, its storey; on a Space, the storey that aggregates it or, for a derived Space, the storey it was cut for. Required on both: `""` on a BuildingComponent part, but always a real Storey id on Space, which by construction always has one. |
| `kind` | `ConnectorKind` | Required on Connector. |
| `connects` | `Space`, multivalued, not inlined, `minimum_cardinality: 2`, `maximum_cardinality: 2` | The two Spaces a Connector joins. Required on Connector. A stair's two Spaces are on different storeys. |
| `clear_width` | `Quantity`, `inlined: true` | The passable width. For a door the IFC OverallWidth, with the opening's geometry as fallback; for a void the opening's geometry; for a stair the flight width, read from geometry. |
| `clear_height` | `Quantity`, `inlined: true` | The passable height. For a door the IFC OverallHeight, with the opening's geometry as fallback; for a void the opening's geometry; for a stair the headroom, read from geometry. |
| `elevation` | `Quantity`, `inlined: true` | The storey's level in the project frame. Required; the unresolved sentinel `{value: 0.0, unit: ""}` when not known. |

Reused from common: `id`, `length`, `width`, `height`, `weight` as slots; `Position`, `Quantity`, `MaterialName` as ranges. Every Position and Quantity slot states `inlined: true` so the document shape is visible in the YAML; a reference slot states `range` alone, no `inlined`, so a reader sees which slots are references. On `BuildingComponent`, `derived_from`, `part_of`, `located_in`, and `contained_in` additionally carry `pattern: "^$|^[0-3][0-9A-Za-z_$]{21}$"` in `slot_usage`, so their value is always a real GlobalId or the empty string, never other text.

### Class rules

One rule, tier 1: `linkml-validate` enforces it and `gen-json-schema` renders it. Probed 2026-09-15 on LinkML 1.11.1: a class with exactly one rule gets a bare `if`/`then` pair on the class itself; a class with more than one gets an `allOf` of `if`/`then` blocks. `Connector` inherits `BuildingComponent`'s rule and adds none, so both classes carry a bare pair.

`ifc_type` needs no rule: it is `required: true` unconditionally, because the parser always has an IFC-sourced component's entity name on hand, so it is never legitimately empty on that branch. `clear_width` and `clear_height` need none for the same reason: a door's are read straight off `OverallWidth` and `OverallHeight`, and as required keys they are present on every Connector, the unresolved sentinel on a stair; a rule cannot look inside a Quantity to demand a real `unit`, so whether a door's clearance is real is a tier 3 check. `derived_from` keeps its rule because it is the derivation's own logic, not a fact IFC hands over, so its correctness is worth a genuine tier 1 check.

| Class | If | Then |
|---|---|---|
| `BuildingComponent`, inherited by `Connector` | `source` equals `derived` | `derived_from` matches the GlobalId pattern, not the empty string |

### What the derivation must deliver

Instances of this module are derived, not authored, and the derivation is a later slice with its own plan. This contract fixes what that slice owes the schema, so the constraints above are promises the derivation keeps rather than errors buildings produce.

- Every record gets an `id` in GlobalId form: the entity's own when parsed, minted when derived, the same on every run.
- Every model gets Spaces. When the file carries `IfcSpace`, they are parsed. When it does not, rooms are cut from wall footprints per storey and marked `source: derived`. Structural and fabrication models without spaces are in scope.
- Every storey gets one exterior Space, `source: derived`, `contained_in` that storey, so that a ground-floor door, a balcony door, and a roof stair each have two ends that are not the same node. When the file carries `IfcExternalSpatialElement`, the ground storey's exterior takes its GlobalId and `source: ifc`.
- Every Connector gets exactly two Spaces. A Connector with one end is a derivation bug, and tier 1 catches it.
- Windows are parsed as BuildingComponents and never as Connectors.
- Every derived Space is a line on the human work list, confirmed as a real exterior or room, or a sign the model is missing one.
- Every `BuildingComponent` key is written on every record, resolved or not: `ifc_type`, `material`, `derived_from`, `part_of`, `located_in`, and `contained_in` hold `""` rather than being left out when they do not apply or have not been resolved yet. Whether an empty one is expected (`part_of` on almost everything) or a gap worth a human's attention (`material`, `contained_in`, `located_in` on a model good enough to have them) is a tier 3 question, not a shape question.

Known ceiling, accepted for the first slice: two disconnected exterior regions on one storey, a north balcony and a south balcony, share one exterior Space and so admit a false path between them. Splitting by connected region needs geometry the first derivation will not have.

### Lineage: IFC construct to slot

Every row is a decision. "Borrowed" means the IFC value is carried as is, "Adapted" means it is transformed or narrowed. Constructs the module carries nothing for are not listed; the research note's table, `docs/research/ifc43-for-product.md` section Proposed lineage table, records them with their source pages, and this table supersedes it for what is carried.

**Identity and naming**

| IFC construct | Slot or class | Borrowed / Adapted | Note |
|---|---|---|---|
| IfcRoot.GlobalId (IfcGloballyUniqueId) | `id` on all four classes | Adapted | The GlobalId is the record's identifier, pattern `^[0-3][0-9A-Za-z_$]{21}$`. Derived records carry a minted id in the same format. |
| Entity name of the IfcBuiltElement subtype | `ifc_type` | Borrowed | The EXPRESS entity name, stable and type-independent. |
| IfcRoot.Name | `name` on all four classes | Borrowed | OPTIONAL IfcLabel, so optional. |
| IfcSpatialElement.LongName | `long_name` on Space and Storey | Borrowed | Name is the room number, LongName the descriptive name. Both optional. |

**Material and position**

| IFC construct | Slot or class | Borrowed / Adapted | Note |
|---|---|---|---|
| IfcRelAssociatesMaterial.RelatingMaterial (IfcMaterialSelect) | `material` | Adapted | One string: occurrence over type, unwrap a usage to its set, IfcMaterial.Name, else the set's name, else member names joined with " / ". Loses layering, profiles, constituents. Rule in the research note, 3.3. |
| IfcProduct.ObjectPlacement resolved through PlacementRelTo to the WorldCoordinateSystem | `target_location` | Adapted | The centroid of the body in the project frame, not the placement origin, which is a corner or axis start. |
| IfcGeometricRepresentationContext.WorldCoordinateSystem, TrueNorth; IfcContext.UnitsInContext | the frame and unit of every location slot | Adapted | Stated once in the slot descriptions; the unit travels on `Position`. TrueNorth and IfcMapConversion are dropped. |

**Spatial structure**

| IFC construct | Slot or class | Borrowed / Adapted | Note |
|---|---|---|---|
| IfcRelContainedInSpatialStructure with an IfcSpace as RelatingStructure | `located_in` | Adapted | Cardinality 0..1 matches. Usually empty in files, so the value is derived from the component's point. |
| IfcRelContainedInSpatialStructure with an IfcBuildingStorey as RelatingStructure, or the containing space's aggregation parent | `contained_in` on BuildingComponent | Borrowed | 0..1. The IFC relation under its own name. |
| IfcRelAggregates, storey aggregates space | `contained_in` on Space | Adapted | IFC files this under aggregation; the module reuses one slot name for both. A derived Space is contained in the storey it was cut for. |
| IfcRelAggregates for element assemblies (IfcStair, IfcCurtainWall, IfcRoof and their parts) | `part_of` | Adapted | Both the assembly and its parts become BuildingComponents, each with its own GlobalId; the part carries `part_of` naming the assembly, the direction of IFC's `Decomposes`, 0..1. Parts have no containment of their own, so a part's `contained_in` is the assembly's, reached through the decomposition chain. The reverse, "the parts of this assembly", is a query. |
| IfcRelSpaceBoundary, 1stLevel, 2ndLevel | input to `connects` and `located_in` | Adapted | Not carried as a relation. One of two inputs to the derivation that fills `connects`; the other is door footprints overlapping room footprints per storey when the file has no boundaries. |
| IfcSpace | `Space` with `source: ifc` | Adapted | GlobalId, Name, LongName, storey. No geometry, CompositionType, PredefinedType, or ElevationWithFlooring. When a file has no IfcSpace, rooms are derived from wall footprints and carry `source: derived`. |
| IfcExternalSpatialElement | the ground storey's exterior `Space` | Adapted | The correct IFC entity for the exterior when present, taken as that Space's id with `source: ifc`; an IfcSpace with Pset_SpaceCommon.IsExternal TRUE is accepted in its place. Otherwise, and for every other storey, the exterior Space is derived with a minted id. |
| IfcBuildingStorey | `Storey` | Adapted | GlobalId, Name, LongName, elevation. |
| IfcBuildingStorey.Elevation | `elevation` | Adapted | Optional Quantity. Precedence: the deprecated Elevation attribute when present, else the storey placement's z in the project frame. Pset_BuildingStoreyCommon's relative elevations are dropped. |

**Openings, doors, windows, stairs**

| IFC construct | Slot or class | Borrowed / Adapted | Note |
|---|---|---|---|
| IfcOpeningElement with PredefinedType OPENING and no filling | `Connector` of kind `void` | Adapted | The one exception to the rule that only IfcBuiltElement subtypes become components: a hole in a wall is a passage. `ifc_type` is `IfcOpeningElement`. RECESS does not become a Connector. |
| IfcDoor as filling element (IfcRelFillsElement) | `Connector` of kind `door` | Adapted | One node carries the component slots and `connects`; there is no second record for the opening. |
| IfcWindow | `BuildingComponent` | Adapted | A component a task installs, not a passage. No `connects`, no clearances. Reinstated as a Connector kind only when a task passes something through a window. |
| IfcDoor.OverallWidth, OverallHeight | `clear_width`, `clear_height` | Adapted | Defined as the opening size excluding the lining, the closest IFC value to a clearance. Fallback is the filled opening's geometry. |
| IfcStair, IfcStairFlight | `Connector` of kind `stair`; flights as BuildingComponents with `part_of` | Adapted | The IfcStair connects two Spaces on different storeys as a door connects two on one; its upper end at a roof lands in that storey's exterior Space. `clear_width` is the flight width and `clear_height` the headroom, both from geometry, both optional. Its flights and landings are plain BuildingComponents, each `part_of` the stair. |

**Quantities and properties**

| IFC construct | Slot or class | Borrowed / Adapted | Note |
|---|---|---|---|
| Qto_WallBaseQuantities Length, Width, Height, NetWeight | `length`, `width`, `height`, `weight` | Borrowed | Direct for walls. |
| Qto_SlabBaseQuantities Length, Depth, Width, NetWeight | `length`, `width`, `height`, `weight` | Adapted | Slab Width is the thickness and maps to `height`; Depth maps to `width`. |
| Qto_BeamBaseQuantities, Qto_ColumnBaseQuantities Length, NetWeight; IfcRectangleProfileDef XDim, YDim | `length`, `weight`; `width`, `height` | Adapted | No width or height quantity exists; taken from the profile when the body is a swept rectangle, else absent. |
| IfcRelDefinesByProperties to IfcElementQuantity | the parser's path to the four dimension slots | Adapted | Name is the template name, MethodOfMeasurement is BaseQuantities; may sit on the type, occurrence overrides. Not a slot. |
| IfcProduct's "permanent use or temporary use", prose only | `permanence` | Adapted | IFC names the distinction in prose and has no attribute; the enum is the module's own. |

### Required

| Slot | Why |
|---|---|
| `record_type` on every class | A record must say what it is on its own terms; a document validated against the wrong class then fails on `record_type` specifically, rather than depending on the classes' other slots happening to differ enough to catch the mistake. |
| `id` on every class, matching the GlobalId pattern | It projects to a node, a node needs an identifier, and the identifier must survive a re-parse of the model. |
| `BuildingComponent.permanence`, `source` | An unknown lifetime or provenance is a hole in the plan; a default would mislabel temporary works. |
| `BuildingComponent.target_location` | A placement task has nothing to bind to without it. |
| `BuildingComponent.ifc_type`, `material`, `derived_from`, `part_of`, `located_in`, `contained_in` as keys, on every record | The document shape must not depend on what the pipeline happened to resolve; a downstream check reads a value, never has to test for a missing key, and `""` on a reference slot renders as no edge at projection time, exactly what absence used to mean. |
| `derived_from` matching the GlobalId pattern, not `""`, when `source` is `derived` | Presence alone does not say a derived record actually names what it came from; unlike `ifc_type`, which the parser always has, this is the derivation's own logic, which can fail or forget. |
| `Space.source` | A derived room or exterior must say so, because it is a claim the derivation made, not a fact the model carried. |
| `name`, `long_name` as keys, on every class that carries them | The same required-everywhere reasoning applies to any plain string slot, not only `BuildingComponent`'s; `""` when the IFC file has none. |
| `Space.contained_in`, holding a real Storey id, never `""` | Every Space has a storey by construction (the derivation's own contract, see What the derivation must deliver); unlike `BuildingComponent`'s use of the same slot, there is no legitimate empty case to allow. |
| `BuildingComponent.supply_location`, `current_location`, `length`, `width`, `height`, `weight`, and `Storey.elevation` as keys, on every record | The same reasoning as the string and reference slots; a Position or Quantity's own `value`/`x_coord`/etc. stay real floats (`0.0` by convention) but its `unit` is `""` when unresolved, which no genuinely resolved Position or Quantity would ever have, so it is as safe a marker as the empty string is for a plain slot. Needs neither `null` nor a change to common's `Position`/`Quantity` (see decision 2). |
| `Connector.kind`, `connects` with exactly two Spaces | A passage with one end is not a passage; the kind says how to read the clearances. |
| `clear_width`, `clear_height` as keys, on every Connector | The fit-through check has nothing to compare otherwise. A door's come straight off the IFC door attributes; a stair's stay the unresolved sentinel until a later slice reads them from geometry, and whether a door's is real is a tier 3 check. |
| Every `Position`'s three coordinates and unit, every `Quantity`'s value and unit | Enforced by common; unaffected by the empty-unit convention above, which uses only values already legal under these constraints. |

Every slot in the module is now a required key. What varies is only what an unresolved or inapplicable value looks like: `""` for a plain string or reference, a Position or Quantity with `unit: ""` for the seven slots typed that way.

### One storey of a building, as documents

`storeys.yaml`:

```yaml
- record_type: Storey
  id: 3ZYW59sxj8lei475l7EhLU
  name: "00"
  long_name: Ground floor
  elevation: {value: 0.0, unit: m}
```

`spaces.yaml`:

```yaml
- record_type: Space
  id: 0jf0rYHfX3RAB3bSIRjmmy
  name: exterior 00
  long_name: ""
  source: derived
  contained_in: 3ZYW59sxj8lei475l7EhLU
- record_type: Space
  id: 1hOSvn6df7F8_7GcBWlRGQ
  name: "001"
  long_name: Entrance hall
  source: ifc
  contained_in: 3ZYW59sxj8lei475l7EhLU
```

`building_components.yaml`:

```yaml
- record_type: BuildingComponent
  id: 3bXiCStxP6Fgxdej$yc50n
  ifc_type: IfcWall
  name: Basic Wall:Exterior - Brick on Block:138157
  material: Brick
  permanence: permanent
  source: ifc
  derived_from: ""
  part_of: ""
  target_location: {x_coord: 4.25, y_coord: 0.15, z_coord: 1.40, unit: m}
  supply_location: {x_coord: 0.0, y_coord: 0.0, z_coord: 0.0, unit: ""}
  current_location: {x_coord: 0.0, y_coord: 0.0, z_coord: 0.0, unit: ""}
  located_in: ""
  contained_in: 3ZYW59sxj8lei475l7EhLU
  length: {value: 8.5, unit: m}
  width: {value: 0.3, unit: m}
  height: {value: 2.8, unit: m}
  weight: {value: 0.0, unit: ""}
- record_type: BuildingComponent
  id: 2O2Fr$t4X7Zf8NOew3FLTF
  ifc_type: ""
  name: brick 0001 of Basic Wall:Exterior - Brick on Block:138157
  material: Brick
  permanence: permanent
  source: derived
  derived_from: 3bXiCStxP6Fgxdej$yc50n
  part_of: ""
  target_location: {x_coord: 0.12, y_coord: 0.15, z_coord: 0.04, unit: m}
  supply_location: {x_coord: 0.0, y_coord: 0.0, z_coord: 0.0, unit: ""}
  current_location: {x_coord: 0.0, y_coord: 0.0, z_coord: 0.0, unit: ""}
  located_in: 1hOSvn6df7F8_7GcBWlRGQ
  contained_in: 3ZYW59sxj8lei475l7EhLU
  length: {value: 0.0, unit: ""}
  width: {value: 0.0, unit: ""}
  height: {value: 0.0, unit: ""}
  weight: {value: 0.0, unit: ""}
```

`connectors.yaml`:

```yaml
- record_type: Connector
  id: 3KMJUyUe9DfQ2FOCd5ZoiN
  ifc_type: IfcDoor
  name: Entrance door
  material: ""
  permanence: permanent
  source: ifc
  derived_from: ""
  part_of: ""
  target_location: {x_coord: 2.1, y_coord: 0.15, z_coord: 1.05, unit: m}
  supply_location: {x_coord: 0.0, y_coord: 0.0, z_coord: 0.0, unit: ""}
  current_location: {x_coord: 0.0, y_coord: 0.0, z_coord: 0.0, unit: ""}
  located_in: ""
  contained_in: 3ZYW59sxj8lei475l7EhLU
  length: {value: 0.0, unit: ""}
  width: {value: 0.0, unit: ""}
  height: {value: 0.0, unit: ""}
  weight: {value: 0.0, unit: ""}
  kind: door
  connects: [0jf0rYHfX3RAB3bSIRjmmy, 1hOSvn6df7F8_7GcBWlRGQ]
  clear_width: {value: 0.9, unit: m}
  clear_height: {value: 2.1, unit: m}
```

The values above show the shape. The committed files hold the real model's values.

### Fixed by the brief

Four classes, one `is_a`. `BuildingComponent` subclassed by kind only, never by source or permanence. `permanence` and `source` required with no default. `id` is the GlobalId, parsed or minted. `derived_from` is a required key on every record, `""` unless `source` is `derived`, when a rule requires it to hold a real id; the producing algorithm not recorded. `material` a required key, `""` when unresolved, still a tier 3 query. `target_location` required and a centroid; `supply_location` and `current_location` also required keys, the unresolved sentinel (a real Position with `unit: ""`) until known. The exterior is a Space per storey; `connects` exactly two. `Storey` a class identified by its GlobalId. `name` and `long_name` are required keys everywhere they appear, `""` when the IFC file has none. `contained_in` ranges Storey and is reused for Space; `located_in` is the component-to-Space relation. Connectors are doors, voids, and stairs; a stair's clearances are optional. Instances are derived, not authored; the derivation is a later slice.

## Code Style

The module follows `SPEC-toolchain.md` and `SPEC-common.md`. The component class with its identifier pattern, its required-everywhere slots, and its one rule, as it will appear:

```yaml
classes:
  BuildingComponent:
    description: >-
      One thing a task acts on. Parsed from the IFC model or derived from a
      parsed component; permanent or temporary.
    slots:
      - record_type
      - id
      - ifc_type
      - name
      - material
      - permanence
      - source
      - derived_from
      - part_of
      - target_location
      - supply_location
      - current_location
      - located_in
      - contained_in
      - length
      - width
      - height
      - weight
    slot_usage:
      id:
        pattern: "^[0-3][0-9A-Za-z_$]{21}$"
        description: >-
          The IFC GlobalId in its 22-character form: the entity's own when parsed,
          minted in the same format when derived.
      permanence:
        required: true
      source:
        required: true
      target_location:
        required: true
      ifc_type:
        required: true
      material:
        required: true
      part_of:
        required: true
        pattern: "^$|^[0-3][0-9A-Za-z_$]{21}$"
      located_in:
        required: true
        pattern: "^$|^[0-3][0-9A-Za-z_$]{21}$"
      contained_in:
        required: true
        pattern: "^$|^[0-3][0-9A-Za-z_$]{21}$"
      derived_from:
        required: true
        pattern: "^$|^[0-3][0-9A-Za-z_$]{21}$"
    rules:
      - description: A derived component names the component it came from, with a real id, not an empty one.
        preconditions:
          slot_conditions:
            source:
              equals_string: derived
        postconditions:
          slot_conditions:
            derived_from:
              required: true
              pattern: "^[0-3][0-9A-Za-z_$]{21}$"
```

Conventions specific to this module:

- **Names follow the linter's `standard_naming` rule**: CamelCase classes and enums, snake_case slots and permissible values.
- **IFC names stay recognisable.** `ifc_type`, `name`, `long_name`, `contained_in`, and `elevation` are IFC's words in snake_case. The module's own words are `located_in`, `connects`, `kind`, `derived_from`, `part_of`, `permanence`, `source`, `record_type`, and the three location slots.
- **Attribution only where the meaning changed.** Adapted slots say in one sentence what the parser does to the IFC value; borrowed slots say what the IFC attribute is; the module's own slots do not mention IFC.
- **Enums are named after what they qualify**: `ComponentPermanence`, `RecordSource`, `ConnectorKind`, so no enum page collides with its slot page.
- **Every rule has a `description`**, one sentence in the indicative, so the generated Rules table reads as prose.
- **`inlined: true` on every Position and Quantity slot**, nothing on reference slots.
- **Ids are GlobalIds, names are for people.** A derived record's `name` says what it is and what it came from, as in the brick above, because its id says nothing a reader can use.
- **Every slot in the module is a required key, with no exceptions.** An unresolved or inapplicable value is never an absent key: `""` for a plain string or reference slot, and for the seven Position/Quantity-typed slots (`target_location` excepted, always real), a real Position or Quantity object whose `unit` is `""` — `value`/`x_coord`/etc. stay ordinary floats (`0.0` by convention), since only `unit` needs to carry the marker and a resolved Position or Quantity never legitimately has an empty one. This is the module's own convention, not IFC's: it keeps the document shape identical across every record of a class regardless of what the pipeline has resolved, and gives the tiered checks a value to read instead of a key to test for, at any depth. `derived_from` and `part_of` on `BuildingComponent`, `located_in`, and `contained_in` on `BuildingComponent` also carry `pattern: "^$|^[0-3][0-9A-Za-z_$]{21}$"`, so their value is always the empty string or a real GlobalId, never other text; `contained_in` on `Space` keeps the plain, unwidened GlobalId pattern instead, because a Space always has one.
- **Every record names its own class, in the data.** `record_type` is declared once, `designates_type: true`, and reused by all four classes exactly as `id` is; each class's own generated schema locks it to that class's own name, computed by LinkML, not hand-maintained per class. A record is therefore self-describing independent of which file holds it, and a document checked against the wrong class fails on `record_type` specifically, not by chance of the classes' other slots differing.

## Testing Strategy

No new test files. Fourteen rows in `EXAMPLES`.

| Document | Class | Expected | Proves |
|---|---|---|---|
| `examples/product/building_components.yaml` | `BuildingComponent` | validates | IFC-sourced and derived components, a temporary one, a window, a part with `part_of`, the dimension slots, `located_in` and `contained_in`, and the required-everywhere convention on every record, ifc-sourced or derived |
| `examples/product/connectors.yaml` | `Connector` | validates | A door with clearances, a stair without, an exterior door whose second Space is an exterior; inherited slots plus the four of its own |
| `examples/product/spaces.yaml` | `Space` | validates | Parsed rooms, one derived exterior per storey, `source` on each |
| `examples/product/storeys.yaml` | `Storey` | validates | Every storey the other files reference |
| `invalid/building_component_missing_permanence.yaml` | `BuildingComponent` | fails on `permanence` | A plain required enum slot |
| `invalid/building_component_id_not_global_id.yaml` | `BuildingComponent` | fails on `id` | The GlobalId pattern reaches the validator |
| `invalid/building_component_ifc_missing_ifc_type.yaml` | `BuildingComponent` | fails on `ifc_type` | `ifc_type` is a required key on every record, not only ifc-sourced ones |
| `invalid/building_component_derived_missing_derived_from.yaml` | `BuildingComponent` | fails on `derived_from` | `derived_from` is a required key on every record |
| `invalid/building_component_derived_from_empty.yaml` | `BuildingComponent` | fails on `derived_from` | The one remaining class rule: a derived record's `derived_from` must be a real id, not `""` |
| `invalid/connector_one_space.yaml` | `Connector` | fails on `connects` | Exactly two, as `minItems` |
| `invalid/connector_door_missing_clear_height.yaml` | `Connector` | fails on `clear_height` | `clear_height` is a required key on every Connector |
| `invalid/space_missing_source.yaml` | `Space` | fails on `source` | A Space always says where it came from |
| `invalid/space_record_type_mismatch.yaml` | `Space` | fails on `record_type` | A record validated as the wrong class fails on its own type designator, not by chance of the classes' other slots |
| `invalid/storey_id_not_global_id.yaml` | `Storey` | fails on `id` | The pattern is set on every class, not only on components |

All nine error messages were probed on 2026-09-15 with the schema shape above and contain the slot name the harness looks for. `test_lint.py` and `test_dist.py` collect the new files with no change.

What the validator does not check, and who does: that `connects`, `located_in`, `contained_in`, `derived_from`, and `part_of` name ids that exist in the sibling files is a tier 2 check for the projection component. Until then, success criterion 5 checks it by hand. The whole-graph checks this module needs are listed under Deferred to CHECKS.md below.

A Connector cannot be written into `building_components.yaml`: validated as `BuildingComponent`, its `kind` and `connects` are unexpected properties. Probed 2026-09-15. Connectors live in their own file, always.

### Deferred to CHECKS.md

Tier 3 checks this module needs and the schema cannot express, because each reads more than one record. The brief places the tier 3 query set in `CHECKS.md` beside the generator; until that file exists, this table is where product's candidates wait. This is the first spec with such a section; resource's one deferred check, that every id in `offers` names a capability, sits in its Testing Strategy. Each check is a Cypher query that must return zero rows, except the work lists, which return the rows a human must look at.

| Check | Reads | Why not tier 1 |
|---|---|---|
| A Connector's two Spaces are distinct | the Connector's `connects` | LinkML's `list_elements_unique` reaches neither the validator nor the JSON Schema on 1.11.1, probed 2026-09-15 |
| A stair Connector's two Spaces lie on different storeys | each Space's `contained_in` | The storeys are on the Space records, not on the Connector |
| A `derived` component's `derived_from` names a component whose `source` is `ifc` | the target's `source` | The target is another record; tier 2 checks only that it exists |
| A part's `part_of` names a component that is not itself a part | the target's `part_of` | Same; keeps the aggregation one level deep, as IFC assemblies are |
| Work list: every component with `material: ""` | all components | Fixed by the brief as a work list, not a shape error; `""` marks it, not a missing key |
| Work list: every non-part component with `contained_in: ""` | all components | Whether an empty one is a defect or an expected absence depends on trusting the source model's quality, a judgement outside what a shape check can make |
| Work list: every component with `located_in: ""` | all components | Empty on every record until the point-in-space derivation exists; a real gap once it does |
| Work list: every component with a dimension slot's `unit: ""` | `length`, `width`, `height`, `weight` on all components | No `IfcElementQuantity` in this model resolves any of the four, so this flags nothing yet; a real gap once a model that has base quantities is parsed |
| A door or void Connector's `clear_width` and `clear_height` have a real `unit` | all Connectors | Took over from the retired clearance rule (decision 4): a rule cannot look inside a Quantity |
| Work list: every Space with `source: derived` | all Spaces | A derived room or exterior is the derivation's claim; a human confirms it or fixes the model |

## Boundaries

**Always.** Every class, slot, enum, permissible value, and rule has a description. `inlined: true` on every Position and Quantity slot. The GlobalId pattern on `id` in every class. Example documents come from the real model. Rebuild `dist/` and `docs/model/` in the same commit as the YAML. `uv run pytest` passes before committing. Conventional Commits. LF.

**Ask first.** Adding a class or slot beyond the lineage table. A second `is_a` subclass. A second class rule. A fourth `ConnectorKind` value, `window` included. Carrying PredefinedType or ObjectType. A flag or slot that marks the exterior Space. A Building or Site class. A third runtime slot beyond `status` and `current_location`. A second level of `part_of`. Moving a slot into common. Adding a test file.

**Never.** Subclassing `BuildingComponent` by `source` or `permanence`. A default on `permanence` or `source`. An `id` that is not in GlobalId form, or a second identifier slot beside it. A `derived_by` or any record of the producing algorithm. A separate Opening node beside a door. Geometry, property sets, or a material taxonomy. `abstract`, `mixins`, or `union_of`. Graph vocabulary or annotations. Hand edits under `dist/` or `docs/model/`. Redefining a slot common declares. Invented example data.

## Success Criteria

1. `uv run pytest` passes with fourteen new rows collected and passing, and no test file other than `test_examples.py` changed.
2. `dist/product.schema.json` declares draft 2020-12, passes the meta-schema check, and its `$defs` contain exactly `BuildingComponent`, `Connector`, `Space`, `Storey`, `ComponentPermanence`, `RecordSource`, `ConnectorKind`, and common's `Position`, `Quantity`, `Interval`, `CapabilityType` (`ParameterKind` until it moved to process, 2026-09-18). `id` carries the GlobalId pattern in all four class definitions; `Connector.properties` holds every BuildingComponent property plus its four own; `connects` has `minItems: 2` and `maxItems: 2`; `BuildingComponent` and `Connector` each carry a bare `if`/`then` pair, the one `derived_from` rule, which `Connector` inherits and adds nothing to. All probed on 2026-09-15 and 2026-09-16.
3. `dist/README.md` lists `product.schema.json` with the module description.
4. `docs/model/product/index.md` lists the four classes with `Connector` indented under `BuildingComponent`, the three enums, and this module's own slots, every entry with a description. The `BuildingComponent` page shows a Rules table; `Connector`'s does not, since `gen-doc` renders a rule only on the class that declares it, and the inherited one shows in the JSON Schema instead. The folder also holds unlinked pages for common's elements, as in resource.
5. The four example files come from one real model. `building_components.yaml` holds at least one IFC-sourced component with a `material`, one window, one derived component whose `derived_from` names a component in the same file, one temporary component, and, when the model has an element assembly, one part whose `part_of` names its assembly in the same file or in `connectors.yaml`. `connectors.yaml` holds at least one door with clearances, one door whose `connects` names an exterior Space, and one stair. `spaces.yaml` holds one exterior Space per storey with `source: derived` and every id named in `connects` and `located_in`. `storeys.yaml` holds every id named in `contained_in`. Every `id` across the four files is distinct.
6. Every slot declared in `schema/product.yaml` appears in the lineage table or is one of the module's own words listed under Code Style. Checked by reading, recorded as done once.
7. `schema/common.yaml` did not change, and the toolchain did not change. `git log -- schema/common.yaml scripts tests/test_build.py tests/test_lint.py tests/test_dist.py` shows no commit from this module.

## Decisions Made Here

Everything the brief fixed is under Fixed by the brief. The following were decided while writing and reviewing this spec on 2026-09-15. Items marked accepted were reviewed by the author; the rest are open to overturn.

1. **`id` is the GlobalId, and derived records get a minted one in the same format.** Accepted. The graph runs on `id`: every edge, every task parameter. A readable slug such as `wall_017` shifts when the model is re-exported, so `id` had to be the stable thing IFC gives, and a derived record's id had to be as stable. Making the minted id a real GlobalId rather than `<GlobalId>_brick_0001` removes the class rule that tied the pattern to `source: ifc`, puts one unconditional pattern on every class, and leaves derived records ready to be written back into the IFC. How the derivation mints them is its own concern. The separate `ifc_global_id` slot of the first draft is gone as a second copy of `id`. The slot keeps common's name `id`, not `global_id`, so product's classes identify themselves the way every other module's do; the description and pattern carry the meaning.
2. **Every slot in this module is `required: true`, with no exceptions; an unresolved or inapplicable one holds `""` (a string or reference slot) or a Position/Quantity object with `unit: ""` (the seven slots typed that way), never an absent key.** Accepted 2026-09-15, superseding the original two-rule design on `BuildingComponent` (`ifc_type` required when `source` is `ifc`, `derived_from` required when `source` is `derived`) and extending the same reasoning to `name`, `long_name` on every class that carries them, `contained_in` on `Space`, and finally `supply_location`, `current_location`, `length`, `width`, `height`, `weight`, and `Storey.elevation`. The document shape is then identical for every record of a class regardless of what the pipeline has resolved, which is what a graph node's property set needs to be predictable, and a downstream check reads a value rather than testing for a missing key; on a reference slot, `""` renders as no edge at projection time, exactly what absence used to mean.

    Two things are not treated with a plain `""`. `derived_from` keeps a genuine tier 1 guarantee on top of being required: unlike `ifc_type`, which the parser always has on hand, `derived_from` is the output of the derivation's own logic, which can fail or forget, so a rule still requires it to match the GlobalId pattern, not `""`, when `source` is `derived` — probed 2026-09-15, a rule's postcondition can carry `pattern` alongside `required`, rendering correctly in both `gen-json-schema`'s `if`/`then` and `linkml-validate`; this retires the `ifc_type` rule entirely. `Space.contained_in` is required with no `""` case at all: every Space has a storey by construction, so its pattern stays the plain GlobalId form, not the widened one `BuildingComponent`'s use of the same slot needs.

    The Position/Quantity-typed slots looked like a harder case, because a required float has no `""`-equivalent of its own: `0.0` reads as real data, `NaN` is not valid JSON, and `null` is unavailable — the toolchain's `include_null=False` (set for the resource module precisely so "absent key" would be the schema's one, unambiguous way to say "no value") is a single flag for the whole generation call, not something this module can override per slot, and reopening it would undo that fix for every module, not just this one; separately, loosening common's `Position`/`Quantity` to accept an empty object would touch `schema/common.yaml`, which success criterion 7 forbids. The actual resolution needs neither: `Position` and `Quantity` both already carry a plain, unconstrained `unit` string among their required fields, and a resolved one always has a real unit, so `unit: ""` is already a safe, honest "not yet resolved" marker under their existing, unmodified schema — probed 2026-09-15, `{value: 0.0, unit: ""}` validates against `common.Quantity` exactly as it stands today, no `any_of`, no pattern, no schema change of any kind beyond `required: true` on the slot itself. The numeric fields carry `0.0` by convention and are meaningless whenever `unit` is empty; a tiered check reads `unit == ""` the same way it reads a plain slot for `== ""`.
3. **Enums are `ComponentPermanence`, `RecordSource`, `ConnectorKind`.** Accepted. The bare names would collide with their slot pages on Windows. `RecordSource` rather than `ComponentSource` because the enum qualifies Spaces as well.
4. **The clearance rule is retired, 2026-09-16.** It was accepted as one `any_of` rule over `door`, `void`, probed to render in both tools. Once `clear_width` and `clear_height` became required keys on every Connector (decision 2) its `required` postconditions added nothing, and a rule cannot look inside a Quantity to demand a real `unit`, so it could not be narrowed the way `derived_from`'s was. Retired for the same reason as the `ifc_type` rule: a door's clearances are read straight off `OverallWidth` and `OverallHeight`; whether one is real is a tier 3 check.
5. **`connects` is `minimum_cardinality: 2` plus `maximum_cardinality: 2` plus `required`.** Accepted. LinkML's `exact_cardinality` and `list_elements_unique` pass the linter but reach neither the validator nor the JSON Schema on 1.11.1, probed 2026-09-15; the bounds render as `minItems` and `maxItems` and apply only when the slot is present, so `required` is needed too.
6. **`elevation` is a `Quantity`, not a float.** Accepted. Every other length in the model carries its unit.
7. **An element assembly and its parts are all components, joined by `part_of`.** Accepted. Parts carry their own GlobalIds and are what a robot installs, while the whole is what connects storeys, so both are needed and one slot joins them. The slot sits on the part and points at the whole, IFC's `Decomposes` direction, single-valued; the reverse is a query. Named `part_of` rather than IFC's `decomposes` because the plain words say the direction.
8. **The exterior is one derived Space per storey, and nothing in the schema marks it.** Accepted. A single exterior node made every exterior door and roof stair meet at one place, so a path could leave a third-floor balcony and arrive at the front door. One exterior per storey, joined only by real Connectors, gives true paths. It is recognised by `source: derived` and by its id rule in the derivation; a boolean borrowed from IFC's `IsExternal` was considered and declined as a slot for a fact the derivation already records.
9. **Windows are not Connectors.** Accepted. Nothing planned passes through a window, and a window wired to the exterior was the other source of false paths. `ConnectorKind` is `door`, `void`, `stair`; `IfcWindow` is a plain BuildingComponent.
10. **`source` on Space.** Accepted. Rooms may be derived from wall footprints when a file has no `IfcSpace`, and every exterior Space is derived. A record that the derivation invented must say so, because "no GlobalId" can no longer say it.
11. **The contract promises topology for every model, and the derivation owes it.** Accepted. Structural and fabrication models without spaces are in scope, so the derivation cuts rooms from wall footprints rather than leaving `connects` empty. The alternative, `connects` optional and empty on spaceless models, was declined because it would let absence carry meaning.
12. **Example files are one per class, four files.** Accepted. A Connector cannot sit in the BuildingComponent file, and Space and Storey are separate classes.
13. **Invalid documents, one per mechanism per class, however many that takes.** Accepted in principle, "however many we need to properly test"; ten as of decisions 2 and 16. A plain required slot, the pattern on a component and on a Storey, `ifc_type` and `derived_from` as required keys, the one class rule (`derived_from` must be a real id when `source` is `derived`), `clear_height` as a required key on a Connector, the cardinality, `source` on Space, and a wrong `record_type` value.
14. **Tier 3 candidates are named, not modelled**, in the section Deferred to CHECKS.md, so they are in one place when the generator's `CHECKS.md` is written. Accepted; the section heading is this spec's own, not an existing convention.
15. **Splitting `BuildingComponent` by `source` into two classes was considered and declined, 2026-09-15.** An abstract base plus an ifc-sourced and a derived subclass would have retired the same two rules for free, via `is_a` slot inheritance the way `Connector` already uses, and let a derived record's identifier not pretend to be GlobalId-shaped. It was declined because it only pays off for the two slots that already had a working rule; `material`, `part_of`, `located_in`, and `contained_in` have the identical shape question and are orthogonal to `source`, so the split would not have touched them, and it reopens "Fixed by the brief: subclassed by kind only, never by source" for a narrower win than decision 2 gives across all six slots at once, in the existing single-class shape.
16. **Every record carries `record_type`, a LinkML type designator naming its own class, added 2026-09-16.** This reverses the original draft's Boundaries, which listed `designates_type` under Never; the reversal is deliberate, not an oversight, and this entry is that Never line's replacement. The four example files stay one per class; nothing about document layout changed. The four classes already differing in required slots meant a document validated against the wrong class was likely, but not guaranteed, to fail; `record_type` makes it a designed, unconditional guarantee, chosen deliberately over relying on that coincidence as the schema's slots evolve. Declared once, `range: string`, `designates_type: true`, reused by all four classes exactly as `id` is; `Connector` inherits it from `BuildingComponent` without a separate declaration, and LinkML computes the class's own name as the locked value from whichever class is actually being generated, confirmed by generating `Connector`'s own schema directly (`record_type` there locks to `"Connector"`, not `"BuildingComponent"`). `linkml-validate`'s `-C`/`--target-class` remains the mechanism that selects which class's schema a run checks against; `record_type` does not replace it and does not make `-C` optional, it only guarantees a mismatch is caught. `invalid/space_record_type_mismatch.yaml` pins the guarantee: a real Space record with `record_type: Storey` fails naming `record_type` alone. Considered as an alternative to the four-file layout (one shared, self-describing collection per LinkML's own property-graph howto pattern, `Node`/`category` and `Edge`/`predicate`) and kept independent of it: the combined-collection question stays open, `designates_type` was adopted on its own merits regardless of how it is decided.

## Open Questions

None. Every model this contract is fed carries storeys, so the exterior Space per storey and `contained_in` always have a Storey to hang on. Every probe this spec relies on ran on 2026-09-15 against LinkML 1.11.1 and is recorded in the section that uses it.
