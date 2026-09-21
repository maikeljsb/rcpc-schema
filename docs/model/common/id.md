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
| [MaterialCategory](MaterialCategory.md) | A category of material a construction method is written for, IFC's IfcMateria... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Domain Of | [CapabilityType](CapabilityType.md), [MaterialCategory](MaterialCategory.md) |

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
rank: 1000
identifier: true
domain_of:
- CapabilityType
- MaterialCategory
range: string
required: true

```
</details></div>