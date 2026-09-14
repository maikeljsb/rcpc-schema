---
search:
  boost: 5.0
---

# Slot: temperature 


_The range of temperatures at which the robot works properly, recommended in degrees Celsius._



<div data-search-exclude markdown="1">



URI: [rcpc:temperature](https://rcpc.for5672/schema/temperature)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [OperationalRequirement](OperationalRequirement.md) | CRS group 2: the site conditions and the people the robot needs to work |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Interval](Interval.md) |
| Domain Of | [OperationalRequirement](OperationalRequirement.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/resource




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:temperature |
| native | rcpc:temperature |




## LinkML Source

<details>
```yaml
name: temperature
description: The range of temperatures at which the robot works properly, recommended
  in degrees Celsius.
from_schema: https://rcpc.for5672/schema/resource
rank: 1000
domain_of:
- OperationalRequirement
range: Interval
inlined: true

```
</details></div>