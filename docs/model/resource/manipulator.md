---
search:
  boost: 5.0
---

# Slot: manipulator 


_The robot's arm: the links and joints that perform tasks._



<div data-search-exclude markdown="1">



URI: [rcpc:manipulator](https://rcpc.for5672/schema/manipulator)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [PhysicalProperty](PhysicalProperty.md) | CRS group 1: the robot's physical dimensions, hardware, and performance |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Domain Of | [PhysicalProperty](PhysicalProperty.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/resource




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:manipulator |
| native | rcpc:manipulator |




## LinkML Source

<details>
```yaml
name: manipulator
description: 'The robot''s arm: the links and joints that perform tasks.'
from_schema: https://rcpc.for5672/schema/resource
rank: 1000
domain_of:
- PhysicalProperty
range: string

```
</details></div>