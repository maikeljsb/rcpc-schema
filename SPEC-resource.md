# Spec: resource

*Module `resource` of `CAPABILITY-MAP.md`. Approved 2026-09-12; extended 2026-09-22 by `Resource` and `Stock` under `SPEC-stock.md` (decision 14). Depends on `common`. Imported by `process`. Direction fixed by `docs/ideas/robot-entry-as-type.md`; metamodel usage follows `docs/research/linkml-metamodel-conformance-and-inheritance.md`.*

## Objective

Let someone enter a robot from its Construction Robot Schema (CRS, Li et al. 2026) attributes alone and get, from that one entry, what planning and orchestration need: the capabilities the robot offers, how many identical machines there are, and a machine node to point at. Since 2026-09-22, also let someone enter a stock a method draws on, formwork or rebar, with how many units there are and whether a unit comes back (`SPEC-stock.md`). Deliver it as `schema/resource.yaml`, with fictional example entries, generated JSON Schema, and generated documentation.

**Users.** The person cataloguing robots, who fills a spec sheet into one YAML entry. The process module, which requires capability types that an entry's `Activity` offers and which points `assigned_unit` at a machine node. The projection component, which expands `count` into machine nodes. Other project teams, who read `docs/model/resource/`.

**Success in one sentence.** `schema/resource.yaml` lints clean, the example entries validate and the four invalid documents fail naming their slot, the toolchain produces its JSON Schema and docs unchanged, and every one of the paper's 56 attributes has exactly one row in the lineage table below.

**What this module deliberately is not.** It carries no robot type, no runtime state beyond `status`, no closed value sets the paper does not publish, and nothing the process side owns: no durations, no assigned-machine slot, no activity types or materials.

## Tech Stack

Inherited from `SPEC-toolchain.md` unchanged. This module adds no dependency.

## Commands

```
uv run linkml-lint schema/resource.yaml
uv run linkml-validate -s schema/resource.yaml -C RobotUnit examples/resource/robot_units.yaml
uv run linkml-validate -s schema/resource.yaml -C Stock examples/resource/stocks.yaml
uv run python scripts/build.py          # produces dist/resource.schema.json, dist/README.md, docs/model/resource/
uv run pytest
```

## Project Structure

Files this module adds.

```
schema/
  resource.yaml                            the module
examples/
  resource/
    robot_units.yaml                       two fictional robots, one with count 2
    stocks.yaml                            formwork_panels, temporary, count 2; rebar, permanent, count 20 (2026-09-22)
    invalid/
      robot_unit_missing_activity.yaml     entry without an Activity group
      robot_unit_zero_count.yaml           count: 0
      robot_unit_group_missing_id.yaml     a PhysicalProperty group without an id
      activity_missing_offers.yaml         an Activity group without offers
      stock_missing_permanence.yaml        a stock without permanence (2026-09-22)
dist/
  resource.schema.json                     generated
  README.md                                regenerated, now lists resource
docs/
  model/
    resource/                              generated, one page per element
tests/
  test_examples.py                         five rows added to EXAMPLES, nothing else; two more for the stocks (2026-09-22)
```

## Prerequisite change to common

Four Quantity slots move to common because product will need them too and product does not import resource: `length`, `width`, `height`, `weight`. Slots are global to the merged schema, so a slot both modules use must be declared in the one module both import. `SPEC-common.md` is amended in the same review; the YAML change is the first task of this module's plan. The same rule moves `ComponentPermanence` and `permanence` from product to common on 2026-09-22, because `Stock` carries them (`SPEC-common.md` decision 18).

## The Model

### Schema header

```yaml
id: https://rcpc.for5672/schema/resource
name: resource
version: 0.1.0
description: >-
  Robots as resources. One RobotUnit entry per robot product, holding the four
  Construction Robot Schema groups and the capabilities the robot offers.
prefixes:
  rcpc: https://rcpc.for5672/schema/
  linkml: https://w3id.org/linkml/
default_prefix: rcpc
default_range: string
imports:
  - linkml:types
  - common
```

### Classes

| Class | Slots | Notes |
|---|---|---|
| `Resource` | `id`, `count` | Something a method draws on, counted in identical units. The base `RobotUnit` and `Stock` are `is_a`, declaring the two shared slots once; never written as a record. No `record_type`: no file mixes the two classes, each validates with `-C` on its own. Added 2026-09-22, decision 14. |
| `RobotUnit` | the two of `Resource`, plus `status`, `physical_property_group`, `operational_requirement_group`, `safety_group`, `activity_group` | The entry. One per robot product; identical machines are one entry with a higher `count`. `id` is a readable product slug and is the CRS Name. Required: `id`, `count`, `activity_group`. |
| `Stock` | the two of `Resource`, plus `permanence` | A stock a method uses one unit of: formwork panels, rebar. `id` matches `^[A-Za-z][A-Za-z0-9_]*$`, an HDDL name, because the export writes it as a type. `permanence` says what happens to a unit a method takes: `temporary`, it comes back when the method ends; `permanent`, it is consumed. Required: all three. Added 2026-09-22, decision 14. |
| `PhysicalProperty` | `id`, 22 attribute slots, `sensors` | CRS group 1. Holds the robot's sensors as a list of `Sensor` objects. |
| `Sensor` | `id`, `sensor_type`, `sensor_requirements`, `sensor_location` | One sensor mounted on the robot. Carries the CRS sensor attributes, so it belongs to the PhysicalProperty group one hop down. Required: `id`. |
| `OperationalRequirement` | `id`, 6 attribute slots | CRS group 2. |
| `Safety` | `id`, 6 attribute slots | CRS group 3. |
| `Activity` | `id`, `offers`, 9 attribute slots | CRS group 4. The one required group, because `offers` is required. |

Every group class and `Sensor` has an authored `id`, so by the projection rule it becomes a node with an edge from its holder, whether written inline or by reference. `Quantity`, `Position`, and `Interval` have no `id` and flatten into the node that holds them. Every `Position` on this side is an installation point on the robot body, in the robot's own frame, and carries its unit.

### Enum

| Enum | Values | Notes |
|---|---|---|
| `RobotStatus` | `idle`, `deployed`, `charging`, `out_of_service` | The runtime state of one machine. Default `idle` via `ifabsent`. The validator and the generated JSON Schema ignore `ifabsent`; the projection component writes the default onto every machine node. |

### Slots declared in this module

The group slots on `RobotUnit`: `physical_property_group`, `operational_requirement_group`, `safety_group`, `activity_group`, each single-valued, `inlined: true`, ranging the class named before the `_group` suffix. The suffix is there because a slot named plain `activity` or `safety` collides with its class's own generated doc page on a case-insensitive filesystem (both would write to `Activity.md`/`activity.md`, indistinguishable on Windows); all four carry it so the pointer slots read alike. `sensors` on `PhysicalProperty`: multivalued, `inlined: true`, `inlined_as_list: true`, range `Sensor`. `count`: `integer`, `minimum_value: 1`, required, on `Resource` since 2026-09-22: how many identical units the entry stands for, machines of a robot or units of a stock, one unit being what one method use takes; the projection mints `<id>_<n>` for each. `status`: range `RobotStatus`, `ifabsent: RobotStatus(idle)`, on `RobotUnit` only. `offers`: multivalued, range `CapabilityType`, not inlined, so a document carries capability ids. Plus the attribute slots in the lineage table. Every object-valued slot states `inlined: true` even where LinkML would infer it, so the document shape is visible in the YAML.

Reused from common: `id`, the four dimension slots, and since 2026-09-22 `permanence` as slots; `Position`, `Quantity`, `Interval`, and `ComponentPermanence` as ranges.

### Lineage: CRS attribute to slot

Every row is one attribute of the paper's Table 3, in the paper's order. "Type" is the paper's data type. `Quantity` means an inlined common `Quantity`, value and unit. Recommended units are for the example documents and are not enforced. Attributes that keep the CRS name carry no attribution in their description; renamed, split, or merged ones name their origin.

**Physical Property, 29 attributes**

| CRS attribute | Type | Slot | Class | Range | Note |
|---|---|---|---|---|---|
| Name | String | `id` | `RobotUnit` | string | Renamed. Description says it is the CRS Name. |
| Manufacturer | String | `manufacturer` | `PhysicalProperty` | string | |
| Level of Autonomy | Enum | `level_of_autonomy` | `PhysicalProperty` | string | Open; the paper publishes no values. |
| Network | Enum | `network` | `PhysicalProperty` | string | Open. |
| Length | Decimal | `length` | `PhysicalProperty` | Quantity, m | Declared in common. |
| Width | Decimal | `width` | `PhysicalProperty` | Quantity, m | Declared in common. |
| Height | Decimal | `height` | `PhysicalProperty` | Quantity, m | Declared in common. |
| Weight | Decimal | `weight` | `PhysicalProperty` | Quantity, kg | Declared in common. |
| Load Capacity | Decimal | `load_capacity` | `PhysicalProperty` | Quantity, kg | |
| Mobility | Enum | `mobility` | `PhysicalProperty` | string | Open. |
| Speed | Decimal | `speed` | `PhysicalProperty` | Quantity, m/s | |
| Navigation | Bool | `navigation` | `PhysicalProperty` | boolean | |
| Power Source | Enum | `power_source` | `PhysicalProperty` | string | Open. |
| Run Duration | Decimal | `run_duration` | `PhysicalProperty` | Quantity, min | |
| Sensor Type | String | `sensor_type` | `Sensor` | string | One per sensor object. |
| Sensor Location | String | `sensor_location` | `Sensor` | Position | Type changed from prose to a point in the robot's own frame. |
| Sensor Requirements | String | `sensor_requirements` | `Sensor` | string | |
| Sensor Capability | String | dropped | | | Covered by `sensor_type`. |
| End Effector | String | `end_effector` | `PhysicalProperty` | string, multivalued | |
| Manipulator | String | `manipulator` | `PhysicalProperty` | string | |
| Coordinate Reach X | Decimal | `coordinate_reach` | `PhysicalProperty` | Position, m | Merged with Y and Z into one triple. Description names the CRS Coordinate Reach X, Y and Z. |
| Coordinate Reach Y | Decimal | folded into `coordinate_reach` | | | |
| Coordinate Reach Z | Decimal | folded into `coordinate_reach` | | | |
| Yaw | Decimal | `yaw` | `PhysicalProperty` | Quantity, deg | |
| Pitch | Decimal | `pitch` | `PhysicalProperty` | Quantity, deg | |
| Roll | Decimal | `roll` | `PhysicalProperty` | Quantity, deg | |
| Manipulator Position | String | `manipulator_position` | `PhysicalProperty` | Position | Type changed from prose to a point in the robot's own frame. |
| Degree of Freedom | Int | `degree_of_freedom` | `PhysicalProperty` | integer | |
| Lifting Capacity | Decimal | `lifting_capacity` | `PhysicalProperty` | Quantity, kg | |

**Operational Requirement, 6 attributes**

| CRS attribute | Type | Slot | Class | Range | Note |
|---|---|---|---|---|---|
| Grade | String | `grade` | `OperationalRequirement` | Interval, deg | |
| Temperature | String | `temperature` | `OperationalRequirement` | Interval, Cel | |
| Humidity | Decimal | `humidity` | `OperationalRequirement` | Interval, % | |
| Site Preparation | String | `site_preparation` | `OperationalRequirement` | string | |
| Req Number Operators | Int | `req_number_operators` | `OperationalRequirement` | integer | |
| Operator Responsibilities | String | `operator_responsibilities` | `OperationalRequirement` | string | |

**Safety, 6 attributes**

| CRS attribute | Type | Slot | Class | Range | Note |
|---|---|---|---|---|---|
| Emergency Stop | String | `emergency_stop` | `Safety` | boolean | Type changed: has one or not. |
| Safe Distance | Decimal | `safe_distance` | `Safety` | Quantity, m | |
| Object Detection Range | Decimal | `object_detection_range` | `Safety` | Quantity, m | |
| Safety Barrier | Bool | `safety_barrier` | `Safety` | boolean | |
| Additional PPE Requirements | String | `additional_ppe_requirements` | `Safety` | string, multivalued | |
| Minimum Workspace | Decimal | `minimum_workspace` | `Safety` | Quantity, m | |

**Activity, 15 attributes**

| CRS attribute | Type | Slot | Class | Range | Note |
|---|---|---|---|---|---|
| Task Type | String | `offers` | `Activity` | CapabilityType, multivalued, required | Renamed. Description says it is the CRS Task Type. |
| Productivity | Decimal | `productivity` | `Activity` | Quantity | Merged with Productivity Units. Unit varies, for example brick/d. |
| Precision | Decimal | `precision` | `Activity` | Quantity, mm | Merged with Precision Units. |
| Accuracy | Decimal | `accuracy` | `Activity` | Quantity, mm | Merged with Accuracy Units. |
| Productivity Units | String | folded into `productivity` | | | |
| Precision Units | String | folded into `precision` | | | |
| Accuracy Units | String | folded into `accuracy` | | | |
| Activity Type | String | dropped | | | Process owns it as compound tasks. |
| Material | String | dropped | | | Process owns it as method applicability. |
| Data Output Type | String | `data_output_type` | `Activity` | string, multivalued | |
| Data Output File Type | String | `data_output_file_type` | `Activity` | string, multivalued | |
| Crew Information | String | `crew_information` | `Activity` | string | |
| Crew Responsibilities | String | `crew_responsibilities` | `Activity` | string | |
| Worker Type | Enum | `worker_type` | `Activity` | string, multivalued | Open. |
| Worker Responsibilities | String | `worker_responsibilities` | `Activity` | string | |

### Required

| Slot | Why |
|---|---|
| `Resource.id`, so on `RobotUnit` and `Stock` | Every machine id and every stock unit id is derived from it. |
| `Resource.count`, at least one | Without it the component cannot create a machine node or a stock unit. |
| `Stock.permanence` | Without it the export cannot say whether a unit comes back or is consumed; a default would mislabel one of the two. |
| `RobotUnit.activity_group`, and `Activity.offers` with at least one | Without a capability the entry can never be matched to a task. |
| `id` on any group or sensor object that is present | It projects to a node, and a node needs an identifier. |
| Every `Position`'s three coordinates and unit | A point without all three coordinates or a unit means nothing. Enforced by common. |

Everything else is optional. An entry with `id`, `count`, and an `Activity` holding `id` and `offers` is valid.

### One robot, as a document

```yaml
- id: mason_m1
  count: 2
  activity_group:
    id: mason_m1_activity
    offers: [grip, align, lift]
    productivity: {value: 250, unit: brick/h}
  physical_property_group:
    id: mason_m1_physical
    manufacturer: Fictional Robotics
    length: {value: 3.0, unit: m}
    load_capacity: {value: 15, unit: kg}
    sensors:
      - id: mason_m1_lidar
        sensor_type: LiDAR
        sensor_location: {x_coord: 0, y_coord: 0.2, z_coord: 0.5, unit: m}
  operational_requirement_group:
    id: mason_m1_operational
    temperature: {minimum: 5, maximum: 40, unit: Cel}
    req_number_operators: 1
  safety_group:
    id: mason_m1_safety
    emergency_stop: true
    safety_barrier: true
```

Example robots are fictional. The second entry in the example file is a single mobile inspection robot offering only `locomote`, with one mounted camera, so a `count` of one appears beside the count of two.

### The stocks, as a document

`stocks.yaml`, validated with `-C Stock`:

```yaml
- id: formwork_panels
  count: 2
  permanence: temporary
- id: rebar
  count: 20
  permanence: permanent
```

### Fixed by the brief and the one-pager

Five classes plus `Sensor`; `Resource` and `Stock` added 2026-09-22 by `SPEC-stock.md`. `RobotType` retired. `count` expands into machine nodes with suffixed ids, the one named-slot rule, and since 2026-09-22 into stock units the same way. `status` is the only runtime slot. `offers` is a flat set matched by containment. Group ids are authored. No `label`. The five CRS enum attributes stay open. `Activity Type` and `Material` are dropped.

## Code Style

The module follows `SPEC-toolchain.md` and `SPEC-common.md`. The base, the entry class, the stock, and the two own slots, as they will appear:

```yaml
classes:
  Resource:
    description: >-
      Something a method draws on, counted in identical units: a robot product
      or a stock.
    slots:
      - id
      - count

  RobotUnit:
    is_a: Resource
    description: >-
      One robot product, entered from its Construction Robot Schema attributes.
      Identical machines are one entry with a count.
    slots:
      - status
      - physical_property_group
      - operational_requirement_group
      - safety_group
      - activity_group
    slot_usage:
      id:
        description: The robot's name, a readable product slug. The CRS Name.
      activity_group:
        required: true

  Stock:
    is_a: Resource
    description: >-
      A stock a method uses one unit of, such as formwork panels or rebar.
    slots:
      - permanence
    slot_usage:
      id:
        pattern: "^[A-Za-z][A-Za-z0-9_]*$"
        description: The stock's name, an HDDL name.
      permanence:
        required: true
        description: >-
          Whether a unit a method takes comes back when the method ends, or is
          consumed.

slots:
  count:
    range: integer
    minimum_value: 1
    required: true
    description: >-
      How many identical units this entry stands for: machines of a robot
      product, or units of a stock.
  status:
    range: RobotStatus
    ifabsent: RobotStatus(idle)
    description: The runtime state of one machine.
```

Conventions specific to this module:

- **Names follow the linter's `standard_naming` rule**: CamelCase classes and enums, snake_case slots and permissible values. Attribute slots are the paper's names in snake_case, verbatim.
- **Attribution only where the name changed.** `id`, `offers`, the three merged quantities, and the merged reach say which CRS attribute they come from. Nothing else mentions the paper.
- **One `is_a` base, nothing else from the inheritance features.** `Resource` declares `id` and `count` once for `RobotUnit` and `Stock`, since 2026-09-22; the other classes are concrete and list global slots, with `slot_usage` for per-class `required`. No `abstract`, `mixins`, `union_of`, or `designates_type`.
- **Every object-valued slot states `inlined: true`.** Mandatory on the group slots and `sensors`, whose ranges have identifiers; stated on the Quantity and position slots too, for a uniform read.
- **Group ids follow the entry id**: `mason_m1_physical`, `mason_m1_operational`, `mason_m1_safety`, `mason_m1_activity`, and sensors `mason_m1_<sensor>`.

## Testing Strategy

No new test files. Five rows in `EXAMPLES`, seven since 2026-09-22.

| Document | Class | Expected | Proves |
|---|---|---|---|
| `examples/resource/robot_units.yaml` | `RobotUnit` | validates | Both entries, all six classes, a mounted sensor on each |
| `examples/resource/stocks.yaml` | `Stock` | validates | A temporary and a permanent stock, `id` and `count` inherited from `Resource` |
| `invalid/stock_missing_permanence.yaml` | `Stock` | fails on `permanence` | The one slot `Stock` adds is required |
| `invalid/robot_unit_missing_activity.yaml` | `RobotUnit` | fails on `activity` | The one required group |
| `invalid/robot_unit_zero_count.yaml` | `RobotUnit` | fails on `count` | `minimum_value` reaches the validator |
| `invalid/robot_unit_group_missing_id.yaml` | `RobotUnit` | fails on `id` | A present group needs its node identifier |
| `invalid/activity_missing_offers.yaml` | `RobotUnit` | fails on `offers` | An entry always offers something |

All four error messages were probed on 2026-09-12 and contain the slot name the harness looks for. `test_lint.py` and `test_dist.py` collect the new files with no change. The common change is covered by common's existing rows and the drift test.

What the validator does not check, and who does: that every id in `offers` names a capability in the vocabulary is a tier 2 check for the projection component, checked in the examples by `tests/test_references.py` since 2026-09-21. That every `uses` id on a process method names a stock in `stocks.yaml` is checked the same way from 2026-09-22, by a row in that test (`SPEC-stock.md`).

## Boundaries

**Always.** Every class, slot, enum, and permissible value has a description. `inlined: true` on every object-valued slot. Example robots are fictional. Rebuild `dist/` and `docs/model/` in the same commit as the YAML. `uv run pytest` passes before committing. Conventional Commits. LF.

**Ask first.** Adding a class or slot beyond the lineage table. Closing any of the five open-string attributes with a value set. A second runtime slot beyond `status`. Moving another slot into common. Changing how sensors pair with their positions. Adding a test file. Making `sensors` or any multivalued slot required.

**Never.** A `RobotType` or any type class over entries. A `label` slot. `abstract`, `mixins`, `union_of`, or `designates_type`. Graph vocabulary or annotations. Hand edits under `dist/` or `docs/model/`. Redefining a slot common declares. Position or any per-machine state beyond `status`. Invented value sets for the paper's enum attributes. Real robot products in the examples.

## Success Criteria

1. `uv run pytest` passes with five new rows collected and passing, and no test file other than `test_examples.py` changed; two more rows from 2026-09-22.
2. `dist/resource.schema.json` declares draft 2020-12, passes the meta-schema check, and its `$defs` contain exactly `RobotUnit`, `PhysicalProperty`, `Sensor`, `OperationalRequirement`, `Safety`, `Activity`, `RobotStatus`, and common's `Position`, `Quantity`, `Interval`, `CapabilityType`, `MaterialCategory` since 2026-09-21 (`ParameterKind` until it moved to process, 2026-09-18), and since 2026-09-22 `Resource`, `Stock`, and common's `ComponentPermanence`, fifteen entries. `RobotUnit.properties.count` has `minimum: 1`, and `RobotUnit.properties` and `RobotUnit.required` are the same set before and after `is_a: Resource`; `Stock.required` is `count`, `id`, `permanence`; `sensors` is an array of `Sensor`; `offers` is an array of strings.
3. `dist/README.md` lists `resource.schema.json` with the module description.
4. `docs/model/resource/index.md` lists exactly the six classes, and since 2026-09-22 `Resource` with `RobotUnit` and `Stock` indented under it, `RobotStatus`, and this module's own slots, every entry with a description. The folder also holds unlinked pages for common's elements and a `common.md` schema page: `gen-doc --no-mergeimports` drops the built-in types but still writes pages for a project import. Accepted as is; stripping them would be a toolchain change.
5. `examples/resource/robot_units.yaml` holds two fictional entries. Both carry a sensor with a `sensor_location`; one has `count: 2` and all four groups, the other `count: 1`. Every id in `offers` appears in `examples/common/capability_types.yaml`. Since 2026-09-22, `examples/resource/stocks.yaml` holds `formwork_panels`, `count: 2`, `temporary`, and `rebar`, `count: 20`, `permanent`.
6. The lineage table has exactly 56 attribute rows, and every slot declared in `schema/resource.yaml` appears in it or in the group-slot list. Checked by reading, recorded as done once.
7. `schema/common.yaml` changed only by the four dimension slots, by `unit` on `Position` and its widened description (`SPEC-common.md` decisions 12 and 13), by the `Interval` value type, and on 2026-09-22 by `ComponentPermanence` and `permanence` arriving from product (`SPEC-common.md` decision 18), and the toolchain did not change. `git log -- scripts tests/test_build.py tests/test_lint.py tests/test_dist.py` shows no commit from this module.

## Decisions Made Here (for review)

All decided 2026-09-12 in Phase 1.

1. **Attribute names are the paper's, snake_cased, verbatim**, including `req_number_operators`. Lineage stays trivial.
2. **The five Enum attributes are open strings.** The paper publishes no values. Closing one later is additive.
3. **Grade, Temperature, and Humidity are `Interval`s**, common's lower-and-upper-bound value type with a unit. The paper defines each as a range.
4. **Sensor Location is one `Position` on a `Sensor` object, in the robot's own frame.** Revised 2026-09-14 in the Task 3 review. The paper's definition allows a sensor on the robot or outside it; this module describes the robot, so `sensor_location` is where a sensor sits on the robot body, and sensors standing on site are not modelled here. The 2026-09-12 version split the attribute into a site position and a mount position; the site half is withdrawn. `Sensor` stays a class because a robot carries several, each with its own attributes.
5. **`Sensor` is an identified class, not a keyed map.** A keyed map would flatten three sensors into some twenty prefixed properties, the wide-node shape the one-pager rejected.
6. **Mount offsets are common's `Position`; `MountPosition` is withdrawn.** Revised 2026-09-14 in the Task 3 review. The 2026-09-12 decision was a second value class, `MountPosition`, because common's `Position` had no unit and the brief declines a frame slot. That put a robot-frame point in the model under a different name, which is the brief's rule sidestepped rather than kept. The paper's `String` type for these two attributes was considered and overruled: a position is not a string. Resolution: `Position` gains `unit` in common (`SPEC-common.md` decision 12), so a point carries its unit wherever it is written, and `sensor_location` and `manipulator_position` are plain `Position` whose descriptions state the robot's own frame. One point class, no second frame class, and the brief's one-frame rule stands as written: it forbids a frame slot, not a unit.
7. **Emergency Stop is boolean.** Has one or not; the trigger condition is not planning input.
8. **Coordinate Reach X, Y, Z are one `Position`, `coordinate_reach`.** Revised 2026-09-14 in the Task 3 review: the 2026-09-12 version was three Quantities, because no object existed for them without the frame problem of decision 6. With `unit` on `Position` that problem is gone, and common's `Position` is described as a point or an extent along each axis (`SPEC-common.md` decision 13). Three extents with one unit are one value.
9. **`length`, `width`, `height`, `weight` are declared in common.** Product cannot see a slot resource declares, and the brief's Capacity check compares component weight against load capacity.
10. **Multivalued strings: `end_effector`, `data_output_type`, `data_output_file_type`, `additional_ppe_requirements`, `worker_type`.** The sensor attributes became single-valued on `Sensor`. Prose attributes stay single sentences.
11. **`status` default is written by the projection component**, since `ifabsent` reaches neither the validator nor the JSON Schema. Documents may omit `status`.
12. **Decided 2026-09-14: `RobotUnit`'s group-pointer slot for `Activity` is named `activity_group`, not `activity`.** A same-named slot and class produce the same generated doc filename (`Activity.md`/`activity.md`) on a case-insensitive filesystem — one silently overwrites the other on Windows, which passed locally but failed `test_committed_outputs_match_fresh_build` on Linux CI. Fixed by suffixing the slot, not the class: the class name is the paper's own CRS category name (section 3.6, "CRS has four categories... Safety, and Activity") and isn't ours to rename; the group-pointer slot is local plumbing with no CRS equivalent. `Safety`'s group-pointer slot will hit the same collision when Task 4 adds it — flag it then and name it `safety_group` to match.
13. **Sensor Capability is dropped; `sensor_type` covers it.** Decided 2026-09-14 in the Task 3 review. The paper's two examples, "computer vision sensors, passive lasers, and motion sensors" for the type and "LiDAR emits laser pulses and measures the time it takes them to bounce back" for the capability, state the same fact, what the sensor is, at two lengths. One string slot holds it.
14. **`Resource` is the base of `RobotUnit` and `Stock`, with `id` and `count`; `Stock` adds `permanence`.** Decided 2026-09-21 in Phase 1 of the `Stock` extension, `SPEC-stock.md` decisions 1, 3, 4, and 6, from the formwork runs in `docs/research/pddl-for-process.md` Appendix C; recorded 2026-09-22. A planner can sequence two walls on one formwork set and run them side by side on two only if the stock is an object with a count, so a stock is a resource the way a robot is: `count` moves from `RobotUnit` to the base and means the same on both, units the projection mints as `<id>_<n>`. It is not a parameter kind and never bound: panels are interchangeable, there is no optimal panel as there is an optimal robot, so the export mints the variable and the plan never says which unit a component got. `Stock` carries one slot of its own, `permanence`, product's distinction reused from common: a temporary unit comes back when the method ends, a permanent one is consumed. `status` stays on `RobotUnit`; robots keep their treatment, machine allocation being orchestration's question, not a count the planner consumes. `Resource` is never written as a record and carries no `record_type`, since no file holds both classes and each validates with `-C` on its own. The one `is_a` in the module, admitted as process admitted `Task` and `TaskInstance`: the two shared slots declared once, and one label over everything a method draws on.

## Open Questions

None. The gen-doc question was answered by probe on 2026-09-12 and is recorded in success criterion 4.
