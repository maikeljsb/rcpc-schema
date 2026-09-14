---
search:
  boost: 5.0
---

# Slot: productivity 


_How much work the robot does per unit of time, in a unit that fits the activity, for example brick/h. The CRS Productivity with its Productivity Units._



<div data-search-exclude markdown="1">



URI: [rcpc:productivity](https://rcpc.for5672/schema/productivity)
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
| self | rcpc:productivity |
| native | rcpc:productivity |




## LinkML Source

<details>
```yaml
name: productivity
description: How much work the robot does per unit of time, in a unit that fits the
  activity, for example brick/h. The CRS Productivity with its Productivity Units.
from_schema: https://rcpc.for5672/schema/resource
rank: 1000
domain_of:
- Activity
range: Quantity
inlined: true

```
</details></div>