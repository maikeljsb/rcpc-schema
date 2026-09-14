---
search:
  boost: 5.0
---

# Slot: height 


_How tall the item is, recommended in metres._



<div data-search-exclude markdown="1">



URI: [rcpc:height](https://rcpc.for5672/schema/height)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [PhysicalProperty](PhysicalProperty.md) | CRS group 1: the robot's physical dimensions, hardware, and performance |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Quantity](Quantity.md) |
| Domain Of | [PhysicalProperty](PhysicalProperty.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/common




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:height |
| native | rcpc:height |




## LinkML Source

<details>
```yaml
name: height
description: How tall the item is, recommended in metres.
from_schema: https://rcpc.for5672/schema/common
domain_of:
- PhysicalProperty
range: Quantity
inlined: true

```
</details></div>