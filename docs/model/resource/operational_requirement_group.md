---
search:
  boost: 5.0
---

# Slot: operational_requirement_group 


_The Operational Requirement group holding the site conditions and people the robot needs._



<div data-search-exclude markdown="1">



URI: [rcpc:operational_requirement_group](https://rcpc.for5672/schema/operational_requirement_group)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [RobotUnit](RobotUnit.md) | One robot product, entered from its Construction Robot Schema attributes |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [OperationalRequirement](OperationalRequirement.md) |
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
| self | rcpc:operational_requirement_group |
| native | rcpc:operational_requirement_group |




## LinkML Source

<details>
```yaml
name: operational_requirement_group
description: The Operational Requirement group holding the site conditions and people
  the robot needs.
from_schema: https://rcpc.for5672/schema/resource
rank: 1000
domain_of:
- RobotUnit
range: OperationalRequirement
inlined: true

```
</details></div>