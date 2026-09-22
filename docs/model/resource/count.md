---
search:
  boost: 5.0
---

# Slot: count 


_How many identical units this entry stands for: machines of a robot product, or units of a stock._



<div data-search-exclude markdown="1">



URI: [rcpc:count](https://rcpc.for5672/schema/count)
<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ResourceEntry](ResourceEntry.md) | Something a method draws on, counted in identical units: a robot product or a... |  no  |
| [RobotUnit](RobotUnit.md) | One robot product, entered from its Construction Robot Schema attributes |  no  |
| [Stock](Stock.md) | A stock a method uses one unit of, such as formwork panels or rebar |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) |
| Domain Of | [ResourceEntry](ResourceEntry.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Required | Yes |
### Value Constraints

| Property | Value |
| --- | --- |
| Minimum Value | 1 |












## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/resource




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:count |
| native | rcpc:count |




## LinkML Source

<details>
```yaml
name: count
description: 'How many identical units this entry stands for: machines of a robot
  product, or units of a stock.'
from_schema: https://rcpc.for5672/schema/resource
rank: 1000
domain_of:
- ResourceEntry
range: integer
required: true
minimum_value: 1

```
</details></div>