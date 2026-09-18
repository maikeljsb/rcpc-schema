---
search:
  boost: 2.0
---


# Enum: ConnectorKind 




_What kind of passage a Connector is._



<div data-search-exclude markdown="1">

URI: [rcpc:ConnectorKind](https://rcpc.for5672/schema/ConnectorKind)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| door | None | A door, the filling of a wall opening |
| void | None | A wall opening with no filling |
| stair | None | A stair joining two Spaces on different storeys |




## Slots

| Name | Description |
| ---  | --- |
| [kind](kind.md) | What kind of passage the Connector is |










## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/product






## LinkML Source

<details>
```yaml
name: ConnectorKind
description: What kind of passage a Connector is.
from_schema: https://rcpc.for5672/schema/product
permissible_values:
  door:
    text: door
    description: A door, the filling of a wall opening.
  void:
    text: void
    description: A wall opening with no filling.
  stair:
    text: stair
    description: A stair joining two Spaces on different storeys.

```
</details>

</div>