# product

Building components as planning targets. BuildingComponent identified by its IFC GlobalId, with lifetime and provenance; Connector for what a robot passes through; Material for what a component is made of; Space and Storey as the topology they sit in.

URI: https://rcpc.for5672/schema/product

Name: product



## Classes

| Class | Description |
| --- | --- |
| [BuildingComponent](BuildingComponent.md) | One thing a task acts on |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Connector](Connector.md) | A door, an unfilled opening, or a stair as one node: the component a task ins... |
| [Material](Material.md) | A material as IFC's IfcMaterial: one record per distinct material string the ... |
| [Space](Space.md) | A room, or the exterior region of one storey |
| [Storey](Storey.md) | A building storey |



## Slots

| Slot | Description |
| --- | --- |
| [category](category.md) | The Material's category, IFC's IfcMaterial |
| [clear_height](clear_height.md) | The passable height: a door's IFC OverallHeight, a void's opening height, a s... |
| [clear_width](clear_width.md) | The passable width: a door's IFC OverallWidth, a void's opening width, a stai... |
| [connects](connects.md) | The two Spaces the Connector joins |
| [contained_in](contained_in.md) | IFC's containment relation under its own name |
| [current_location](current_location.md) | Where the component is now |
| [derived_from](derived_from.md) | The IFC-sourced component this one was generated from |
| [elevation](elevation.md) | The storey's level in the project frame |
| [ifc_type](ifc_type.md) | The bare IFC entity name, such as IfcWall |
| [kind](kind.md) | What kind of passage the Connector is |
| [located_in](located_in.md) | The Space the component's point lies in |
| [long_name](long_name.md) | The IFC LongName of a Space or Storey |
| [made_of](made_of.md) | The Material the component is made of, IFC's IfcRelAssociatesMaterial from th... |
| [name](name.md) | The IFC Name |
| [part_of](part_of.md) | The assembly this component is a part of, IFC's aggregation from the part's s... |
| [record_type](record_type.md) | Which class in this schema the record belongs to |
| [source](source.md) | Where a component or Space came from: parsed from the IFC model, or produced ... |
| [supply_location](supply_location.md) | Where the component is delivered or staged |
| [target_location](target_location.md) | The centroid of the component's body in the IFC project frame, in the project... |


## Enumerations

| Enumeration | Description |
| --- | --- |
| [ConnectorKind](ConnectorKind.md) | What kind of passage a Connector is |
| [RecordSource](RecordSource.md) | Where a component or Space came from: parsed from the IFC model, or produced ... |


## Types

| Type | Description |
| --- | --- |


## Subsets

| Subset | Description |
| --- | --- |
