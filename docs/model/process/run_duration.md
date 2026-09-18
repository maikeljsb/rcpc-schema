---
search:
  boost: 5.0
---

# Slot: run_duration 


_How long the robot can run continuously on its power source, recommended in minutes._



<div data-search-exclude markdown="1">



URI: [rcpc:run_duration](https://rcpc.for5672/schema/run_duration)
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
| self | rcpc:run_duration |
| native | rcpc:run_duration |




## LinkML Source

<details>
```yaml
name: run_duration
description: How long the robot can run continuously on its power source, recommended
  in minutes.
from_schema: https://rcpc.for5672/schema/resource
domain_of:
- PhysicalProperty
range: Quantity
inlined: true

```
</details></div>