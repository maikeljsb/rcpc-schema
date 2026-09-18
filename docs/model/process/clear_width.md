---
search:
  boost: 5.0
---

# Slot: clear_width 


_The passable width: a door's IFC OverallWidth, a void's opening width, a stair's flight width. Empty when not read._



<div data-search-exclude markdown="1">



URI: [rcpc:clear_width](https://rcpc.for5672/schema/clear_width)
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
| self | rcpc:clear_width |
| native | rcpc:clear_width |




## LinkML Source

<details>
```yaml
name: clear_width
description: 'The passable width: a door''s IFC OverallWidth, a void''s opening width,
  a stair''s flight width. Empty when not read.'
from_schema: https://rcpc.for5672/schema/product
domain_of:
- Connector
range: Quantity
inlined: true

```
</details></div>