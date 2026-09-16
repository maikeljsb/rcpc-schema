---
search:
  boost: 5.0
---

# Slot: ifc_type 


_The bare IFC entity name, such as IfcWall. Empty on a derived record, which has none._



<div data-search-exclude markdown="1">



URI: [rcpc:ifc_type](https://rcpc.for5672/schema/ifc_type)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [BuildingComponent](BuildingComponent.md) | One thing a task acts on |  yes  |
| [Connector](Connector.md) | A door, an unfilled opening, or a stair as one node: the component a task ins... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Domain Of | [BuildingComponent](BuildingComponent.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/product




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:ifc_type |
| native | rcpc:ifc_type |




## LinkML Source

<details>
```yaml
name: ifc_type
description: The bare IFC entity name, such as IfcWall. Empty on a derived record,
  which has none.
from_schema: https://rcpc.for5672/schema/product
rank: 1000
domain_of:
- BuildingComponent
range: string

```
</details></div>