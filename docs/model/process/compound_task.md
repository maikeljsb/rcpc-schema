---
search:
  boost: 5.0
---

# Slot: compound_task 


_The compound task a method decomposes, a subtask names, or an instance realises._



<div data-search-exclude markdown="1">



URI: [rcpc:compound_task](https://rcpc.for5672/schema/compound_task)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Method](Method.md) | One way to decompose a compound task into an ordered network of subtasks |  yes  |
| [Subtask](Subtask.md) | One entry of a method's subtask list: the task it names and the arguments it ... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [CompoundTask](CompoundTask.md) |
| Domain Of | [Method](Method.md), [Subtask](Subtask.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/process




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:compound_task |
| native | rcpc:compound_task |




## LinkML Source

<details>
```yaml
name: compound_task
description: The compound task a method decomposes, a subtask names, or an instance
  realises.
from_schema: https://rcpc.for5672/schema/process
rank: 1000
domain_of:
- Method
- Subtask
range: CompoundTask

```
</details></div>