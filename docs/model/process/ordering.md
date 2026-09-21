---
search:
  boost: 5.0
---

# Slot: ordering 


_Pairs of positions in the owner's subtask or task list; in each pair the first ends before the second starts. Empty when unordered._



<div data-search-exclude markdown="1">



URI: [rcpc:ordering](https://rcpc.for5672/schema/ordering)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Method](Method.md) | One way to decompose a compound task into an ordered network of subtasks, for... |  yes  |
| [TaskNetwork](TaskNetwork.md) | HDDL's initial task network: what the plan is asked to accomplish, the compou... |  yes  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) |
| Domain Of | [Method](Method.md), [TaskNetwork](TaskNetwork.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
<details>
<summary>Advanced Properties</summary>
**Array Configuration:**

- **Dimensions:** DimensionExpression({'alias': 'pair'}) x DimensionExpression({'exact_cardinality': 2})
- **Exact Dimensions Required:** Yes

</details>











## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/process




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:ordering |
| native | rcpc:ordering |




## LinkML Source

<details>
```yaml
name: ordering
description: Pairs of positions in the owner's subtask or task list; in each pair
  the first ends before the second starts. Empty when unordered.
from_schema: https://rcpc.for5672/schema/process
rank: 1000
domain_of:
- Method
- TaskNetwork
range: integer
array:
  exact_number_dimensions: 2
  dimensions:
  - alias: pair
  - exact_cardinality: 2

```
</details></div>