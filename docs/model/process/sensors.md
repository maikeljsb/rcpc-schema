---
search:
  boost: 5.0
---

# Slot: sensors 


_The sensors mounted on or around the robot._



<div data-search-exclude markdown="1">



URI: [rcpc:sensors](https://rcpc.for5672/schema/sensors)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [PhysicalProperty](PhysicalProperty.md) | CRS group 1: the robot's physical dimensions, hardware, and performance |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Sensor](Sensor.md) |
| Domain Of | [PhysicalProperty](PhysicalProperty.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Multivalued | Yes |










## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/resource




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:sensors |
| native | rcpc:sensors |




## LinkML Source

<details>
```yaml
name: sensors
description: The sensors mounted on or around the robot.
from_schema: https://rcpc.for5672/schema/resource
domain_of:
- PhysicalProperty
range: Sensor
multivalued: true
inlined: true
inlined_as_list: true

```
</details></div>