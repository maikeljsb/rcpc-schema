---
search:
  boost: 5.0
---

# Slot: material 


_The one material string the parser derives, as the IFC spells it. Empty when unresolved._



<div data-search-exclude markdown="1">



URI: [rcpc:material](https://rcpc.for5672/schema/material)
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
| Range | [MaterialName](MaterialName.md) |
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
| self | rcpc:material |
| native | rcpc:material |




## LinkML Source

<details>
```yaml
name: material
description: The one material string the parser derives, as the IFC spells it. Empty
  when unresolved.
from_schema: https://rcpc.for5672/schema/product
rank: 1000
domain_of:
- BuildingComponent
range: MaterialName

```
</details></div>