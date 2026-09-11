---
search:
  boost: 10.0
---

# Class: CapabilityType 


_Something a robot can do, named by a bare verb, that a PrimitiveTask requires and a RobotType offers. The id is the name; matching is by id and there are no levels or qualifiers. Type-level allocation asks whether a robot type offers every capability a task requires._



<div data-search-exclude markdown="1">



URI: [rcpc:CapabilityType](https://rcpc.for5672/schema/CapabilityType)





```mermaid
 classDiagram
    class CapabilityType
    click CapabilityType href "../CapabilityType/"
      CapabilityType : description
        
          
    
        
        
        CapabilityType --> "1" String : description
        click String href "../http://www.w3.org/2001/XMLSchema#string/"
    

        
      CapabilityType : id
        
          
    
        
        
        CapabilityType --> "1" String : id
        click String href "../http://www.w3.org/2001/XMLSchema#string/"
    

        
      
```




<!-- no inheritance hierarchy -->

## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [id](id.md) | 1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) | Identifier, unique among instances of its class | direct |
| [description](description.md) | 1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) | What this is, for a human reader | direct |















## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/common




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:CapabilityType |
| native | rcpc:CapabilityType |






## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: CapabilityType
description: Something a robot can do, named by a bare verb, that a PrimitiveTask
  requires and a RobotType offers. The id is the name; matching is by id and there
  are no levels or qualifiers. Type-level allocation asks whether a robot type offers
  every capability a task requires.
from_schema: https://rcpc.for5672/schema/common
slots:
- id
- description
slot_usage:
  description:
    name: description
    required: true

```
</details>

### Induced

<details>
```yaml
name: CapabilityType
description: Something a robot can do, named by a bare verb, that a PrimitiveTask
  requires and a RobotType offers. The id is the name; matching is by id and there
  are no levels or qualifiers. Type-level allocation asks whether a robot type offers
  every capability a task requires.
from_schema: https://rcpc.for5672/schema/common
slot_usage:
  description:
    name: description
    required: true
attributes:
  id:
    name: id
    description: Identifier, unique among instances of its class. The class is always
      known from the slot that references it, so the id carries no namespace.
    from_schema: https://rcpc.for5672/schema/common
    rank: 1000
    identifier: true
    owner: CapabilityType
    domain_of:
    - CapabilityType
    range: string
    required: true
  description:
    name: description
    description: What this is, for a human reader.
    from_schema: https://rcpc.for5672/schema/common
    rank: 1000
    owner: CapabilityType
    domain_of:
    - CapabilityType
    range: string
    required: true

```
</details></div>