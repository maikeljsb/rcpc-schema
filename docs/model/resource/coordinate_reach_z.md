---
search:
  boost: 5.0
---

# Slot: coordinate_reach_z 


_How far the manipulator reaches along the robot's z-axis, recommended in metres._



<div data-search-exclude markdown="1">



URI: [rcpc:coordinate_reach_z](https://rcpc.for5672/schema/coordinate_reach_z)
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
| self | rcpc:coordinate_reach_z |
| native | rcpc:coordinate_reach_z |




## LinkML Source

<details>
```yaml
name: coordinate_reach_z
description: How far the manipulator reaches along the robot's z-axis, recommended
  in metres.
from_schema: https://rcpc.for5672/schema/resource
rank: 1000
domain_of:
- PhysicalProperty
range: Quantity
inlined: true

```
</details></div>