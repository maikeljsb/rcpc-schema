---
search:
  boost: 5.0
---

# Slot: site_preparation 


_What the site needs before the robot can work properly on it._



<div data-search-exclude markdown="1">



URI: [rcpc:site_preparation](https://rcpc.for5672/schema/site_preparation)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [OperationalRequirement](OperationalRequirement.md) | CRS group 2: the site conditions and the people the robot needs to work |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
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
| self | rcpc:site_preparation |
| native | rcpc:site_preparation |




## LinkML Source

<details>
```yaml
name: site_preparation
description: What the site needs before the robot can work properly on it.
from_schema: https://rcpc.for5672/schema/resource
rank: 1000
domain_of:
- OperationalRequirement
range: string

```
</details></div>