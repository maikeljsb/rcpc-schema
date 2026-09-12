---
search:
  boost: 5.0
---

# Slot: offers 


_The capability types this robot offers. The CRS Task Type._



<div data-search-exclude markdown="1">



URI: [rcpc:offers](https://rcpc.for5672/schema/offers)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Activity](Activity.md) | CRS group 4: the capabilities a robot offers and how it performs them |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [CapabilityType](CapabilityType.md) |
| Domain Of | [Activity](Activity.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Required | Yes |
| Multivalued | Yes |










## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/resource




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:offers |
| native | rcpc:offers |




## LinkML Source

<details>
```yaml
name: offers
description: The capability types this robot offers. The CRS Task Type.
from_schema: https://rcpc.for5672/schema/resource
rank: 1000
domain_of:
- Activity
range: CapabilityType
required: true
multivalued: true

```
</details></div>