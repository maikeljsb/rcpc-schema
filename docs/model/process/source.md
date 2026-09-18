---
search:
  boost: 5.0
---

# Slot: source 


_Where a component or Space came from: parsed from the IFC model, or produced by the derivation._



<div data-search-exclude markdown="1">



URI: [rcpc:source](https://rcpc.for5672/schema/source)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Space](Space.md) | A room, or the exterior region of one storey |  yes  |
| [BuildingComponent](BuildingComponent.md) | One thing a task acts on |  yes  |
| [Connector](Connector.md) | A door, an unfilled opening, or a stair as one node: the component a task ins... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [RecordSource](RecordSource.md) |
| Domain Of | [Space](Space.md), [BuildingComponent](BuildingComponent.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/product




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:source |
| native | rcpc:source |




## LinkML Source

<details>
```yaml
name: source
description: 'Where a component or Space came from: parsed from the IFC model, or
  produced by the derivation.'
from_schema: https://rcpc.for5672/schema/product
domain_of:
- Space
- BuildingComponent
range: RecordSource

```
</details></div>