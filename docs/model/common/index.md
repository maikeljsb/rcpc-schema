# common

Shared vocabulary for the Product Process Graph: value types, the material name type, the parameter kinds, and the capability types. Imported by every other module.

URI: https://rcpc.for5672/schema/common

Name: common



## Classes

| Class | Description |
| --- | --- |
| [CapabilityType](CapabilityType.md) | Something a robot can do, named by a verb |
| [Position](Position.md) | A point in the IFC project coordinate frame, in metres |
| [Quantity](Quantity.md) | A number with a unit |



## Slots

| Slot | Description |
| --- | --- |
| [description](description.md) | What this is, in one or two plain sentences |
| [id](id.md) | Identifier, unique among instances of its class |
| [unit](unit.md) | The unit of the value |
| [value](value.md) | The numeric value |
| [x_coord](x_coord.md) | Easting, in metres |
| [y_coord](y_coord.md) | Northing, in metres |
| [z_coord](z_coord.md) | Height, in metres |


## Enumerations

| Enumeration | Description |
| --- | --- |
| [ParameterKind](ParameterKind.md) | The kinds of value a task parameter can hold |


## Types

| Type | Description |
| --- | --- |
| [MaterialName](MaterialName.md) | An IFC material name, exactly as it appears in the model |


## Subsets

| Subset | Description |
| --- | --- |
