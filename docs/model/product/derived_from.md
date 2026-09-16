---
search:
  boost: 5.0
---

# Slot: derived_from 


_The IFC-sourced component this one was generated from. Empty except on a derived record._



<div data-search-exclude markdown="1">



URI: [rcpc:derived_from](https://rcpc.for5672/schema/derived_from)
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
| Range | [BuildingComponent](BuildingComponent.md) |
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
| self | rcpc:derived_from |
| native | rcpc:derived_from |




## LinkML Source

<details>
```yaml
name: derived_from
description: The IFC-sourced component this one was generated from. Empty except on
  a derived record.
from_schema: https://rcpc.for5672/schema/product
rank: 1000
domain_of:
- BuildingComponent
range: BuildingComponent

```
</details></div>