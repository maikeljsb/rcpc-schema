---
search:
  boost: 5.0
---

# Slot: elevation 


_The storey's level in the project frame. Empty when not resolved._



<div data-search-exclude markdown="1">



URI: [rcpc:elevation](https://rcpc.for5672/schema/elevation)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Storey](Storey.md) | A building storey |  yes  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Quantity](Quantity.md) |
| Domain Of | [Storey](Storey.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/product




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:elevation |
| native | rcpc:elevation |




## LinkML Source

<details>
```yaml
name: elevation
description: The storey's level in the project frame. Empty when not resolved.
from_schema: https://rcpc.for5672/schema/product
domain_of:
- Storey
range: Quantity
inlined: true

```
</details></div>