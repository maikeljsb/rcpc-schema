---
search:
  boost: 5.0
---

# Slot: connects 


_The two Spaces the Connector joins. A stair's two Spaces are on different storeys._



<div data-search-exclude markdown="1">



URI: [rcpc:connects](https://rcpc.for5672/schema/connects)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Connector](Connector.md) | A door, an unfilled opening, or a stair as one node: the component a task ins... |  yes  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Space](Space.md) |
| Domain Of | [Connector](Connector.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Multivalued | Yes |
| Minimum Cardinality | 2 |
| Maximum Cardinality | 2 |










## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/product




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:connects |
| native | rcpc:connects |




## LinkML Source

<details>
```yaml
name: connects
description: The two Spaces the Connector joins. A stair's two Spaces are on different
  storeys.
from_schema: https://rcpc.for5672/schema/product
domain_of:
- Connector
range: Space
multivalued: true
minimum_cardinality: 2
maximum_cardinality: 2

```
</details></div>