---
search:
  boost: 5.0
---

# Slot: unit 


_The unit of the value, or of the coordinates._



<div data-search-exclude markdown="1">



URI: [rcpc:unit](https://rcpc.for5672/schema/unit)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Position](Position.md) | Three cartesian coordinates and their unit: a point, or an extent along each ... |  yes  |
| [Quantity](Quantity.md) | A number with a unit |  yes  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Domain Of | [Position](Position.md), [Quantity](Quantity.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/common




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:unit |
| native | rcpc:unit |




## LinkML Source

<details>
```yaml
name: unit
description: The unit of the value, or of the coordinates.
from_schema: https://rcpc.for5672/schema/common
rank: 1000
domain_of:
- Position
- Quantity
range: string

```
</details></div>