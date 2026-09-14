---
search:
  boost: 5.0
---

# Slot: manipulator_position 


_Where the manipulator is mounted on the robot, in the robot's own frame._



<div data-search-exclude markdown="1">



URI: [rcpc:manipulator_position](https://rcpc.for5672/schema/manipulator_position)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [PhysicalProperty](PhysicalProperty.md) | CRS group 1: the robot's physical dimensions, hardware, and performance |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [MountPosition](MountPosition.md) |
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
| self | rcpc:manipulator_position |
| native | rcpc:manipulator_position |




## LinkML Source

<details>
```yaml
name: manipulator_position
description: Where the manipulator is mounted on the robot, in the robot's own frame.
from_schema: https://rcpc.for5672/schema/resource
rank: 1000
domain_of:
- PhysicalProperty
range: MountPosition
inlined: true

```
</details></div>