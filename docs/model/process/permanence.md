---
search:
  boost: 5.0
---

# Slot: permanence 


_Whether the component stays in the building._



<div data-search-exclude markdown="1">



URI: [rcpc:permanence](https://rcpc.for5672/schema/permanence)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [BuildingComponent](BuildingComponent.md) | One thing a task acts on |  yes  |
| [Stock](Stock.md) | A stock a method uses one unit of, such as formwork panels or rebar |  yes  |
| [Connector](Connector.md) | A door, an unfilled opening, or a stair as one node: the component a task ins... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [ComponentPermanence](ComponentPermanence.md) |
| Domain Of | [BuildingComponent](BuildingComponent.md), [Stock](Stock.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/common




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:permanence |
| native | rcpc:permanence |




## LinkML Source

<details>
```yaml
name: permanence
description: Whether the component stays in the building.
from_schema: https://rcpc.for5672/schema/common
domain_of:
- BuildingComponent
- Stock
range: ComponentPermanence

```
</details></div>