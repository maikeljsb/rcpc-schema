---
search:
  boost: 5.0
---

# Slot: id 


_Identifier, unique among instances of its class._



<div data-search-exclude markdown="1">



URI: [rcpc:id](https://rcpc.for5672/schema/id)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [CapabilityType](CapabilityType.md) | Something a robot can do, named by a verb |  no  |
| [Storey](Storey.md) | A building storey |  yes  |
| [Space](Space.md) | A room, or the exterior region of one storey |  yes  |
| [BuildingComponent](BuildingComponent.md) | One thing a task acts on |  yes  |
| [RobotUnit](RobotUnit.md) | One robot product, entered from its Construction Robot Schema attributes |  yes  |
| [PhysicalProperty](PhysicalProperty.md) | CRS group 1: the robot's physical dimensions, hardware, and performance |  no  |
| [Sensor](Sensor.md) | One sensor on or around the robot |  no  |
| [OperationalRequirement](OperationalRequirement.md) | CRS group 2: the site conditions and the people the robot needs to work |  no  |
| [Safety](Safety.md) | CRS group 3: how the robot protects the people and objects around it |  no  |
| [Activity](Activity.md) | CRS group 4: the capabilities a robot offers and how it performs them |  no  |
| [Task](Task.md) | HDDL's task: a name and typed parameters, before it is said whether the task ... |  yes  |
| [Method](Method.md) | One way to decompose a compound task into an ordered network of subtasks |  yes  |
| [Connector](Connector.md) | A door, an unfilled opening, or a stair as one node: the component a task ins... |  no  |
| [PrimitiveTask](PrimitiveTask.md) | HDDL's action: a task a robot performs directly, with what performing it requ... |  no  |
| [CompoundTask](CompoundTask.md) | HDDL's abstract task: a task performed only by decomposing it through a metho... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Domain Of | [CapabilityType](CapabilityType.md), [Storey](Storey.md), [Space](Space.md), [BuildingComponent](BuildingComponent.md), [RobotUnit](RobotUnit.md), [PhysicalProperty](PhysicalProperty.md), [Sensor](Sensor.md), [OperationalRequirement](OperationalRequirement.md), [Safety](Safety.md), [Activity](Activity.md), [Task](Task.md), [Method](Method.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Required | Yes |
### Slot Characteristics

| Property | Value |
| --- | --- |
| Identifier | Yes |












## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/common




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:id |
| native | rcpc:id |




## LinkML Source

<details>
```yaml
name: id
description: Identifier, unique among instances of its class.
from_schema: https://rcpc.for5672/schema/common
identifier: true
domain_of:
- CapabilityType
- Storey
- Space
- BuildingComponent
- RobotUnit
- PhysicalProperty
- Sensor
- OperationalRequirement
- Safety
- Activity
- Task
- Method
range: string
required: true

```
</details></div>