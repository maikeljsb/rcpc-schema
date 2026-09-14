---
search:
  boost: 5.0
---

# Slot: operational_requirement 


_The Operational Requirement group holding the site conditions and people the robot needs._



<div data-search-exclude markdown="1">



URI: [rcpc:operational_requirement](https://rcpc.for5672/schema/operational_requirement)
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
| self | rcpc:operational_requirement |
| native | rcpc:operational_requirement |




## LinkML Source

<details>
```yaml
name: operational_requirement
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