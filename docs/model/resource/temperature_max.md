---
search:
  boost: 5.0
---

# Slot: temperature_max 


_The highest temperature at which the robot works properly, recommended in degrees Celsius. The upper bound of the CRS Temperature._



<div data-search-exclude markdown="1">



URI: [rcpc:temperature_max](https://rcpc.for5672/schema/temperature_max)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [OperationalRequirement](OperationalRequirement.md) | CRS group 2: the site conditions and the people the robot needs to work |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Quantity](Quantity.md) |
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
| self | rcpc:temperature_max |
| native | rcpc:temperature_max |




## LinkML Source

<details>
```yaml
name: temperature_max
description: The highest temperature at which the robot works properly, recommended
  in degrees Celsius. The upper bound of the CRS Temperature.
from_schema: https://rcpc.for5672/schema/resource
rank: 1000
domain_of:
- OperationalRequirement
range: Quantity
inlined: true

```
</details></div>