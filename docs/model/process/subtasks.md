---
search:
  boost: 5.0
---

# Slot: subtasks 


_The subtasks in list order, counted from 1. On a method, the entries of its decomposition; on a compound task instance, the instances that replaced it._



<div data-search-exclude markdown="1">



URI: [rcpc:subtasks](https://rcpc.for5672/schema/subtasks)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Method](Method.md) | One way to decompose a compound task into an ordered network of subtasks, for... |  yes  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Domain Of | [Method](Method.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Multivalued | Yes |










## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/process




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:subtasks |
| native | rcpc:subtasks |




## LinkML Source

<details>
```yaml
name: subtasks
description: The subtasks in list order, counted from 1. On a method, the entries
  of its decomposition; on a compound task instance, the instances that replaced it.
from_schema: https://rcpc.for5672/schema/process
rank: 1000
domain_of:
- Method
range: string
multivalued: true

```
</details></div>