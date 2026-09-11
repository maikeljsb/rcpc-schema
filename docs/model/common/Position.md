---
search:
  boost: 10.0
---

# Class: Position 


_A point in the IFC project coordinate frame, in metres._



<div data-search-exclude markdown="1">



URI: [rcpc:Position](https://rcpc.for5672/schema/Position)





```mermaid
 classDiagram
    class Position
    click Position href "../Position/"
      Position : x_coord
        
          
    
        
        
        Position --> "1" Float : x_coord
        click Float href "../http://www.w3.org/2001/XMLSchema#float/"
    

        
      Position : y_coord
        
          
    
        
        
        Position --> "1" Float : y_coord
        click Float href "../http://www.w3.org/2001/XMLSchema#float/"
    

        
      Position : z_coord
        
          
    
        
        
        Position --> "1" Float : z_coord
        click Float href "../http://www.w3.org/2001/XMLSchema#float/"
    

        
      
```




<!-- no inheritance hierarchy -->

## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [x_coord](x_coord.md) | 1 <br/> [xsd:float](http://www.w3.org/2001/XMLSchema#float) | Easting, in metres | direct |
| [y_coord](y_coord.md) | 1 <br/> [xsd:float](http://www.w3.org/2001/XMLSchema#float) | Northing, in metres | direct |
| [z_coord](z_coord.md) | 1 <br/> [xsd:float](http://www.w3.org/2001/XMLSchema#float) | Height, in metres | direct |















## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/common




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:Position |
| native | rcpc:Position |






## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Position
description: A point in the IFC project coordinate frame, in metres.
from_schema: https://rcpc.for5672/schema/common
slots:
- x_coord
- y_coord
- z_coord
slot_usage:
  x_coord:
    name: x_coord
    required: true
  y_coord:
    name: y_coord
    required: true
  z_coord:
    name: z_coord
    required: true

```
</details>

### Induced

<details>
```yaml
name: Position
description: A point in the IFC project coordinate frame, in metres.
from_schema: https://rcpc.for5672/schema/common
slot_usage:
  x_coord:
    name: x_coord
    required: true
  y_coord:
    name: y_coord
    required: true
  z_coord:
    name: z_coord
    required: true
attributes:
  x_coord:
    name: x_coord
    description: Easting, in metres.
    from_schema: https://rcpc.for5672/schema/common
    rank: 1000
    owner: Position
    domain_of:
    - Position
    range: float
    required: true
  y_coord:
    name: y_coord
    description: Northing, in metres.
    from_schema: https://rcpc.for5672/schema/common
    rank: 1000
    owner: Position
    domain_of:
    - Position
    range: float
    required: true
  z_coord:
    name: z_coord
    description: Height, in metres.
    from_schema: https://rcpc.for5672/schema/common
    rank: 1000
    owner: Position
    domain_of:
    - Position
    range: float
    required: true

```
</details></div>