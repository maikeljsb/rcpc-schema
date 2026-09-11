---
search:
  boost: 10.0
---

# Class: Quantity 


_A number with a unit._



<div data-search-exclude markdown="1">



URI: [rcpc:Quantity](https://rcpc.for5672/schema/Quantity)





```mermaid
 classDiagram
    class Quantity
    click Quantity href "../Quantity/"
      Quantity : unit
        
          
    
        
        
        Quantity --> "1" String : unit
        click String href "../http://www.w3.org/2001/XMLSchema#string/"
    

        
      Quantity : value
        
          
    
        
        
        Quantity --> "1" Float : value
        click Float href "../http://www.w3.org/2001/XMLSchema#float/"
    

        
      
```




<!-- no inheritance hierarchy -->

## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [value](value.md) | 1 <br/> [xsd:float](http://www.w3.org/2001/XMLSchema#float) | The numeric value | direct |
| [unit](unit.md) | 1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) | The unit of the value | direct |















## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/common




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:Quantity |
| native | rcpc:Quantity |






## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Quantity
description: A number with a unit.
from_schema: https://rcpc.for5672/schema/common
slots:
- value
- unit
slot_usage:
  value:
    name: value
    required: true
  unit:
    name: unit
    required: true

```
</details>

### Induced

<details>
```yaml
name: Quantity
description: A number with a unit.
from_schema: https://rcpc.for5672/schema/common
slot_usage:
  value:
    name: value
    required: true
  unit:
    name: unit
    required: true
attributes:
  value:
    name: value
    description: The numeric value.
    from_schema: https://rcpc.for5672/schema/common
    rank: 1000
    owner: Quantity
    domain_of:
    - Quantity
    range: float
    required: true
  unit:
    name: unit
    description: The unit of the value. UCUM case-sensitive codes are recommended.
    from_schema: https://rcpc.for5672/schema/common
    rank: 1000
    owner: Quantity
    domain_of:
    - Quantity
    range: string
    required: true

```
</details></div>