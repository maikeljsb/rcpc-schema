---
search:
  boost: 5.0
---

# Slot: made_of 


_The Material the component is made of, IFC's IfcRelAssociatesMaterial from the element's side. Empty when the parser derived no material string._



<div data-search-exclude markdown="1">



URI: [rcpc:made_of](https://rcpc.for5672/schema/made_of)
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
| Range | [Material](Material.md) |
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
| self | rcpc:made_of |
| native | rcpc:made_of |




## LinkML Source

<details>
```yaml
name: made_of
description: The Material the component is made of, IFC's IfcRelAssociatesMaterial
  from the element's side. Empty when the parser derived no material string.
from_schema: https://rcpc.for5672/schema/product
rank: 1000
domain_of:
- BuildingComponent
range: Material

```
</details></div>