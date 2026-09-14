---
search:
  boost: 5.0
---

# Slot: emergency_stop 


_Whether the robot stops automatically and immediately when specific conditions are triggered._



<div data-search-exclude markdown="1">



URI: [rcpc:emergency_stop](https://rcpc.for5672/schema/emergency_stop)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Safety](Safety.md) | CRS group 3: how the robot protects the people and objects around it |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) |
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
| self | rcpc:emergency_stop |
| native | rcpc:emergency_stop |




## LinkML Source

<details>
```yaml
name: emergency_stop
description: Whether the robot stops automatically and immediately when specific conditions
  are triggered.
from_schema: https://rcpc.for5672/schema/resource
rank: 1000
domain_of:
- Safety
range: boolean

```
</details></div>