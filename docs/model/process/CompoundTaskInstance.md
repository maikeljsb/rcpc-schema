---
search:
  boost: 10.0
---

# Class: CompoundTaskInstance 


_One planned occurrence of a compound task: the task, the method chosen to decompose it, and the instances that replaced it, one per line of the method's subtasks and in the same order._



<div data-search-exclude markdown="1">



URI: [rcpc:CompoundTaskInstance](https://rcpc.for5672/schema/CompoundTaskInstance)





```mermaid
 classDiagram
    class CompoundTaskInstance
    click CompoundTaskInstance href "../CompoundTaskInstance/"
      TaskInstance <|-- CompoundTaskInstance
        click TaskInstance href "../TaskInstance/"
      
      CompoundTaskInstance : bindings
        
          
    
        
        
        CompoundTaskInstance --> "1..*" ParameterBinding : bindings
        click ParameterBinding href "../ParameterBinding/"
    

        
      CompoundTaskInstance : compound_task
        
          
    
        
        
        CompoundTaskInstance --> "1" CompoundTask : compound_task
        click CompoundTask href "../CompoundTask/"
    

        
      CompoundTaskInstance : decomposed_by
        
          
    
        
        
        CompoundTaskInstance --> "1" Method : decomposed_by
        click Method href "../Method/"
    

        
      CompoundTaskInstance : id
        
          
    
        
        
        CompoundTaskInstance --> "1" String : id
        click String href "../http://www.w3.org/2001/XMLSchema#string/"
    

        
      CompoundTaskInstance : record_type
        
          
    
        
        
        CompoundTaskInstance --> "1" String : record_type
        click String href "../http://www.w3.org/2001/XMLSchema#string/"
    

        
      CompoundTaskInstance : subtasks
        
          
    
        
        
        CompoundTaskInstance --> "1..*" TaskInstance : subtasks
        click TaskInstance href "../TaskInstance/"
    

        
      
```





## Inheritance
* [TaskInstance](TaskInstance.md)
    * **CompoundTaskInstance**


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [compound_task](compound_task.md) | 1 <br/> [CompoundTask](CompoundTask.md) | The compound task a method decomposes, a subtask names, or an instance realis... | direct |
| [decomposed_by](decomposed_by.md) | 1 <br/> [Method](Method.md) | The method chosen to decompose a compound task instance | direct |
| [subtasks](subtasks.md) | 1..* <br/> [TaskInstance](TaskInstance.md) | The subtasks in list order, counted from 1 | direct |
| [record_type](record_type.md) | 1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) | Which class in this schema the record belongs to | [TaskInstance](TaskInstance.md) |
| [id](id.md) | 1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) | The instance's id, unique within the plan | [TaskInstance](TaskInstance.md) |
| [bindings](bindings.md) | 1..* <br/> [ParameterBinding](ParameterBinding.md) | The instance's parameters bound to object ids, keyed by parameter name | [TaskInstance](TaskInstance.md) |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [TaskNetwork](TaskNetwork.md) | [tasks](tasks.md) | range | [CompoundTaskInstance](CompoundTaskInstance.md) |












## Identifier and Mapping Information





### Schema Source


* from schema: https://rcpc.for5672/schema/process




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rcpc:CompoundTaskInstance |
| native | rcpc:CompoundTaskInstance |






## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: CompoundTaskInstance
description: 'One planned occurrence of a compound task: the task, the method chosen
  to decompose it, and the instances that replaced it, one per line of the method''s
  subtasks and in the same order.'
from_schema: https://rcpc.for5672/schema/process
is_a: TaskInstance
slots:
- compound_task
- decomposed_by
- subtasks
slot_usage:
  compound_task:
    name: compound_task
    required: true
  decomposed_by:
    name: decomposed_by
    required: true
  subtasks:
    name: subtasks
    range: TaskInstance
    required: true

```
</details>

### Induced

<details>
```yaml
name: CompoundTaskInstance
description: 'One planned occurrence of a compound task: the task, the method chosen
  to decompose it, and the instances that replaced it, one per line of the method''s
  subtasks and in the same order.'
from_schema: https://rcpc.for5672/schema/process
is_a: TaskInstance
slot_usage:
  compound_task:
    name: compound_task
    required: true
  decomposed_by:
    name: decomposed_by
    required: true
  subtasks:
    name: subtasks
    range: TaskInstance
    required: true
attributes:
  compound_task:
    name: compound_task
    description: The compound task a method decomposes, a subtask names, or an instance
      realises.
    from_schema: https://rcpc.for5672/schema/process
    rank: 1000
    owner: CompoundTaskInstance
    domain_of:
    - Method
    - Subtask
    - CompoundTaskInstance
    range: CompoundTask
    required: true
  decomposed_by:
    name: decomposed_by
    description: The method chosen to decompose a compound task instance. Empty until
      chosen.
    from_schema: https://rcpc.for5672/schema/process
    rank: 1000
    owner: CompoundTaskInstance
    domain_of:
    - CompoundTaskInstance
    range: Method
    required: true
    pattern: ^$|^[A-Za-z][A-Za-z0-9_]*$
  subtasks:
    name: subtasks
    description: The subtasks in list order, counted from 1. On a method, the entries
      of its decomposition; on a compound task instance, the instances that replaced
      it.
    from_schema: https://rcpc.for5672/schema/process
    rank: 1000
    owner: CompoundTaskInstance
    domain_of:
    - Method
    - CompoundTaskInstance
    range: TaskInstance
    required: true
    multivalued: true
  record_type:
    name: record_type
    description: Which class in this schema the record belongs to.
    from_schema: https://rcpc.for5672/schema/product
    designates_type: true
    owner: CompoundTaskInstance
    domain_of:
    - Storey
    - Space
    - BuildingComponent
    - Material
    - Task
    - Method
    - TaskNetwork
    - TaskInstance
    range: string
    required: true
  id:
    name: id
    description: The instance's id, unique within the plan.
    from_schema: https://rcpc.for5672/schema/common
    identifier: true
    owner: CompoundTaskInstance
    domain_of:
    - CapabilityType
    - MaterialCategory
    - Storey
    - Space
    - BuildingComponent
    - Material
    - ResourceEntry
    - PhysicalProperty
    - Sensor
    - OperationalRequirement
    - Safety
    - Activity
    - Task
    - Method
    - TaskNetwork
    - TaskInstance
    range: string
    required: true
  bindings:
    name: bindings
    description: The instance's parameters bound to object ids, keyed by parameter
      name.
    from_schema: https://rcpc.for5672/schema/process
    rank: 1000
    owner: CompoundTaskInstance
    domain_of:
    - TaskInstance
    range: ParameterBinding
    required: true
    multivalued: true
    inlined: true

```
</details></div>