---
search:
  boost: 5.0
---

# Slot: end_effector 


_The tools the robot's manipulator can attach, such as a bucket or gripper._



<div data-search-exclude markdown="1">



URI: [rcpc:end_effector](https://rcpc.for5672/schema/end_effector)
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
| Multivalued | Yes |










## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/resource




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:end_effector |
| native | rcpc:end_effector |




## LinkML Source

<details>
```yaml
name: end_effector
description: The tools the robot's manipulator can attach, such as a bucket or gripper.
from_schema: https://rcpc.for5672/schema/resource
domain_of:
- PhysicalProperty
range: string
multivalued: true

```
</details></div>