---
search:
  boost: 5.0
---

# Slot: coordinate_reach 


_How far the manipulator reaches along each of the robot's three axes, recommended in metres. The CRS Coordinate Reach X, Y and Z._



<div data-search-exclude markdown="1">



URI: [rcpc:coordinate_reach](https://rcpc.for5672/schema/coordinate_reach)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [PhysicalProperty](PhysicalProperty.md) | CRS group 1: the robot's physical dimensions, hardware, and performance |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Position](Position.md) |
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
| self | rcpc:coordinate_reach |
| native | rcpc:coordinate_reach |




## LinkML Source

<details>
```yaml
name: coordinate_reach
description: How far the manipulator reaches along each of the robot's three axes,
  recommended in metres. The CRS Coordinate Reach X, Y and Z.
from_schema: https://rcpc.for5672/schema/resource
rank: 1000
domain_of:
- PhysicalProperty
range: Position
inlined: true

```
</details></div>