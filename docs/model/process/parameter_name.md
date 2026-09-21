---
search:
  boost: 5.0
---

# Slot: parameter_name 


_The parameter's name, a plain word such as c, r, or from._



<div data-search-exclude markdown="1">



URI: [rcpc:parameter_name](https://rcpc.for5672/schema/parameter_name)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Parameter](Parameter.md) | One declared parameter of a task or a method: the kind of object it ranges ov... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Domain Of | [Parameter](Parameter.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Required | Yes |
### Slot Characteristics

| Property | Value |
| --- | --- |
| Key | Yes |












## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/process




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:parameter_name |
| native | rcpc:parameter_name |




## LinkML Source

<details>
```yaml
name: parameter_name
description: The parameter's name, a plain word such as c, r, or from.
from_schema: https://rcpc.for5672/schema/process
rank: 1000
key: true
domain_of:
- Parameter
range: string
required: true

```
</details></div>