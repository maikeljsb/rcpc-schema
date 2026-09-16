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






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Domain Of | [CapabilityType](CapabilityType.md), [Storey](Storey.md), [Space](Space.md), [BuildingComponent](BuildingComponent.md) |

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
range: string
required: true

```
</details></div>