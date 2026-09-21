---
search:
  boost: 10.0
---

# Class: Storey 


_A building storey._



<div data-search-exclude markdown="1">



URI: [rcpc:Storey](https://rcpc.for5672/schema/Storey)





```mermaid
 classDiagram
    class Storey
    click Storey href "../Storey/"
      Storey : elevation
        
          
    
        
        
        Storey --> "1" Quantity : elevation
        click Quantity href "../Quantity/"
    

        
      Storey : id
        
          
    
        
        
        Storey --> "1" String : id
        click String href "../http://www.w3.org/2001/XMLSchema#string/"
    

        
      Storey : long_name
        
          
    
        
        
        Storey --> "1" String : long_name
        click String href "../http://www.w3.org/2001/XMLSchema#string/"
    

        
      Storey : name
        
          
    
        
        
        Storey --> "1" String : name
        click String href "../http://www.w3.org/2001/XMLSchema#string/"
    

        
      Storey : record_type
        
          
    
        
        
        Storey --> "1" String : record_type
        click String href "../http://www.w3.org/2001/XMLSchema#string/"
    

        
      
```




<!-- no inheritance hierarchy -->

## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [record_type](record_type.md) | 1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) | Which class in this schema the record belongs to | direct |
| [id](id.md) | 1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) | The IFC GlobalId in its 22-character form: the entity's own when parsed, mint... | direct |
| [name](name.md) | 1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) | The IFC Name | direct |
| [long_name](long_name.md) | 1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) | The IFC LongName of a Space or Storey | direct |
| [elevation](elevation.md) | 1 <br/> [Quantity](Quantity.md) | The storey's level in the project frame | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Space](Space.md) | [contained_in](contained_in.md) | range | [Storey](Storey.md) |
| [BuildingComponent](BuildingComponent.md) | [contained_in](contained_in.md) | range | [Storey](Storey.md) |
| [Connector](Connector.md) | [contained_in](contained_in.md) | range | [Storey](Storey.md) |












## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/product




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:Storey |
| native | rcpc:Storey |






## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Storey
description: A building storey.
from_schema: https://rcpc.for5672/schema/product
slots:
- record_type
- id
- name
- long_name
- elevation
slot_usage:
  id:
    name: id
    description: 'The IFC GlobalId in its 22-character form: the entity''s own when
      parsed, minted in the same format when derived.'
    pattern: ^[0-3][0-9A-Za-z_$]{21}$
  elevation:
    name: elevation
    required: true

```
</details>

### Induced

<details>
```yaml
name: Storey
description: A building storey.
from_schema: https://rcpc.for5672/schema/product
slot_usage:
  id:
    name: id
    description: 'The IFC GlobalId in its 22-character form: the entity''s own when
      parsed, minted in the same format when derived.'
    pattern: ^[0-3][0-9A-Za-z_$]{21}$
  elevation:
    name: elevation
    required: true
attributes:
  record_type:
    name: record_type
    description: Which class in this schema the record belongs to.
    from_schema: https://rcpc.for5672/schema/product
    rank: 1000
    designates_type: true
    owner: Storey
    domain_of:
    - Storey
    - Space
    - BuildingComponent
    - Material
    range: string
    required: true
  id:
    name: id
    description: 'The IFC GlobalId in its 22-character form: the entity''s own when
      parsed, minted in the same format when derived.'
    from_schema: https://rcpc.for5672/schema/common
    identifier: true
    owner: Storey
    domain_of:
    - CapabilityType
    - MaterialCategory
    - Storey
    - Space
    - BuildingComponent
    - Material
    range: string
    required: true
    pattern: ^[0-3][0-9A-Za-z_$]{21}$
  name:
    name: name
    description: The IFC Name. Empty when the IFC file has none.
    from_schema: https://rcpc.for5672/schema/product
    rank: 1000
    owner: Storey
    domain_of:
    - Storey
    - Space
    - BuildingComponent
    range: string
    required: true
  long_name:
    name: long_name
    description: The IFC LongName of a Space or Storey. Empty when the IFC file has
      none.
    from_schema: https://rcpc.for5672/schema/product
    rank: 1000
    owner: Storey
    domain_of:
    - Storey
    - Space
    range: string
    required: true
  elevation:
    name: elevation
    description: The storey's level in the project frame. Empty when not resolved.
    from_schema: https://rcpc.for5672/schema/product
    rank: 1000
    owner: Storey
    domain_of:
    - Storey
    range: Quantity
    required: true
    inlined: true

```
</details></div>