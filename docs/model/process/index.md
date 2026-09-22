# process

Tasks and how they decompose. PrimitiveTask, CompoundTask, and Method as the catalogue; TaskNetwork, CompoundTaskInstance, and PrimitiveTaskInstance as a plan: what is asked for, and each planned occurrence bound to components, spaces, and machines.

URI: https://rcpc.for5672/schema/process

Name: process



## Classes

| Class | Description |
| --- | --- |
| [Method](Method.md) | One way to decompose a compound task into an ordered network of subtasks, for... |
| [Parameter](Parameter.md) | HDDL's typed variable: one declared parameter of a task or a method, its name... |
| [ParameterBinding](ParameterBinding.md) | One parameter of a task instance bound to one object |
| [Subtask](Subtask.md) | One entry of a method's subtask list: the task it names and the arguments it ... |
| [Task](Task.md) | HDDL's task: a name and typed parameters, before it is said whether the task ... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[CompoundTask](CompoundTask.md) | HDDL's abstract task: a task performed only by decomposing it through a metho... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[PrimitiveTask](PrimitiveTask.md) | HDDL's action: a task a robot performs directly, with what performing it requ... |
| [TaskInstance](TaskInstance.md) | One planned occurrence of a task, before it is said whether the task is primi... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[CompoundTaskInstance](CompoundTaskInstance.md) | One planned occurrence of a compound task: the task, the method chosen to dec... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[PrimitiveTaskInstance](PrimitiveTaskInstance.md) | One planned occurrence of a primitive task: the action and every parameter of... |
| [TaskNetwork](TaskNetwork.md) | HDDL's initial task network: what the plan is asked to accomplish, the compou... |



## Slots

| Slot | Description |
| --- | --- |
| [applies_to](applies_to.md) | The material category of the components a method decomposes its task for; a c... |
| [arguments](arguments.md) | The values a subtask passes, in the named task's parameter order: method para... |
| [bindings](bindings.md) | The instance's parameters bound to object ids, keyed by parameter name |
| [bound_to](bound_to.md) | The id of the object the parameter is bound to: a BuildingComponent, a Space,... |
| [compound_task](compound_task.md) | The compound task a method decomposes, a subtask names, or an instance realis... |
| [decomposed_by](decomposed_by.md) | The method chosen to decompose a compound task instance |
| [duration](duration.md) | How long one performance of the primitive task takes, recommended in seconds |
| [ordering](ordering.md) | Pairs of positions in the owner's subtask or task list; in each pair the firs... |
| [parameter_kind](parameter_kind.md) | The kind of object the parameter ranges over |
| [parameter_name](parameter_name.md) | The parameter's name, a plain word such as c, r, or from |
| [parameters](parameters.md) | The declared parameters, keyed by name |
| [primitive_task](primitive_task.md) | The primitive task a subtask names or an instance realises |
| [requires](requires.md) | The capabilities a robot must offer to perform the primitive task |
| [subtasks](subtasks.md) | The subtasks in list order, counted from 1 |
| [tasks](tasks.md) | The network's tasks in list order, counted from 1, each position its label |
| [uses](uses.md) | The stocks a method holds one unit of each for its whole span |


## Enumerations

| Enumeration | Description |
| --- | --- |
| [ParameterKind](ParameterKind.md) | The kinds of object a parameter ranges over |


## Types

| Type | Description |
| --- | --- |


## Subsets

| Subset | Description |
| --- | --- |
