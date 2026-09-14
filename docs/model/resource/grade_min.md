---
search:
  boost: 5.0
---

# Slot: grade_min 


_The gentlest ground slope the robot can work on, recommended in degrees. The lower bound of the CRS Grade._



<div data-search-exclude markdown="1">



URI: [rcpc:grade_min](https://rcpc.for5672/schema/grade_min)
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
| self | rcpc:grade_min |
| native | rcpc:grade_min |




## LinkML Source

<details>
```yaml
name: grade_min
description: The gentlest ground slope the robot can work on, recommended in degrees.
  The lower bound of the CRS Grade.
from_schema: https://rcpc.for5672/schema/resource
rank: 1000
domain_of:
- OperationalRequirement
range: Quantity
inlined: true

```
</details></div>