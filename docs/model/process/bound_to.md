---
search:
  boost: 5.0
---

# Slot: bound_to 


_The id of the object the parameter is bound to: a BuildingComponent, a Space, or a machine such as mason_m1_1, as the parameter's declared kind says._



<div data-search-exclude markdown="1">



URI: [rcpc:bound_to](https://rcpc.for5672/schema/bound_to)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ParameterBinding](ParameterBinding.md) | One parameter of a task instance bound to one object |  yes  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Domain Of | [ParameterBinding](ParameterBinding.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/process




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:bound_to |
| native | rcpc:bound_to |




## LinkML Source

<details>
```yaml
name: bound_to
description: 'The id of the object the parameter is bound to: a BuildingComponent,
  a Space, or a machine such as mason_m1_1, as the parameter''s declared kind says.'
from_schema: https://rcpc.for5672/schema/process
rank: 1000
domain_of:
- ParameterBinding
range: string

```
</details></div>