# common

Shared vocabulary for the Product Process Graph: value types, the material name type, and the capability types. Imported by every other module.

URI: https://rcpc.for5672/schema/common

Name: common



## Classes

| Class | Description |
| --- | --- |
| [CapabilityType](CapabilityType.md) | Something a robot can do, named by a verb |
| [Interval](Interval.md) | A lower and an upper bound with their unit |
| [Position](Position.md) | Three cartesian coordinates and their unit: a point, or an extent along each ... |
| [Quantity](Quantity.md) | A number with a unit |



## Slots

| Slot | Description |
| --- | --- |
| [description](description.md) | What this is, in one or two plain sentences |
| [height](height.md) | How tall the item is, recommended in metres |
| [id](id.md) | Identifier, unique among instances of its class |
| [length](length.md) | How long the item is, recommended in metres |
| [maximum](maximum.md) | The upper bound |
| [minimum](minimum.md) | The lower bound |
| [unit](unit.md) | The unit of the value, of the coordinates, or of the bounds |
| [value](value.md) | The numeric value |
| [weight](weight.md) | How much the item weighs, recommended in kilograms |
| [width](width.md) | How wide the item is, recommended in metres |
| [x_coord](x_coord.md) | Cartesian x coordinate |
| [y_coord](y_coord.md) | Cartesian y coordinate |
| [z_coord](z_coord.md) | Cartesian z coordinate |


## Enumerations

| Enumeration | Description |
| --- | --- |


## Types

| Type | Description |
| --- | --- |
| [MaterialName](MaterialName.md) | An IFC material name, exactly as it appears in the model |


## Subsets

| Subset | Description |
| --- | --- |
