---
search:
  boost: 5.0
---

# Slot: applies_to 


_The materials a method applies to, as IFC spells them; a component matches when its material is in the list. Set on a method's component parameter only._



<div data-search-exclude markdown="1">



URI: [rcpc:applies_to](https://rcpc.for5672/schema/applies_to)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Parameter](Parameter.md) | One declared parameter of a task or a method: the kind of object it ranges ov... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [MaterialName](MaterialName.md) |
| Domain Of | [Parameter](Parameter.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Multivalued | Yes |










## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/process




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:applies_to |
| native | rcpc:applies_to |




## LinkML Source

<details>
```yaml
name: applies_to
description: The materials a method applies to, as IFC spells them; a component matches
  when its material is in the list. Set on a method's component parameter only.
from_schema: https://rcpc.for5672/schema/process
rank: 1000
domain_of:
- Parameter
range: MaterialName
multivalued: true

```
</details></div>