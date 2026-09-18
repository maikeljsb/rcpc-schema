---
search:
  boost: 5.0
---

# Slot: arguments 


_The values a subtask passes, in the named task's parameter order: method parameter names or object ids._



<div data-search-exclude markdown="1">



URI: [rcpc:arguments](https://rcpc.for5672/schema/arguments)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Subtask](Subtask.md) | One entry of a method's subtask list: the task it names and the arguments it ... |  yes  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Domain Of | [Subtask](Subtask.md) |

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
| self | rcpc:arguments |
| native | rcpc:arguments |




## LinkML Source

<details>
```yaml
name: arguments
description: 'The values a subtask passes, in the named task''s parameter order: method
  parameter names or object ids.'
from_schema: https://rcpc.for5672/schema/process
rank: 1000
domain_of:
- Subtask
range: string
multivalued: true

```
</details></div>