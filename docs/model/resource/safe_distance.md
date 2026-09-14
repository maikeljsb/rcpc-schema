---
search:
  boost: 5.0
---

# Slot: safe_distance 


_The minimum distance to keep between humans and the robot while they work together, recommended in metres._



<div data-search-exclude markdown="1">



URI: [rcpc:safe_distance](https://rcpc.for5672/schema/safe_distance)
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
| self | rcpc:safe_distance |
| native | rcpc:safe_distance |




## LinkML Source

<details>
```yaml
name: safe_distance
description: The minimum distance to keep between humans and the robot while they
  work together, recommended in metres.
from_schema: https://rcpc.for5672/schema/resource
rank: 1000
domain_of:
- Safety
range: Quantity
inlined: true

```
</details></div>