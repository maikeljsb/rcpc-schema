---
search:
  boost: 2.0
---


# Enum: ComponentPermanence 




_Whether the component stays in the building. Reinforcement is permanent, formwork temporary._



<div data-search-exclude markdown="1">

URI: [rcpc:ComponentPermanence](https://rcpc.for5672/schema/ComponentPermanence)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| permanent | None | The component remains in the finished building |
| temporary | None | The component is removed before the building is finished |




## Slots

| Name | Description |
| ---  | --- |
| [permanence](permanence.md) | Whether the component stays in the building |










## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/common






## LinkML Source

<details>
```yaml
name: ComponentPermanence
description: Whether the component stays in the building. Reinforcement is permanent,
  formwork temporary.
from_schema: https://rcpc.for5672/schema/common
rank: 1000
permissible_values:
  permanent:
    text: permanent
    description: The component remains in the finished building.
  temporary:
    text: temporary
    description: The component is removed before the building is finished.

```
</details>

</div>