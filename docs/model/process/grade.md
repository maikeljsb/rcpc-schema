---
search:
  boost: 5.0
---

# Slot: grade 


_The range of ground slopes the robot can work on, recommended in degrees._



<div data-search-exclude markdown="1">



URI: [rcpc:grade](https://rcpc.for5672/schema/grade)
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
| self | rcpc:grade |
| native | rcpc:grade |




## LinkML Source

<details>
```yaml
name: grade
description: The range of ground slopes the robot can work on, recommended in degrees.
from_schema: https://rcpc.for5672/schema/resource
domain_of:
- OperationalRequirement
range: Interval
inlined: true

```
</details></div>