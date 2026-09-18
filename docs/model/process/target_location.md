---
search:
  boost: 5.0
---

# Slot: target_location 


_The centroid of the component's body in the IFC project frame, in the project length unit. Where the design puts it and what a placement task binds to._



<div data-search-exclude markdown="1">



URI: [rcpc:target_location](https://rcpc.for5672/schema/target_location)
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
| Range | [Position](Position.md) |
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
| self | rcpc:target_location |
| native | rcpc:target_location |




## LinkML Source

<details>
```yaml
name: target_location
description: The centroid of the component's body in the IFC project frame, in the
  project length unit. Where the design puts it and what a placement task binds to.
from_schema: https://rcpc.for5672/schema/product
domain_of:
- BuildingComponent
range: Position
inlined: true

```
</details></div>