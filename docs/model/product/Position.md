---
search:
  boost: 10.0
---

# Class: Position 


_Three cartesian coordinates and their unit: a point, or an extent along each axis._



<div data-search-exclude markdown="1">



URI: [rcpc:Position](https://rcpc.for5672/schema/Position)





```mermaid
 classDiagram
    class Position
    click Position href "../Position/"
      Position : unit
        
          
    
        
        
        Position --> "1" String : unit
        click String href "../http://www.w3.org/2001/XMLSchema#string/"
    

        
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
| [x_coord](x_coord.md) | 1 <br/> [xsd:float](http://www.w3.org/2001/XMLSchema#float) | Cartesian x coordinate | direct |
| [y_coord](y_coord.md) | 1 <br/> [xsd:float](http://www.w3.org/2001/XMLSchema#float) | Cartesian y coordinate | direct |
| [z_coord](z_coord.md) | 1 <br/> [xsd:float](http://www.w3.org/2001/XMLSchema#float) | Cartesian z coordinate | direct |
| [unit](unit.md) | 1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) | The unit of the value, of the coordinates, or of the bounds | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [BuildingComponent](BuildingComponent.md) | [target_location](target_location.md) | range | [Position](Position.md) |
| [BuildingComponent](BuildingComponent.md) | [supply_location](supply_location.md) | range | [Position](Position.md) |
| [BuildingComponent](BuildingComponent.md) | [current_location](current_location.md) | range | [Position](Position.md) |












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
description: 'Three cartesian coordinates and their unit: a point, or an extent along
  each axis.'
from_schema: https://rcpc.for5672/schema/common
slots:
- x_coord
- y_coord
- z_coord
- unit
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
  unit:
    name: unit
    required: true

```
</details>

### Induced

<details>
```yaml
name: Position
description: 'Three cartesian coordinates and their unit: a point, or an extent along
  each axis.'
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
  unit:
    name: unit
    required: true
attributes:
  x_coord:
    name: x_coord
    description: Cartesian x coordinate.
    from_schema: https://rcpc.for5672/schema/common
    owner: Position
    domain_of:
    - Position
    range: float
    required: true
  y_coord:
    name: y_coord
    description: Cartesian y coordinate.
    from_schema: https://rcpc.for5672/schema/common
    owner: Position
    domain_of:
    - Position
    range: float
    required: true
  z_coord:
    name: z_coord
    description: Cartesian z coordinate.
    from_schema: https://rcpc.for5672/schema/common
    owner: Position
    domain_of:
    - Position
    range: float
    required: true
  unit:
    name: unit
    description: The unit of the value, of the coordinates, or of the bounds.
    from_schema: https://rcpc.for5672/schema/common
    owner: Position
    domain_of:
    - Position
    - Quantity
    - Interval
    range: string
    required: true

```
</details></div>