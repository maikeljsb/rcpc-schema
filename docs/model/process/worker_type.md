---
search:
  boost: 5.0
---

# Slot: worker_type 


_The kinds of worker who work with the robot._



<div data-search-exclude markdown="1">



URI: [rcpc:worker_type](https://rcpc.for5672/schema/worker_type)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Activity](Activity.md) | CRS group 4: the capabilities a robot offers and how it performs them |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Domain Of | [Activity](Activity.md) |

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
| self | rcpc:worker_type |
| native | rcpc:worker_type |




## LinkML Source

<details>
```yaml
name: worker_type
description: The kinds of worker who work with the robot.
from_schema: https://rcpc.for5672/schema/resource
domain_of:
- Activity
range: string
multivalued: true

```
</details></div>