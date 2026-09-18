---
search:
  boost: 5.0
---

# Slot: navigation 


_Whether the robot can find its own position and plan a path to a destination._



<div data-search-exclude markdown="1">



URI: [rcpc:navigation](https://rcpc.for5672/schema/navigation)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [PhysicalProperty](PhysicalProperty.md) | CRS group 1: the robot's physical dimensions, hardware, and performance |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) |
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
| self | rcpc:navigation |
| native | rcpc:navigation |




## LinkML Source

<details>
```yaml
name: navigation
description: Whether the robot can find its own position and plan a path to a destination.
from_schema: https://rcpc.for5672/schema/resource
domain_of:
- PhysicalProperty
range: boolean

```
</details></div>