---
search:
  boost: 5.0
---

# Slot: record_type 


_Which class in this schema the record belongs to._



<div data-search-exclude markdown="1">



URI: [rcpc:record_type](https://rcpc.for5672/schema/record_type)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Storey](Storey.md) | A building storey |  no  |
| [Space](Space.md) | A room, or the exterior region of one storey |  no  |
| [BuildingComponent](BuildingComponent.md) | One thing a task acts on |  no  |
| [Connector](Connector.md) | A door, an unfilled opening, or a stair as one node: the component a task ins... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Domain Of | [Storey](Storey.md), [Space](Space.md), [BuildingComponent](BuildingComponent.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Required | Yes |
### Slot Characteristics

| Property | Value |
| --- | --- |
| Designates Type | Yes |












## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/product




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:record_type |
| native | rcpc:record_type |




## LinkML Source

<details>
```yaml
name: record_type
description: Which class in this schema the record belongs to.
from_schema: https://rcpc.for5672/schema/product
rank: 1000
designates_type: true
domain_of:
- Storey
- Space
- BuildingComponent
range: string
required: true

```
</details></div>