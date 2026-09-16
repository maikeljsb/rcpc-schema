# product

Building components as planning targets. BuildingComponent identified by its IFC GlobalId, with lifetime and provenance; Connector for what a robot passes through; Space and Storey as the topology they sit in.

URI: https://rcpc.for5672/schema/product

Name: product



## Classes

| Class | Description |
| --- | --- |
| [BuildingComponent](BuildingComponent.md) | One thing a task acts on |
| [Space](Space.md) | A room, or the exterior region of one storey |
| [Storey](Storey.md) | A building storey |



## Slots

| Slot | Description |
| --- | --- |
| [contained_in](contained_in.md) | IFC's containment relation under its own name |
| [current_location](current_location.md) | Where the component is now |
| [derived_from](derived_from.md) | The IFC-sourced component this one was generated from |
| [elevation](elevation.md) | The storey's level in the project frame |
| [ifc_type](ifc_type.md) | The bare IFC entity name, such as IfcWall |
| [located_in](located_in.md) | The Space the component's point lies in |
| [long_name](long_name.md) | The IFC LongName of a Space or Storey |
| [material](material.md) | The one material string the parser derives, as the IFC spells it |
| [name](name.md) | The IFC Name |
| [part_of](part_of.md) | The assembly this component is a part of, IFC's aggregation from the part's s... |
| [permanence](permanence.md) | Whether the component stays in the building |
| [source](source.md) | Where a component or Space came from: parsed from the IFC model, or produced ... |
| [supply_location](supply_location.md) | Where the component is delivered or staged |
| [target_location](target_location.md) | The centroid of the component's body in the IFC project frame, in the project... |


## Enumerations

| Enumeration | Description |
| --- | --- |
| [ComponentPermanence](ComponentPermanence.md) | Whether the component stays in the building |
| [RecordSource](RecordSource.md) | Where a component or Space came from: parsed from the IFC model, or produced ... |


## Types

| Type | Description |
| --- | --- |


## Subsets

| Subset | Description |
| --- | --- |
