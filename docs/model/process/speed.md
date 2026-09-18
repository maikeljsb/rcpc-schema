---
search:
  boost: 5.0
---

# Slot: speed 


_How fast the robot travels, recommended in metres per second._



<div data-search-exclude markdown="1">



URI: [rcpc:speed](https://rcpc.for5672/schema/speed)
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


* from schema: https://rcpc.for5672/schema/resource




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:speed |
| native | rcpc:speed |




## LinkML Source

<details>
```yaml
name: speed
description: How fast the robot travels, recommended in metres per second.
from_schema: https://rcpc.for5672/schema/resource
domain_of:
- PhysicalProperty
range: Quantity
inlined: true

```
</details></div>