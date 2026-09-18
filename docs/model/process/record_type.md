---
search:
  boost: 5.0
---

# Slot: record_type 


_Which class in this schema the record belongs to._



<div data-search-exclude markdown="1">



URI: [rcpc:record_type](https://rcpc.for5672/schema/record_type)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Storey](Storey.md) | A building storey |  no  |
| [Space](Space.md) | A room, or the exterior region of one storey |  no  |
| [BuildingComponent](BuildingComponent.md) | One thing a task acts on |  no  |
| [Task](Task.md) | HDDL's task: a name and typed parameters, before it is said whether the task ... |  no  |
| [Method](Method.md) | One way to decompose a compound task into an ordered network of subtasks |  no  |
| [Connector](Connector.md) | A door, an unfilled opening, or a stair as one node: the component a task ins... |  no  |
| [PrimitiveTask](PrimitiveTask.md) | HDDL's action: a task a robot performs directly, with what performing it requ... |  no  |
| [CompoundTask](CompoundTask.md) | HDDL's abstract task: a task performed only by decomposing it through a metho... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Domain Of | [Storey](Storey.md), [Space](Space.md), [BuildingComponent](BuildingComponent.md), [Task](Task.md), [Method](Method.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Required | Yes |
### Slot Characteristics

| Property | Value |
| --- | --- |
| Designates Type | Yes |












## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/product




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:record_type |
| native | rcpc:record_type |




## LinkML Source

<details>
```yaml
name: record_type
description: Which class in this schema the record belongs to.
from_schema: https://rcpc.for5672/schema/product
designates_type: true
domain_of:
- Storey
- Space
- BuildingComponent
- Task
- Method
range: string
required: true

```
</details></div>