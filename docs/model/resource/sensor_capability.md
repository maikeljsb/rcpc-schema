---
search:
  boost: 5.0
---

# Slot: sensor_capability 


_What the sensor senses or measures._



<div data-search-exclude markdown="1">



URI: [rcpc:sensor_capability](https://rcpc.for5672/schema/sensor_capability)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Sensor](Sensor.md) | One sensor on or around the robot |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
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
| self | rcpc:sensor_capability |
| native | rcpc:sensor_capability |




## LinkML Source

<details>
```yaml
name: sensor_capability
description: What the sensor senses or measures.
from_schema: https://rcpc.for5672/schema/resource
rank: 1000
domain_of:
- Sensor
range: string

```
</details></div>