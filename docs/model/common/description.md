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
| [MaterialCategory](MaterialCategory.md) | A category of material a construction method is written for, IFC's IfcMateria... |  yes  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Domain Of | [CapabilityType](CapabilityType.md), [MaterialCategory](MaterialCategory.md) |

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
rank: 1000
domain_of:
- CapabilityType
- MaterialCategory
range: string

```
</details></div>