---
search:
  boost: 5.0
---

# Slot: duration 


_How long one performance of the primitive task takes, recommended in seconds._



<div data-search-exclude markdown="1">



URI: [rcpc:duration](https://rcpc.for5672/schema/duration)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [PrimitiveTask](PrimitiveTask.md) | HDDL's action: a task a robot performs directly, with what performing it requ... |  yes  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Quantity](Quantity.md) |
| Domain Of | [PrimitiveTask](PrimitiveTask.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/process




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:duration |
| native | rcpc:duration |




## LinkML Source

<details>
```yaml
name: duration
description: How long one performance of the primitive task takes, recommended in
  seconds.
from_schema: https://rcpc.for5672/schema/process
rank: 1000
domain_of:
- PrimitiveTask
range: Quantity
inlined: true

```
</details></div>