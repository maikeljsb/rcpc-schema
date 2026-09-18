---
search:
  boost: 5.0
---

# Slot: current_location 


_Where the component is now. Written by execution; the model's second runtime slot after status. Empty until execution writes one._



<div data-search-exclude markdown="1">



URI: [rcpc:current_location](https://rcpc.for5672/schema/current_location)
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
| self | rcpc:current_location |
| native | rcpc:current_location |




## LinkML Source

<details>
```yaml
name: current_location
description: Where the component is now. Written by execution; the model's second
  runtime slot after status. Empty until execution writes one.
from_schema: https://rcpc.for5672/schema/product
domain_of:
- BuildingComponent
range: Position
inlined: true

```
</details></div>