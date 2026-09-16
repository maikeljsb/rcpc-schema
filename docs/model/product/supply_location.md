---
search:
  boost: 5.0
---

# Slot: supply_location 


_Where the component is delivered or staged. Empty when not yet known._



<div data-search-exclude markdown="1">



URI: [rcpc:supply_location](https://rcpc.for5672/schema/supply_location)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [BuildingComponent](BuildingComponent.md) | One thing a task acts on |  yes  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Position](Position.md) |
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
| self | rcpc:supply_location |
| native | rcpc:supply_location |




## LinkML Source

<details>
```yaml
name: supply_location
description: Where the component is delivered or staged. Empty when not yet known.
from_schema: https://rcpc.for5672/schema/product
rank: 1000
domain_of:
- BuildingComponent
range: Position
inlined: true

```
</details></div>