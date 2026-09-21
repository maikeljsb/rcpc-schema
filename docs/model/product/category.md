---
search:
  boost: 5.0
---

# Slot: category 


_The Material's category, IFC's IfcMaterial.Category as this project's vocabulary, assigned by a mapping step after the parse. Empty until mapped._



<div data-search-exclude markdown="1">



URI: [rcpc:category](https://rcpc.for5672/schema/category)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Material](Material.md) | A material as IFC's IfcMaterial: one record per distinct material string the ... |  yes  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [MaterialCategory](MaterialCategory.md) |
| Domain Of | [Material](Material.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/product




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:category |
| native | rcpc:category |




## LinkML Source

<details>
```yaml
name: category
description: The Material's category, IFC's IfcMaterial.Category as this project's
  vocabulary, assigned by a mapping step after the parse. Empty until mapped.
from_schema: https://rcpc.for5672/schema/product
rank: 1000
domain_of:
- Material
range: MaterialCategory

```
</details></div>