---
search:
  boost: 5.0
---

# Slot: parameters 


_The declared parameters, keyed by name._



<div data-search-exclude markdown="1">



URI: [rcpc:parameters](https://rcpc.for5672/schema/parameters)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Task](Task.md) | HDDL's task: a name and typed parameters, before it is said whether the task ... |  yes  |
| [Method](Method.md) | One way to decompose a compound task into an ordered network of subtasks, for... |  yes  |
| [PrimitiveTask](PrimitiveTask.md) | HDDL's action: a task a robot performs directly, with what performing it requ... |  no  |
| [CompoundTask](CompoundTask.md) | HDDL's abstract task: a task performed only by decomposing it through a metho... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Parameter](Parameter.md) |
| Domain Of | [Task](Task.md), [Method](Method.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Multivalued | Yes |










## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/process




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:parameters |
| native | rcpc:parameters |




## LinkML Source

<details>
```yaml
name: parameters
description: The declared parameters, keyed by name.
from_schema: https://rcpc.for5672/schema/process
rank: 1000
domain_of:
- Task
- Method
range: Parameter
multivalued: true
inlined: true

```
</details></div>