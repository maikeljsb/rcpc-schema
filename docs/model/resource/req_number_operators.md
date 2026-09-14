---
search:
  boost: 5.0
---

# Slot: req_number_operators 


_How many people control the robot._



<div data-search-exclude markdown="1">



URI: [rcpc:req_number_operators](https://rcpc.for5672/schema/req_number_operators)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [OperationalRequirement](OperationalRequirement.md) | CRS group 2: the site conditions and the people the robot needs to work |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) |
| Domain Of | [OperationalRequirement](OperationalRequirement.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/resource




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:req_number_operators |
| native | rcpc:req_number_operators |




## LinkML Source

<details>
```yaml
name: req_number_operators
description: How many people control the robot.
from_schema: https://rcpc.for5672/schema/resource
rank: 1000
domain_of:
- OperationalRequirement
range: integer

```
</details></div>