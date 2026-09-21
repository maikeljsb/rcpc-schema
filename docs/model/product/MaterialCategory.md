---
search:
  boost: 2.0
---


# Enum: MaterialCategory 




_The categories of material a construction method is written for, IFC's IfcMaterial.Category as this project's vocabulary._



<div data-search-exclude markdown="1">

URI: [rcpc:MaterialCategory](https://rcpc.for5672/schema/MaterialCategory)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| masonry | None | Brick, block, and stone, laid or prefabricated as a unit |
| timber | None | Wood, solid or engineered, including joisted floors and roofs |
| concrete | None | Cast or precast concrete, including slabs and foundation walls |
| unassigned | None | No category yet; the parser writes it and a mapping step replaces it |




## Slots

| Name | Description |
| ---  | --- |
| [category](category.md) | The Material's category, IFC's IfcMaterial |










## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/common






## LinkML Source

<details>
```yaml
name: MaterialCategory
description: The categories of material a construction method is written for, IFC's
  IfcMaterial.Category as this project's vocabulary.
from_schema: https://rcpc.for5672/schema/common
permissible_values:
  masonry:
    text: masonry
    description: Brick, block, and stone, laid or prefabricated as a unit.
  timber:
    text: timber
    description: Wood, solid or engineered, including joisted floors and roofs.
  concrete:
    text: concrete
    description: Cast or precast concrete, including slabs and foundation walls.
  unassigned:
    text: unassigned
    description: No category yet; the parser writes it and a mapping step replaces
      it.

```
</details>

</div>