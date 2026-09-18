---
search:
  boost: 5.0
---

# Slot: humidity 


_The range of relative humidity at which the robot works properly, recommended in percent._



<div data-search-exclude markdown="1">



URI: [rcpc:humidity](https://rcpc.for5672/schema/humidity)
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
| self | rcpc:humidity |
| native | rcpc:humidity |




## LinkML Source

<details>
```yaml
name: humidity
description: The range of relative humidity at which the robot works properly, recommended
  in percent.
from_schema: https://rcpc.for5672/schema/resource
domain_of:
- OperationalRequirement
range: Interval
inlined: true

```
</details></div>