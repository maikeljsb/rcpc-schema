# product

Building components as planning targets. BuildingComponent identified by its IFC GlobalId, with lifetime and provenance; Connector for what a robot passes through; Space and Storey as the topology they sit in.

URI: https://rcpc.for5672/schema/product

Name: product



## Classes

| Class | Description |
| --- | --- |
| [Space](Space.md) | A room, or the exterior region of one storey |
| [Storey](Storey.md) | A building storey |



## Slots

| Slot | Description |
| --- | --- |
| [contained_in](contained_in.md) | IFC's containment relation under its own name |
| [elevation](elevation.md) | The storey's level in the project frame |
| [long_name](long_name.md) | The IFC LongName of a Space or Storey |
| [name](name.md) | The IFC Name |
| [source](source.md) | Where a component or Space came from: parsed from the IFC model, or produced ... |


## Enumerations

| Enumeration | Description |
| --- | --- |
| [RecordSource](RecordSource.md) | Where a component or Space came from: parsed from the IFC model, or produced ... |


## Types

| Type | Description |
| --- | --- |


## Subsets

| Subset | Description |
| --- | --- |
