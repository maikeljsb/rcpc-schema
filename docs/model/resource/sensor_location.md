---
search:
  boost: 5.0
---

# Slot: sensor_location 


_Where the sensor sits on the robot, a point in the robot's own frame._



<div data-search-exclude markdown="1">



URI: [rcpc:sensor_location](https://rcpc.for5672/schema/sensor_location)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Sensor](Sensor.md) | One sensor on or around the robot |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Position](Position.md) |
| Domain Of | [Sensor](Sensor.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/resource




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:sensor_location |
| native | rcpc:sensor_location |




## LinkML Source

<details>
```yaml
name: sensor_location
description: Where the sensor sits on the robot, a point in the robot's own frame.
from_schema: https://rcpc.for5672/schema/resource
rank: 1000
domain_of:
- Sensor
range: Position
inlined: true

```
</details></div>