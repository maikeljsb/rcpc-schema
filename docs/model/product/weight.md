---
search:
  boost: 5.0
---

# Slot: weight 


_How much the item weighs, recommended in kilograms._



<div data-search-exclude markdown="1">



URI: [rcpc:weight](https://rcpc.for5672/schema/weight)
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
| Range | [Quantity](Quantity.md) |
| Domain Of | [BuildingComponent](BuildingComponent.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/common




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:weight |
| native | rcpc:weight |




## LinkML Source

<details>
```yaml
name: weight
description: How much the item weighs, recommended in kilograms.
from_schema: https://rcpc.for5672/schema/common
domain_of:
- BuildingComponent
range: Quantity
inlined: true

```
</details></div>