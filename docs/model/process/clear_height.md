---
search:
  boost: 5.0
---

# Slot: clear_height 


_The passable height: a door's IFC OverallHeight, a void's opening height, a stair's headroom. Empty when not read._



<div data-search-exclude markdown="1">



URI: [rcpc:clear_height](https://rcpc.for5672/schema/clear_height)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Connector](Connector.md) | A door, an unfilled opening, or a stair as one node: the component a task ins... |  yes  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Quantity](Quantity.md) |
| Domain Of | [Connector](Connector.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/product




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:clear_height |
| native | rcpc:clear_height |




## LinkML Source

<details>
```yaml
name: clear_height
description: 'The passable height: a door''s IFC OverallHeight, a void''s opening
  height, a stair''s headroom. Empty when not read.'
from_schema: https://rcpc.for5672/schema/product
domain_of:
- Connector
range: Quantity
inlined: true

```
</details></div>