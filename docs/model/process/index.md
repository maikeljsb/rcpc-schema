# process

Tasks and how they decompose. PrimitiveTask, CompoundTask, and Method as the catalogue; TaskNetwork, CompoundTaskInstance, and PrimitiveTaskInstance as a plan: what is asked for, and each planned occurrence bound to components, spaces, and machines.

URI: https://rcpc.for5672/schema/process

Name: process



## Classes

| Class | Description |
| --- | --- |
| [Parameter](Parameter.md) | One declared parameter of a task or a method: the kind of object it ranges ov... |
| [Task](Task.md) | HDDL's task: a name and typed parameters, before it is said whether the task ... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[CompoundTask](CompoundTask.md) | HDDL's abstract task: a task performed only by decomposing it through a metho... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[PrimitiveTask](PrimitiveTask.md) | HDDL's action: a task a robot performs directly, with what performing it requ... |



## Slots

| Slot | Description |
| --- | --- |
| [applies_to](applies_to.md) | The materials a method applies to, as IFC spells them; a component matches wh... |
| [duration](duration.md) | How long one performance of the primitive task takes, recommended in seconds |
| [parameter_kind](parameter_kind.md) | The kind of object the parameter ranges over |
| [parameter_name](parameter_name.md) | The parameter's name, a plain word such as c, r, or from |
| [parameters](parameters.md) | The declared parameters, keyed by name |
| [requires](requires.md) | The capabilities a robot must offer to perform the primitive task |


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
