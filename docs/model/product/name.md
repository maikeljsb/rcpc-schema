---
search:
  boost: 5.0
---

# Slot: name 


_The IFC Name. Empty when the IFC file has none._



<div data-search-exclude markdown="1">



URI: [rcpc:name](https://rcpc.for5672/schema/name)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Storey](Storey.md) | A building storey |  no  |
| [Space](Space.md) | A room, or the exterior region of one storey |  no  |
| [BuildingComponent](BuildingComponent.md) | One thing a task acts on |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Domain Of | [Storey](Storey.md), [Space](Space.md), [BuildingComponent](BuildingComponent.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Required | Yes |










## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/product




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:name |
| native | rcpc:name |




## LinkML Source

<details>
```yaml
name: name
description: The IFC Name. Empty when the IFC file has none.
from_schema: https://rcpc.for5672/schema/product
rank: 1000
domain_of:
- Storey
- Space
- BuildingComponent
range: string
required: true

```
</details></div>