---
search:
  boost: 5.0
---

# Slot: decomposed_by 


_The method chosen to decompose a compound task instance. Empty until chosen._



<div data-search-exclude markdown="1">



URI: [rcpc:decomposed_by](https://rcpc.for5672/schema/decomposed_by)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [CompoundTaskInstance](CompoundTaskInstance.md) | One planned occurrence of a compound task: the task, the method chosen to dec... |  yes  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Method](Method.md) |
| Domain Of | [CompoundTaskInstance](CompoundTaskInstance.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
### Value Constraints

| Property | Value |
| --- | --- |
| Regex Pattern | `^$|^[A-Za-z][A-Za-z0-9_]*$` |












## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/process




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:decomposed_by |
| native | rcpc:decomposed_by |




## LinkML Source

<details>
```yaml
name: decomposed_by
description: The method chosen to decompose a compound task instance. Empty until
  chosen.
from_schema: https://rcpc.for5672/schema/process
rank: 1000
domain_of:
- CompoundTaskInstance
range: Method
pattern: ^$|^[A-Za-z][A-Za-z0-9_]*$

```
</details></div>