---
search:
  boost: 5.0
---

# Slot: requires 


_The capabilities a robot must offer to perform the primitive task._



<div data-search-exclude markdown="1">



URI: [rcpc:requires](https://rcpc.for5672/schema/requires)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [PrimitiveTask](PrimitiveTask.md) | HDDL's action: a task a robot performs directly, with what performing it requ... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [CapabilityType](CapabilityType.md) |
| Domain Of | [PrimitiveTask](PrimitiveTask.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Required | Yes |
| Multivalued | Yes |
| Minimum Cardinality | 1 |










## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/process




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:requires |
| native | rcpc:requires |




## LinkML Source

<details>
```yaml
name: requires
description: The capabilities a robot must offer to perform the primitive task.
from_schema: https://rcpc.for5672/schema/process
rank: 1000
domain_of:
- PrimitiveTask
range: CapabilityType
required: true
multivalued: true
minimum_cardinality: 1

```
</details></div>