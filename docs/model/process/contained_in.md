---
search:
  boost: 5.0
---

# Slot: contained_in 


_IFC's containment relation under its own name. On a BuildingComponent, its storey; on a Space, the storey that aggregates it or, for a derived Space, the storey it was cut for. Empty on a part, contained only through its assembly._



<div data-search-exclude markdown="1">



URI: [rcpc:contained_in](https://rcpc.for5672/schema/contained_in)
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
| Range | [Storey](Storey.md) |
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
| self | rcpc:contained_in |
| native | rcpc:contained_in |




## LinkML Source

<details>
```yaml
name: contained_in
description: IFC's containment relation under its own name. On a BuildingComponent,
  its storey; on a Space, the storey that aggregates it or, for a derived Space, the
  storey it was cut for. Empty on a part, contained only through its assembly.
from_schema: https://rcpc.for5672/schema/product
domain_of:
- Space
- BuildingComponent
range: Storey

```
</details></div>