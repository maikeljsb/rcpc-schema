---
search:
  boost: 5.0
---

# Slot: accuracy 


_How close the robot's work comes to the target, recommended in millimetres. The CRS Accuracy with its Accuracy Units._



<div data-search-exclude markdown="1">



URI: [rcpc:accuracy](https://rcpc.for5672/schema/accuracy)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Activity](Activity.md) | CRS group 4: the capabilities a robot offers and how it performs them |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Quantity](Quantity.md) |
| Domain Of | [Activity](Activity.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/resource




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:accuracy |
| native | rcpc:accuracy |




## LinkML Source

<details>
```yaml
name: accuracy
description: How close the robot's work comes to the target, recommended in millimetres.
  The CRS Accuracy with its Accuracy Units.
from_schema: https://rcpc.for5672/schema/resource
domain_of:
- Activity
range: Quantity
inlined: true

```
</details></div>