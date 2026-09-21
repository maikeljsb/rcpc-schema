---
search:
  boost: 5.0
---

# Slot: applies_to 


_The material category of the components a method decomposes its task for; a component matches when the Material it is made_of has that category. Absent when the method applies to any component._



<div data-search-exclude markdown="1">



URI: [rcpc:applies_to](https://rcpc.for5672/schema/applies_to)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Method](Method.md) | One way to decompose a compound task into an ordered network of subtasks, for... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [MaterialCategory](MaterialCategory.md) |
| Domain Of | [Method](Method.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/process




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:applies_to |
| native | rcpc:applies_to |




## LinkML Source

<details>
```yaml
name: applies_to
description: The material category of the components a method decomposes its task
  for; a component matches when the Material it is made_of has that category. Absent
  when the method applies to any component.
from_schema: https://rcpc.for5672/schema/process
rank: 1000
domain_of:
- Method
range: MaterialCategory

```
</details></div>