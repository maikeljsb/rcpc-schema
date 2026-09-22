---
search:
  boost: 5.0
---

# Slot: uses 


_The stocks a method holds one unit of each for its whole span. Absent when the method uses no stock._



<div data-search-exclude markdown="1">



URI: [rcpc:uses](https://rcpc.for5672/schema/uses)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Method](Method.md) | One way to decompose a compound task into an ordered network of subtasks, for... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Stock](Stock.md) |
| Domain Of | [Method](Method.md) |

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
| self | rcpc:uses |
| native | rcpc:uses |




## LinkML Source

<details>
```yaml
name: uses
description: The stocks a method holds one unit of each for its whole span. Absent
  when the method uses no stock.
from_schema: https://rcpc.for5672/schema/process
rank: 1000
domain_of:
- Method
range: Stock
multivalued: true

```
</details></div>