---
search:
  boost: 5.0
---

# Slot: load_capacity 


_The maximum weight the robot can carry for extended work, recommended in kilograms._



<div data-search-exclude markdown="1">



URI: [rcpc:load_capacity](https://rcpc.for5672/schema/load_capacity)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [PhysicalProperty](PhysicalProperty.md) | CRS group 1: the robot's physical dimensions, hardware, and performance |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Quantity](Quantity.md) |
| Domain Of | [PhysicalProperty](PhysicalProperty.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/resource




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:load_capacity |
| native | rcpc:load_capacity |




## LinkML Source

<details>
```yaml
name: load_capacity
description: The maximum weight the robot can carry for extended work, recommended
  in kilograms.
from_schema: https://rcpc.for5672/schema/resource
rank: 1000
domain_of:
- PhysicalProperty
range: Quantity
inlined: true

```
</details></div>