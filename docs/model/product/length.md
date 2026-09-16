---
search:
  boost: 5.0
---

# Slot: length 


_How long the item is, recommended in metres._



<div data-search-exclude markdown="1">



URI: [rcpc:length](https://rcpc.for5672/schema/length)
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
| self | rcpc:length |
| native | rcpc:length |




## LinkML Source

<details>
```yaml
name: length
description: How long the item is, recommended in metres.
from_schema: https://rcpc.for5672/schema/common
domain_of:
- BuildingComponent
range: Quantity
inlined: true

```
</details></div>