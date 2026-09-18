---
search:
  boost: 5.0
---

# Slot: status 


_The runtime state of one machine._



<div data-search-exclude markdown="1">



URI: [rcpc:status](https://rcpc.for5672/schema/status)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [RobotUnit](RobotUnit.md) | One robot product, entered from its Construction Robot Schema attributes |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [RobotStatus](RobotStatus.md) |
| Domain Of | [RobotUnit](RobotUnit.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
### Slot Characteristics

| Property | Value |
| --- | --- |
| If Absent | `RobotStatus(idle)` |












## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/resource




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:status |
| native | rcpc:status |




## LinkML Source

<details>
```yaml
name: status
description: The runtime state of one machine.
from_schema: https://rcpc.for5672/schema/resource
ifabsent: RobotStatus(idle)
domain_of:
- RobotUnit
range: RobotStatus

```
</details></div>