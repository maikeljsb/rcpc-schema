# Spec: product

*Module `product` of `CAPABILITY-MAP.md`. Drafted 2026-09-15, reviewed the same day, awaiting the author's approval. Depends on `common`. Imported by `process`. Direction fixed by the brief's Product Side and its dated decisions; IFC lineage from `docs/research/ifc43-for-product.md`; derivation limits from `docs/research/topologicpy-for-product.md`; metamodel usage follows `docs/research/linkml-metamodel-conformance-and-inheritance.md`.*

## Objective

Give the process side something to build: a building component identified by an IFC GlobalId, parsed or minted, with the material string a method matches on, the point a placement task binds to, and the light spatial topology that says where it is and what a robot passes through to reach it. Deliver it as `schema/product.yaml`, with example documents taken from a real model, generated JSON Schema, and generated documentation.

**Users.** The IFC parser and the derivation, later, which fill BuildingComponents, Spaces, Storeys, and Connectors from a model. The person resolving a parsed model, who adds derived components such as bricks and fills missing materials. The process module, whose methods match `material` and whose primitives reference components by id. The projection component, which turns `derived_from`, `part_of`, `located_in`, `contained_in`, and `connects` into edges. Other project teams, who read `docs/model/product/`.

**Success in one sentence.** `schema/product.yaml` lints clean, the four example documents from the real model validate and the eight invalid documents fail naming their slot, the toolchain produces its JSON Schema and docs unchanged, and every row of the lineage table below names the IFC construct it borrows or adapts.

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
      building_component_ifc_missing_ifc_type.yaml      source ifc, no ifc_type
      building_component_derived_missing_derived_from.yaml   source derived, no derived_from
      connector_one_space.yaml                          connects lists one Space
      connector_door_missing_clear_height.yaml          kind door, no clear_height
      space_missing_source.yaml                         a Space without source
      storey_id_not_global_id.yaml                      a Storey whose id is not a GlobalId
dist/
  product.schema.json                                   generated
  README.md                                             regenerated, now lists product
docs/
  model/
    product/                                            generated, one page per element
tests/
  test_examples.py                                      twelve rows added to EXAMPLES, nothing else
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
| `BuildingComponent` | `id`, `ifc_type`, `name`, `material`, `permanence`, `source`, `derived_from`, `part_of`, `target_location`, `supply_location`, `current_location`, `located_in`, `contained_in`, `length`, `width`, `height`, `weight` | One thing a task acts on. Required: `id`, `permanence`, `source`, `target_location`. Two class rules: `source: ifc` requires `ifc_type`; `source: derived` requires `derived_from`. |
| `Connector` | the BuildingComponent slots plus `kind`, `connects`, `clear_width`, `clear_height` | `is_a BuildingComponent`, the model's one subclass. A door, an unfilled opening, or a stair as one node: the component a task installs and the passage a robot fits through. Required: `kind`, `connects` with exactly two Spaces. One class rule of its own: kind `door` or `void` requires `clear_width` and `clear_height`; kind `stair` leaves both optional. Inherits the two BuildingComponent rules. |
| `Space` | `id`, `name`, `long_name`, `source`, `contained_in` | A room, or the exterior region of one storey. Parsed from `IfcSpace`, or derived: rooms cut from wall footprints when the file has no spaces, and one exterior Space per storey so that an exterior door and a roof stair have two ends. Required: `id`, `source`. |
| `Storey` | `id`, `name`, `long_name`, `elevation` | A building storey. Always parsed. Required: `id`. |

All four classes carry an identifier and project to nodes. `derived_from`, `part_of`, `located_in`, `contained_in`, and `connects` are reference slots and project to edges. `Position` and `Quantity` have no identifier and flatten into the node that holds them.

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
| `ifc_type` | string | The bare IFC entity name, such as `IfcWall`. No PredefinedType, no ObjectType. Required by rule when `source` is `ifc`. |
| `name` | string | The IFC Name. Optional everywhere. |
| `long_name` | string | The IFC LongName of a Space or Storey. Optional. |
| `material` | `MaterialName` | The one material string the parser derives, exactly as the IFC spells it. Optional; a component without one is a tier 3 work item. |
| `permanence` | `ComponentPermanence` | Required, no default. |
| `source` | `RecordSource` | Required on BuildingComponent and Space, no default. |
| `derived_from` | `BuildingComponent`, not inlined | The IFC-sourced component this one was generated from. Required by rule when `source` is `derived`. |
| `part_of` | `BuildingComponent`, not inlined | The assembly this component is a part of, IFC's aggregation from the part's side. A stair flight is `part_of` its stair. Optional; single-valued because an IFC element decomposes at most one whole. |
| `target_location` | `Position`, `inlined: true` | The centroid of the component's body in the IFC project frame, in the project length unit. Where the design puts it and what a placement task binds to. Required. |
| `supply_location` | `Position`, `inlined: true` | Where the component is delivered or staged. Optional. |
| `current_location` | `Position`, `inlined: true` | Where the component is now. Written by execution; the model's second runtime slot after `status`. Optional. |
| `located_in` | `Space`, not inlined | The Space the component's point lies in. Empty for walls and slabs. |
| `contained_in` | `Storey`, not inlined | IFC's containment relation under its own name. On a BuildingComponent, its storey; on a Space, the storey that aggregates it or, for a derived Space, the storey it was cut for. |
| `kind` | `ConnectorKind` | Required on Connector. |
| `connects` | `Space`, multivalued, not inlined, `minimum_cardinality: 2`, `maximum_cardinality: 2` | The two Spaces a Connector joins. Required on Connector. A stair's two Spaces are on different storeys. |
| `clear_width` | `Quantity`, `inlined: true` | The passable width. For a door the IFC OverallWidth, with the opening's geometry as fallback; for a void the opening's geometry; for a stair the flight width, read from geometry. |
| `clear_height` | `Quantity`, `inlined: true` | The passable height. For a door the IFC OverallHeight, with the opening's geometry as fallback; for a void the opening's geometry; for a stair the headroom, read from geometry. |
| `elevation` | `Quantity`, `inlined: true` | The storey's level in the project frame. Optional. |

Reused from common: `id`, `length`, `width`, `height`, `weight` as slots; `Position`, `Quantity`, `MaterialName` as ranges. Every Position and Quantity slot states `inlined: true` so the document shape is visible in the YAML; reference slots state nothing, so a reader sees which slots are references.

### Class rules

Three rules, all tier 1: `linkml-validate` enforces them and `gen-json-schema` renders each as an `if`/`then` block under `allOf`. Probed 2026-09-15 on LinkML 1.11.1; each failure names the missing slot in its message. `Connector` inherits the first two, so its `allOf` holds three blocks.

| Class | If | Then required |
|---|---|---|
| `BuildingComponent` | `source` equals `ifc` | `ifc_type` |
| `BuildingComponent` | `source` equals `derived` | `derived_from` |
| `Connector` | `kind` is any of `door`, `void` | `clear_width`, `clear_height` |

### What the derivation must deliver

Instances of this module are derived, not authored, and the derivation is a later slice with its own plan. This contract fixes what that slice owes the schema, so the constraints above are promises the derivation keeps rather than errors buildings produce.

- Every record gets an `id` in GlobalId form: the entity's own when parsed, minted when derived, the same on every run.
- Every model gets Spaces. When the file carries `IfcSpace`, they are parsed. When it does not, rooms are cut from wall footprints per storey and marked `source: derived`. Structural and fabrication models without spaces are in scope.
- Every storey gets one exterior Space, `source: derived`, `contained_in` that storey, so that a ground-floor door, a balcony door, and a roof stair each have two ends that are not the same node. When the file carries `IfcExternalSpatialElement`, the ground storey's exterior takes its GlobalId and `source: ifc`.
- Every Connector gets exactly two Spaces. A Connector with one end is a derivation bug, and tier 1 catches it.
- Windows are parsed as BuildingComponents and never as Connectors.
- Every derived Space is a line on the human work list, confirmed as a real exterior or room, or a sign the model is missing one.

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
| `id` on every class, matching the GlobalId pattern | It projects to a node, a node needs an identifier, and the identifier must survive a re-parse of the model. |
| `BuildingComponent.permanence`, `source` | An unknown lifetime or provenance is a hole in the plan; a default would mislabel temporary works. |
| `BuildingComponent.target_location` | A placement task has nothing to bind to without it. |
| `ifc_type` when `source` is `ifc` | Without the entity name nothing says what was parsed. |
| `derived_from` when `source` is `derived` | The wall-to-bricks relationship must be in the graph. |
| `Space.source` | A derived room or exterior must say so, because it is a claim the derivation made, not a fact the model carried. |
| `Connector.kind`, `connects` with exactly two Spaces | A passage with one end is not a passage; the kind says how to read the clearances. |
| `clear_width`, `clear_height` when `kind` is `door` or `void` | The fit-through check has nothing to compare otherwise. IFC carries the values as door attributes and as opening geometry. |
| Every `Position`'s three coordinates and unit, every `Quantity`'s value and unit | Enforced by common. |

Everything else is optional. A component with `id`, `permanence`, `source: derived`, `derived_from`, and `target_location` is valid.

### One storey of a building, as documents

`storeys.yaml`:

```yaml
- id: 3ZYW59sxj8lei475l7EhLU
  name: "00"
  long_name: Ground floor
  elevation: {value: 0.0, unit: m}
```

`spaces.yaml`:

```yaml
- id: 0jf0rYHfX3RAB3bSIRjmmy
  name: exterior 00
  source: derived
  contained_in: 3ZYW59sxj8lei475l7EhLU
- id: 1hOSvn6df7F8_7GcBWlRGQ
  name: "001"
  long_name: Entrance hall
  source: ifc
  contained_in: 3ZYW59sxj8lei475l7EhLU
```

`building_components.yaml`:

```yaml
- id: 3bXiCStxP6Fgxdej$yc50n
  ifc_type: IfcWall
  name: Basic Wall:Exterior - Brick on Block:138157
  material: Brick
  permanence: permanent
  source: ifc
  target_location: {x_coord: 4.25, y_coord: 0.15, z_coord: 1.40, unit: m}
  contained_in: 3ZYW59sxj8lei475l7EhLU
  length: {value: 8.5, unit: m}
  width: {value: 0.3, unit: m}
  height: {value: 2.8, unit: m}
- id: 2O2Fr$t4X7Zf8NOew3FLTF
  name: brick 0001 of Basic Wall:Exterior - Brick on Block:138157
  material: Brick
  permanence: permanent
  source: derived
  derived_from: 3bXiCStxP6Fgxdej$yc50n
  target_location: {x_coord: 0.12, y_coord: 0.15, z_coord: 0.04, unit: m}
  located_in: 1hOSvn6df7F8_7GcBWlRGQ
  contained_in: 3ZYW59sxj8lei475l7EhLU
```

`connectors.yaml`:

```yaml
- id: 3KMJUyUe9DfQ2FOCd5ZoiN
  ifc_type: IfcDoor
  name: Entrance door
  permanence: permanent
  source: ifc
  target_location: {x_coord: 2.1, y_coord: 0.15, z_coord: 1.05, unit: m}
  contained_in: 3ZYW59sxj8lei475l7EhLU
  kind: door
  connects: [0jf0rYHfX3RAB3bSIRjmmy, 1hOSvn6df7F8_7GcBWlRGQ]
  clear_width: {value: 0.9, unit: m}
  clear_height: {value: 2.1, unit: m}
```

The values above show the shape. The committed files hold the real model's values.

### Fixed by the brief

Four classes, one `is_a`. `BuildingComponent` subclassed by kind only, never by source or permanence. `permanence` and `source` required with no default. `id` is the GlobalId, parsed or minted. `derived_from` rule-required; the producing algorithm not recorded. `material` optional, a missing one a tier 3 query. `target_location` required and a centroid; `supply_location` and `current_location` optional. The exterior is a Space per storey; `connects` exactly two. `Storey` a class identified by its GlobalId. `name` and `long_name` optional everywhere. `contained_in` ranges Storey and is reused for Space; `located_in` is the component-to-Space relation. Connectors are doors, voids, and stairs; a stair's clearances are optional. Instances are derived, not authored; the derivation is a later slice.

## Code Style

The module follows `SPEC-toolchain.md` and `SPEC-common.md`. The component class with its identifier pattern and two rules, as it will appear:

```yaml
classes:
  BuildingComponent:
    description: >-
      One thing a task acts on. Parsed from the IFC model or derived from a
      parsed component; permanent or temporary.
    slots:
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
    rules:
      - description: An IFC-sourced component carries its entity name.
        preconditions:
          slot_conditions:
            source:
              equals_string: ifc
        postconditions:
          slot_conditions:
            ifc_type:
              required: true
      - description: A derived component names the component it came from.
        preconditions:
          slot_conditions:
            source:
              equals_string: derived
        postconditions:
          slot_conditions:
            derived_from:
              required: true
```

Conventions specific to this module:

- **Names follow the linter's `standard_naming` rule**: CamelCase classes and enums, snake_case slots and permissible values.
- **IFC names stay recognisable.** `ifc_type`, `name`, `long_name`, `contained_in`, and `elevation` are IFC's words in snake_case. The module's own words are `located_in`, `connects`, `kind`, `derived_from`, `part_of`, `permanence`, `source`, and the three location slots.
- **Attribution only where the meaning changed.** Adapted slots say in one sentence what the parser does to the IFC value; borrowed slots say what the IFC attribute is; the module's own slots do not mention IFC.
- **Enums are named after what they qualify**: `ComponentPermanence`, `RecordSource`, `ConnectorKind`, so no enum page collides with its slot page.
- **Every rule has a `description`**, one sentence in the indicative, so the generated Rules table reads as prose.
- **`inlined: true` on every Position and Quantity slot**, nothing on reference slots.
- **Ids are GlobalIds, names are for people.** A derived record's `name` says what it is and what it came from, as in the brick above, because its id says nothing a reader can use.

## Testing Strategy

No new test files. Twelve rows in `EXAMPLES`.

| Document | Class | Expected | Proves |
|---|---|---|---|
| `examples/product/building_components.yaml` | `BuildingComponent` | validates | IFC-sourced and derived components, a temporary one, a window, a part with `part_of`, the dimension slots, `located_in` and `contained_in` |
| `examples/product/connectors.yaml` | `Connector` | validates | A door with clearances, a stair without, an exterior door whose second Space is an exterior; inherited slots plus the four of its own |
| `examples/product/spaces.yaml` | `Space` | validates | Parsed rooms, one derived exterior per storey, `source` on each |
| `examples/product/storeys.yaml` | `Storey` | validates | Every storey the other files reference |
| `invalid/building_component_missing_permanence.yaml` | `BuildingComponent` | fails on `permanence` | A plain required enum slot |
| `invalid/building_component_id_not_global_id.yaml` | `BuildingComponent` | fails on `id` | The GlobalId pattern reaches the validator |
| `invalid/building_component_ifc_missing_ifc_type.yaml` | `BuildingComponent` | fails on `ifc_type` | The first class rule |
| `invalid/building_component_derived_missing_derived_from.yaml` | `BuildingComponent` | fails on `derived_from` | The second class rule |
| `invalid/connector_one_space.yaml` | `Connector` | fails on `connects` | Exactly two, as `minItems` |
| `invalid/connector_door_missing_clear_height.yaml` | `Connector` | fails on `clear_height` | The third class rule |
| `invalid/space_missing_source.yaml` | `Space` | fails on `source` | A Space always says where it came from |
| `invalid/storey_id_not_global_id.yaml` | `Storey` | fails on `id` | The pattern is set on every class, not only on components |

All eight error messages were probed on 2026-09-15 with the schema shape above and contain the slot name the harness looks for. `test_lint.py` and `test_dist.py` collect the new files with no change.

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
| Work list: every component with no `material` | all components | Fixed by the brief as a work list, not a shape error |
| Work list: every Space with `source: derived` | all Spaces | A derived room or exterior is the derivation's claim; a human confirms it or fixes the model |

## Boundaries

**Always.** Every class, slot, enum, permissible value, and rule has a description. `inlined: true` on every Position and Quantity slot. The GlobalId pattern on `id` in every class. Example documents come from the real model. Rebuild `dist/` and `docs/model/` in the same commit as the YAML. `uv run pytest` passes before committing. Conventional Commits. LF.

**Ask first.** Adding a class or slot beyond the lineage table. A second `is_a` subclass. A fourth class rule. A fourth `ConnectorKind` value, `window` included. Carrying PredefinedType or ObjectType. A flag or slot that marks the exterior Space. A Building or Site class. A third runtime slot beyond `status` and `current_location`. A second level of `part_of`. Moving a slot into common. Adding a test file.

**Never.** Subclassing `BuildingComponent` by `source` or `permanence`. A default on `permanence` or `source`. An `id` that is not in GlobalId form, or a second identifier slot beside it. A `derived_by` or any record of the producing algorithm. A separate Opening node beside a door. Geometry, property sets, or a material taxonomy. `abstract`, `mixins`, `union_of`, or `designates_type`. Graph vocabulary or annotations. Hand edits under `dist/` or `docs/model/`. Redefining a slot common declares. Invented example data.

## Success Criteria

1. `uv run pytest` passes with twelve new rows collected and passing, and no test file other than `test_examples.py` changed.
2. `dist/product.schema.json` declares draft 2020-12, passes the meta-schema check, and its `$defs` contain exactly `BuildingComponent`, `Connector`, `Space`, `Storey`, `ComponentPermanence`, `RecordSource`, `ConnectorKind`, and common's `Position`, `Quantity`, `Interval`, `CapabilityType`, `ParameterKind`. `id` carries the GlobalId pattern in all four class definitions; `Connector.properties` holds every BuildingComponent property plus its four own; `connects` has `minItems: 2` and `maxItems: 2`; `BuildingComponent` carries an `allOf` of two `if`/`then` blocks and `Connector` one of three. All probed on 2026-09-15.
3. `dist/README.md` lists `product.schema.json` with the module description.
4. `docs/model/product/index.md` lists the four classes with `Connector` indented under `BuildingComponent`, the three enums, and this module's own slots, every entry with a description. The `BuildingComponent` and `Connector` pages each show a Rules table. The folder also holds unlinked pages for common's elements, as in resource.
5. The four example files come from one real model. `building_components.yaml` holds at least one IFC-sourced component with a `material`, one window, one derived component whose `derived_from` names a component in the same file, one temporary component, and, when the model has an element assembly, one part whose `part_of` names its assembly in the same file or in `connectors.yaml`. `connectors.yaml` holds at least one door with clearances, one door whose `connects` names an exterior Space, and one stair. `spaces.yaml` holds one exterior Space per storey with `source: derived` and every id named in `connects` and `located_in`. `storeys.yaml` holds every id named in `contained_in`. Every `id` across the four files is distinct.
6. Every slot declared in `schema/product.yaml` appears in the lineage table or is one of the module's own words listed under Code Style. Checked by reading, recorded as done once.
7. `schema/common.yaml` did not change, and the toolchain did not change. `git log -- schema/common.yaml scripts tests/test_build.py tests/test_lint.py tests/test_dist.py` shows no commit from this module.

## Decisions Made Here

Everything the brief fixed is under Fixed by the brief. The following were decided while writing and reviewing this spec on 2026-09-15. Items marked accepted were reviewed by the author; the rest are open to overturn.

1. **`id` is the GlobalId, and derived records get a minted one in the same format.** Accepted. The graph runs on `id`: every edge, every task parameter. A readable slug such as `wall_017` shifts when the model is re-exported, so `id` had to be the stable thing IFC gives, and a derived record's id had to be as stable. Making the minted id a real GlobalId rather than `<GlobalId>_brick_0001` removes the class rule that tied the pattern to `source: ifc`, puts one unconditional pattern on every class, and leaves derived records ready to be written back into the IFC. How the derivation mints them is its own concern. The separate `ifc_global_id` slot of the first draft is gone as a second copy of `id`. The slot keeps common's name `id`, not `global_id`, so product's classes identify themselves the way every other module's do; the description and pattern carry the meaning.
2. **`ifc_type` is required by rule when `source` is `ifc`.** Accepted. A derived brick has no entity name to give; an IFC-sourced component always does.
3. **Enums are `ComponentPermanence`, `RecordSource`, `ConnectorKind`.** Accepted. The bare names would collide with their slot pages on Windows. `RecordSource` rather than `ComponentSource` because the enum qualifies Spaces as well.
4. **One clearance rule with `any_of` over `door`, `void`**, not one rule per kind. Accepted. Probed: `linkml-validate` and `gen-json-schema` both honour it.
5. **`connects` is `minimum_cardinality: 2` plus `maximum_cardinality: 2` plus `required`.** Accepted. LinkML's `exact_cardinality` and `list_elements_unique` pass the linter but reach neither the validator nor the JSON Schema on 1.11.1, probed 2026-09-15; the bounds render as `minItems` and `maxItems` and apply only when the slot is present, so `required` is needed too.
6. **`elevation` is a `Quantity`, not a float.** Accepted. Every other length in the model carries its unit.
7. **An element assembly and its parts are all components, joined by `part_of`.** Accepted. Parts carry their own GlobalIds and are what a robot installs, while the whole is what connects storeys, so both are needed and one slot joins them. The slot sits on the part and points at the whole, IFC's `Decomposes` direction, single-valued; the reverse is a query. Named `part_of` rather than IFC's `decomposes` because the plain words say the direction.
8. **The exterior is one derived Space per storey, and nothing in the schema marks it.** Accepted. A single exterior node made every exterior door and roof stair meet at one place, so a path could leave a third-floor balcony and arrive at the front door. One exterior per storey, joined only by real Connectors, gives true paths. It is recognised by `source: derived` and by its id rule in the derivation; a boolean borrowed from IFC's `IsExternal` was considered and declined as a slot for a fact the derivation already records.
9. **Windows are not Connectors.** Accepted. Nothing planned passes through a window, and a window wired to the exterior was the other source of false paths. `ConnectorKind` is `door`, `void`, `stair`; `IfcWindow` is a plain BuildingComponent.
10. **`source` on Space.** Accepted. Rooms may be derived from wall footprints when a file has no `IfcSpace`, and every exterior Space is derived. A record that the derivation invented must say so, because "no GlobalId" can no longer say it.
11. **The contract promises topology for every model, and the derivation owes it.** Accepted. Structural and fabrication models without spaces are in scope, so the derivation cuts rooms from wall footprints rather than leaving `connects` empty. The alternative, `connects` optional and empty on spaceless models, was declined because it would let absence carry meaning.
12. **Example files are one per class, four files.** Accepted. A Connector cannot sit in the BuildingComponent file, and Space and Storey are separate classes.
13. **Eight invalid documents, one per mechanism per class.** Accepted in principle, "however many we need to properly test". A plain required slot, the pattern on a component and on a Storey, each of the three class rules, the cardinality, and `source` on Space.
14. **Tier 3 candidates are named, not modelled**, in the section Deferred to CHECKS.md, so they are in one place when the generator's `CHECKS.md` is written. Accepted; the section heading is this spec's own, not an existing convention.

## Open Questions

None. Every model this contract is fed carries storeys, so the exterior Space per storey and `contained_in` always have a Storey to hang on. Every probe this spec relies on ran on 2026-09-15 against LinkML 1.11.1 and is recorded in the section that uses it.
