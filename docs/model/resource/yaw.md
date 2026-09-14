---
search:
  boost: 5.0
---

# Slot: yaw 


_The manipulator's rotation range around the vertical axis, recommended in degrees._



<div data-search-exclude markdown="1">



URI: [rcpc:yaw](https://rcpc.for5672/schema/yaw)
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
| self | rcpc:yaw |
| native | rcpc:yaw |




## LinkML Source

<details>
```yaml
name: yaw
description: The manipulator's rotation range around the vertical axis, recommended
  in degrees.
from_schema: https://rcpc.for5672/schema/resource
rank: 1000
domain_of:
- PhysicalProperty
range: Quantity
inlined: true

```
</details></div>