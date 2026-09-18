---
search:
  boost: 5.0
---

# Slot: part_of 


_The assembly this component is a part of, IFC's aggregation from the part's side. Empty on a component that is not part of an assembly._



<div data-search-exclude markdown="1">



URI: [rcpc:part_of](https://rcpc.for5672/schema/part_of)
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
| self | rcpc:part_of |
| native | rcpc:part_of |




## LinkML Source

<details>
```yaml
name: part_of
description: The assembly this component is a part of, IFC's aggregation from the
  part's side. Empty on a component that is not part of an assembly.
from_schema: https://rcpc.for5672/schema/product
domain_of:
- BuildingComponent
range: BuildingComponent

```
</details></div>