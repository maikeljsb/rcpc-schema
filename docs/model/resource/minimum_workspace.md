---
search:
  boost: 5.0
---

# Slot: minimum_workspace 


_The minimum space the robot needs to operate without collisions, recommended in metres._



<div data-search-exclude markdown="1">



URI: [rcpc:minimum_workspace](https://rcpc.for5672/schema/minimum_workspace)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Safety](Safety.md) | CRS group 3: how the robot protects the people and objects around it |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Quantity](Quantity.md) |
| Domain Of | [Safety](Safety.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/resource




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:minimum_workspace |
| native | rcpc:minimum_workspace |




## LinkML Source

<details>
```yaml
name: minimum_workspace
description: The minimum space the robot needs to operate without collisions, recommended
  in metres.
from_schema: https://rcpc.for5672/schema/resource
rank: 1000
domain_of:
- Safety
range: Quantity
inlined: true

```
</details></div>