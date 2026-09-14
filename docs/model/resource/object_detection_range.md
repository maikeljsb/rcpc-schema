---
search:
  boost: 5.0
---

# Slot: object_detection_range 


_How far away the robot can detect and recognise objects, recommended in metres._



<div data-search-exclude markdown="1">



URI: [rcpc:object_detection_range](https://rcpc.for5672/schema/object_detection_range)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Safety](Safety.md) | CRS group 3: how the robot protects the people and objects around it |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Quantity](Quantity.md) |
| Domain Of | [Safety](Safety.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/resource




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:object_detection_range |
| native | rcpc:object_detection_range |




## LinkML Source

<details>
```yaml
name: object_detection_range
description: How far away the robot can detect and recognise objects, recommended
  in metres.
from_schema: https://rcpc.for5672/schema/resource
rank: 1000
domain_of:
- Safety
range: Quantity
inlined: true

```
</details></div>