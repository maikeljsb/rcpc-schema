---
search:
  boost: 5.0
---

# Slot: id 


_Unique identifier within the document set._



<div data-search-exclude markdown="1">



URI: [rcpc:id](https://rcpc.for5672/schema/id)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [CapabilityType](CapabilityType.md) | A named capability that a PrimitiveTask requires and a RobotType offers |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Domain Of | [CapabilityType](CapabilityType.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Required | Yes |
### Slot Characteristics

| Property | Value |
| --- | --- |
| Identifier | Yes |












## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/common




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:id |
| native | rcpc:id |




## LinkML Source

<details>
```yaml
name: id
description: Unique identifier within the document set.
from_schema: https://rcpc.for5672/schema/common
rank: 1000
identifier: true
domain_of:
- CapabilityType
range: string
required: true

```
</details></div>