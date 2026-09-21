---
search:
  boost: 5.0
---

# Slot: bindings 


_The instance's parameters bound to object ids, keyed by parameter name._



<div data-search-exclude markdown="1">



URI: [rcpc:bindings](https://rcpc.for5672/schema/bindings)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [TaskInstance](TaskInstance.md) | One planned occurrence of a task, before it is said whether the task is primi... |  yes  |
| [CompoundTaskInstance](CompoundTaskInstance.md) | One planned occurrence of a compound task: the task, the method chosen to dec... |  no  |
| [PrimitiveTaskInstance](PrimitiveTaskInstance.md) | One planned occurrence of a primitive task: the action and every parameter of... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [ParameterBinding](ParameterBinding.md) |
| Domain Of | [TaskInstance](TaskInstance.md) |

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
| self | rcpc:bindings |
| native | rcpc:bindings |




## LinkML Source

<details>
```yaml
name: bindings
description: The instance's parameters bound to object ids, keyed by parameter name.
from_schema: https://rcpc.for5672/schema/process
rank: 1000
domain_of:
- TaskInstance
range: ParameterBinding
multivalued: true
inlined: true

```
</details></div>