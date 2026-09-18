---
search:
  boost: 5.0
---

# Slot: activity_group 


_The Activity group holding this robot's offered capabilities._



<div data-search-exclude markdown="1">



URI: [rcpc:activity_group](https://rcpc.for5672/schema/activity_group)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [RobotUnit](RobotUnit.md) | One robot product, entered from its Construction Robot Schema attributes |  yes  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Activity](Activity.md) |
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
| self | rcpc:activity_group |
| native | rcpc:activity_group |




## LinkML Source

<details>
```yaml
name: activity_group
description: The Activity group holding this robot's offered capabilities.
from_schema: https://rcpc.for5672/schema/resource
domain_of:
- RobotUnit
range: Activity
inlined: true

```
</details></div>