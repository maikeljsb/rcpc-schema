---
search:
  boost: 5.0
---

# Slot: tasks 


_The network's tasks in list order, counted from 1, each position its label._



<div data-search-exclude markdown="1">



URI: [rcpc:tasks](https://rcpc.for5672/schema/tasks)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [TaskNetwork](TaskNetwork.md) | HDDL's initial task network: what the plan is asked to accomplish, the compou... |  yes  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [CompoundTaskInstance](CompoundTaskInstance.md) |
| Domain Of | [TaskNetwork](TaskNetwork.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Multivalued | Yes |
| Minimum Cardinality | 1 |










## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/process




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:tasks |
| native | rcpc:tasks |




## LinkML Source

<details>
```yaml
name: tasks
description: The network's tasks in list order, counted from 1, each position its
  label.
from_schema: https://rcpc.for5672/schema/process
rank: 1000
domain_of:
- TaskNetwork
range: CompoundTaskInstance
multivalued: true
minimum_cardinality: 1

```
</details></div>