---
search:
  boost: 5.0
---

# Slot: located_in 


_The Space the component's point lies in. Empty for walls and slabs._



<div data-search-exclude markdown="1">



URI: [rcpc:located_in](https://rcpc.for5672/schema/located_in)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [BuildingComponent](BuildingComponent.md) | One thing a task acts on |  yes  |
| [Connector](Connector.md) | A door, an unfilled opening, or a stair as one node: the component a task ins... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Space](Space.md) |
| Domain Of | [BuildingComponent](BuildingComponent.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/product




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:located_in |
| native | rcpc:located_in |




## LinkML Source

<details>
```yaml
name: located_in
description: The Space the component's point lies in. Empty for walls and slabs.
from_schema: https://rcpc.for5672/schema/product
domain_of:
- BuildingComponent
range: Space

```
</details></div>