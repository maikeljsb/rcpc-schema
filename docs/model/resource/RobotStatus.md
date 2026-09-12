---
search:
  boost: 2.0
---


# Enum: RobotStatus 




_The runtime state of one machine._



<div data-search-exclude markdown="1">

URI: [rcpc:RobotStatus](https://rcpc.for5672/schema/RobotStatus)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| idle | None | Not currently assigned to any task |
| deployed | None | Actively performing a task |
| charging | None | Recharging and unavailable for assignment |
| out_of_service | None | Unavailable for assignment due to maintenance or failure |




## Slots

| Name | Description |
| ---  | --- |
| [status](status.md) | The runtime state of one machine |










## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/resource






## LinkML Source

<details>
```yaml
name: RobotStatus
description: The runtime state of one machine.
from_schema: https://rcpc.for5672/schema/resource
rank: 1000
permissible_values:
  idle:
    text: idle
    description: Not currently assigned to any task.
  deployed:
    text: deployed
    description: Actively performing a task.
  charging:
    text: charging
    description: Recharging and unavailable for assignment.
  out_of_service:
    text: out_of_service
    description: Unavailable for assignment due to maintenance or failure.

```
</details>

</div>