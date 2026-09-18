---
search:
  boost: 5.0
---

# Slot: long_name 


_The IFC LongName of a Space or Storey. Empty when the IFC file has none._



<div data-search-exclude markdown="1">



URI: [rcpc:long_name](https://rcpc.for5672/schema/long_name)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Storey](Storey.md) | A building storey |  no  |
| [Space](Space.md) | A room, or the exterior region of one storey |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Domain Of | [Storey](Storey.md), [Space](Space.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Required | Yes |










## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/product




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:long_name |
| native | rcpc:long_name |




## LinkML Source

<details>
```yaml
name: long_name
description: The IFC LongName of a Space or Storey. Empty when the IFC file has none.
from_schema: https://rcpc.for5672/schema/product
domain_of:
- Storey
- Space
range: string
required: true

```
</details></div>