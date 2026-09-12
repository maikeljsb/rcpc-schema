---
search:
  boost: 2.0
---


# Enum: ParameterKind 




_The kinds of value a task parameter can hold._



<div data-search-exclude markdown="1">

URI: [rcpc:ParameterKind](https://rcpc.for5672/schema/ParameterKind)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| position | None | A Position |
| component_reference | None | A reference to a BuildingComponent, by id |
| quantity | None | A Quantity |













## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/common






## LinkML Source

<details>
```yaml
name: ParameterKind
description: The kinds of value a task parameter can hold.
from_schema: https://rcpc.for5672/schema/common
permissible_values:
  position:
    text: position
    description: A Position.
  component_reference:
    text: component_reference
    description: A reference to a BuildingComponent, by id.
  quantity:
    text: quantity
    description: A Quantity.

```
</details>

</div>