---
search:
  boost: 10.0
---

# Class: RobotUnit 


_One robot product, entered from its Construction Robot Schema attributes. Identical machines are one entry with a count._



<div data-search-exclude markdown="1">



URI: [rcpc:RobotUnit](https://rcpc.for5672/schema/RobotUnit)





```mermaid
 classDiagram
    class RobotUnit
    click RobotUnit href "../RobotUnit/"
      RobotUnit : activity_group
        
          
    
        
        
        RobotUnit --> "1" Activity : activity_group
        click Activity href "../Activity/"
    

        
      RobotUnit : count
        
          
    
        
        
        RobotUnit --> "1" Integer : count
        click Integer href "../http://www.w3.org/2001/XMLSchema#integer/"
    

        
      RobotUnit : id
        
          
    
        
        
        RobotUnit --> "1" String : id
        click String href "../http://www.w3.org/2001/XMLSchema#string/"
    

        
      RobotUnit : operational_requirement_group
        
          
    
        
        
        RobotUnit --> "0..1" OperationalRequirement : operational_requirement_group
        click OperationalRequirement href "../OperationalRequirement/"
    

        
      RobotUnit : physical_property_group
        
          
    
        
        
        RobotUnit --> "0..1" PhysicalProperty : physical_property_group
        click PhysicalProperty href "../PhysicalProperty/"
    

        
      RobotUnit : safety_group
        
          
    
        
        
        RobotUnit --> "0..1" Safety : safety_group
        click Safety href "../Safety/"
    

        
      RobotUnit : status
        
          
    
        
        
        RobotUnit --> "0..1" RobotStatus : status
        click RobotStatus href "../RobotStatus/"
    

        
      
```




<!-- no inheritance hierarchy -->

## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [id](id.md) | 1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) | The robot's name, a readable product slug | direct |
| [count](count.md) | 1 <br/> [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) | How many identical machines this entry stands for | direct |
| [status](status.md) | 0..1 <br/> [RobotStatus](RobotStatus.md) | The runtime state of one machine | direct |
| [physical_property_group](physical_property_group.md) | 0..1 <br/> [PhysicalProperty](PhysicalProperty.md) | The Physical Property group holding the robot's dimensions, hardware, and per... | direct |
| [operational_requirement_group](operational_requirement_group.md) | 0..1 <br/> [OperationalRequirement](OperationalRequirement.md) | The Operational Requirement group holding the site conditions and people the ... | direct |
| [safety_group](safety_group.md) | 0..1 <br/> [Safety](Safety.md) | The Safety group holding how the robot protects the people and objects around... | direct |
| [activity_group](activity_group.md) | 1 <br/> [Activity](Activity.md) | The Activity group holding this robot's offered capabilities | direct |















## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/resource




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:RobotUnit |
| native | rcpc:RobotUnit |






## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: RobotUnit
description: One robot product, entered from its Construction Robot Schema attributes.
  Identical machines are one entry with a count.
from_schema: https://rcpc.for5672/schema/resource
slots:
- id
- count
- status
- physical_property_group
- operational_requirement_group
- safety_group
- activity_group
slot_usage:
  id:
    name: id
    description: The robot's name, a readable product slug. The CRS Name.
  activity_group:
    name: activity_group
    required: true

```
</details>

### Induced

<details>
```yaml
name: RobotUnit
description: One robot product, entered from its Construction Robot Schema attributes.
  Identical machines are one entry with a count.
from_schema: https://rcpc.for5672/schema/resource
slot_usage:
  id:
    name: id
    description: The robot's name, a readable product slug. The CRS Name.
  activity_group:
    name: activity_group
    required: true
attributes:
  id:
    name: id
    description: The robot's name, a readable product slug. The CRS Name.
    from_schema: https://rcpc.for5672/schema/common
    identifier: true
    owner: RobotUnit
    domain_of:
    - CapabilityType
    - Storey
    - Space
    - BuildingComponent
    - Material
    - RobotUnit
    - PhysicalProperty
    - Sensor
    - OperationalRequirement
    - Safety
    - Activity
    - Task
    - Method
    range: string
    required: true
  count:
    name: count
    description: How many identical machines this entry stands for.
    from_schema: https://rcpc.for5672/schema/resource
    owner: RobotUnit
    domain_of:
    - RobotUnit
    range: integer
    required: true
    minimum_value: 1
  status:
    name: status
    description: The runtime state of one machine.
    from_schema: https://rcpc.for5672/schema/resource
    ifabsent: RobotStatus(idle)
    owner: RobotUnit
    domain_of:
    - RobotUnit
    range: RobotStatus
  physical_property_group:
    name: physical_property_group
    description: The Physical Property group holding the robot's dimensions, hardware,
      and performance.
    from_schema: https://rcpc.for5672/schema/resource
    owner: RobotUnit
    domain_of:
    - RobotUnit
    range: PhysicalProperty
    inlined: true
  operational_requirement_group:
    name: operational_requirement_group
    description: The Operational Requirement group holding the site conditions and
      people the robot needs.
    from_schema: https://rcpc.for5672/schema/resource
    owner: RobotUnit
    domain_of:
    - RobotUnit
    range: OperationalRequirement
    inlined: true
  safety_group:
    name: safety_group
    description: The Safety group holding how the robot protects the people and objects
      around it.
    from_schema: https://rcpc.for5672/schema/resource
    owner: RobotUnit
    domain_of:
    - RobotUnit
    range: Safety
    inlined: true
  activity_group:
    name: activity_group
    description: The Activity group holding this robot's offered capabilities.
    from_schema: https://rcpc.for5672/schema/resource
    owner: RobotUnit
    domain_of:
    - RobotUnit
    range: Activity
    required: true
    inlined: true

```
</details></div>