---
search:
  boost: 5.0
---

# Slot: description 


_What this is, in one or two plain sentences._



<div data-search-exclude markdown="1">



URI: [rcpc:description](https://rcpc.for5672/schema/description)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [CapabilityType](CapabilityType.md) | Something a robot can do, named by a verb |  yes  |
| [Task](Task.md) | HDDL's task: a name and typed parameters, before it is said whether the task ... |  yes  |
| [Method](Method.md) | One way to decompose a compound task into an ordered network of subtasks, for... |  yes  |
| [PrimitiveTask](PrimitiveTask.md) | HDDL's action: a task a robot performs directly, with what performing it requ... |  no  |
| [CompoundTask](CompoundTask.md) | HDDL's abstract task: a task performed only by decomposing it through a metho... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Domain Of | [CapabilityType](CapabilityType.md), [Task](Task.md), [Method](Method.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/common




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:description |
| native | rcpc:description |




## LinkML Source

<details>
```yaml
name: description
description: What this is, in one or two plain sentences.
from_schema: https://rcpc.for5672/schema/common
domain_of:
- CapabilityType
- Task
- Method
range: string

```
</details></div>