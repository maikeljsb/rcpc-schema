---
search:
  boost: 2.0
---


# Enum: RecordSource 




_Where a component or Space came from: parsed from the IFC model, or produced by derivation._



<div data-search-exclude markdown="1">

URI: [rcpc:RecordSource](https://rcpc.for5672/schema/RecordSource)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| ifc | None | Parsed directly from the IFC model |
| derived | None | Produced by derivation |




## Slots

| Name | Description |
| ---  | --- |
| [source](source.md) | Where a component or Space came from: parsed from the IFC model, or produced ... |










## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/product






## LinkML Source

<details>
```yaml
name: RecordSource
description: 'Where a component or Space came from: parsed from the IFC model, or
  produced by derivation.'
from_schema: https://rcpc.for5672/schema/product
rank: 1000
permissible_values:
  ifc:
    text: ifc
    description: Parsed directly from the IFC model.
  derived:
    text: derived
    description: Produced by derivation.

```
</details>

</div>