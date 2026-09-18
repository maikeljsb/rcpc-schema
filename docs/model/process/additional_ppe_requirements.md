---
search:
  boost: 5.0
---

# Slot: additional_ppe_requirements 


_Extra personal protective equipment required when humans operate or work with the robot._



<div data-search-exclude markdown="1">



URI: [rcpc:additional_ppe_requirements](https://rcpc.for5672/schema/additional_ppe_requirements)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Safety](Safety.md) | CRS group 3: how the robot protects the people and objects around it |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Domain Of | [Safety](Safety.md) |

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
| self | rcpc:additional_ppe_requirements |
| native | rcpc:additional_ppe_requirements |




## LinkML Source

<details>
```yaml
name: additional_ppe_requirements
description: Extra personal protective equipment required when humans operate or work
  with the robot.
from_schema: https://rcpc.for5672/schema/resource
domain_of:
- Safety
range: string
multivalued: true

```
</details></div>