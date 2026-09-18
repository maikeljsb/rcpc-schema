---
search:
  boost: 2.0
---


# Enum: ParameterKind 




_The kinds of object a parameter ranges over._



<div data-search-exclude markdown="1">

URI: [rcpc:ParameterKind](https://rcpc.for5672/schema/ParameterKind)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| component | None | A BuildingComponent, or one of its subclasses |
| location | None | A Space |
| robot | None | One machine of a RobotUnit entry |




## Slots

| Name | Description |
| ---  | --- |
| [parameter_kind](parameter_kind.md) | The kind of object the parameter ranges over |










## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/process






## LinkML Source

<details>
```yaml
name: ParameterKind
description: The kinds of object a parameter ranges over.
from_schema: https://rcpc.for5672/schema/process
rank: 1000
permissible_values:
  component:
    text: component
    description: A BuildingComponent, or one of its subclasses.
  location:
    text: location
    description: A Space.
  robot:
    text: robot
    description: One machine of a RobotUnit entry.

```
</details>

</div>