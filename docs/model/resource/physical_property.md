---
search:
  boost: 5.0
---

# Slot: physical_property 


_The Physical Property group holding the robot's dimensions, hardware, and performance._



<div data-search-exclude markdown="1">



URI: [rcpc:physical_property](https://rcpc.for5672/schema/physical_property)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [RobotUnit](RobotUnit.md) | One robot product, entered from its Construction Robot Schema attributes |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [PhysicalProperty](PhysicalProperty.md) |
| Domain Of | [RobotUnit](RobotUnit.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/resource




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:physical_property |
| native | rcpc:physical_property |




## LinkML Source

<details>
```yaml
name: physical_property
description: The Physical Property group holding the robot's dimensions, hardware,
  and performance.
from_schema: https://rcpc.for5672/schema/resource
rank: 1000
domain_of:
- RobotUnit
range: PhysicalProperty
inlined: true

```
</details></div>