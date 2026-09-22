# resource

Robots as resources. One RobotUnit entry per robot product, holding the four Construction Robot Schema groups and the capabilities the robot offers.

URI: https://rcpc.for5672/schema/resource

Name: resource



## Classes

| Class | Description |
| --- | --- |
| [Activity](Activity.md) | CRS group 4: the capabilities a robot offers and how it performs them |
| [OperationalRequirement](OperationalRequirement.md) | CRS group 2: the site conditions and the people the robot needs to work |
| [PhysicalProperty](PhysicalProperty.md) | CRS group 1: the robot's physical dimensions, hardware, and performance |
| [ResourceEntry](ResourceEntry.md) | Something a method draws on, counted in identical units: a robot product or a... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[RobotUnit](RobotUnit.md) | One robot product, entered from its Construction Robot Schema attributes |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Stock](Stock.md) | A stock a method uses one unit of, such as formwork panels or rebar |
| [Safety](Safety.md) | CRS group 3: how the robot protects the people and objects around it |
| [Sensor](Sensor.md) | One sensor on or around the robot |



## Slots

| Slot | Description |
| --- | --- |
| [accuracy](accuracy.md) | How close the robot's work comes to the target, recommended in millimetres |
| [activity_group](activity_group.md) | The Activity group holding this robot's offered capabilities |
| [additional_ppe_requirements](additional_ppe_requirements.md) | Extra personal protective equipment required when humans operate or work with... |
| [coordinate_reach](coordinate_reach.md) | How far the manipulator reaches along each of the robot's three axes, recomme... |
| [count](count.md) | How many identical units this entry stands for: machines of a robot product, ... |
| [crew_information](crew_information.md) | The composition of the team working with the robot |
| [crew_responsibilities](crew_responsibilities.md) | What the crew does while the robot performs its tasks |
| [data_output_file_type](data_output_file_type.md) | The file formats of the data the robot's sensors output |
| [data_output_type](data_output_type.md) | The forms of data the robot's sensors output |
| [degree_of_freedom](degree_of_freedom.md) | How many axes of the manipulator can rotate or extend |
| [emergency_stop](emergency_stop.md) | Whether the robot stops automatically and immediately when specific condition... |
| [end_effector](end_effector.md) | The tools the robot's manipulator can attach, such as a bucket or gripper |
| [grade](grade.md) | The range of ground slopes the robot can work on, recommended in degrees |
| [humidity](humidity.md) | The range of relative humidity at which the robot works properly, recommended... |
| [level_of_autonomy](level_of_autonomy.md) | How independently the robot performs its tasks |
| [lifting_capacity](lifting_capacity.md) | The maximum weight the manipulator can lift during operation, recommended in ... |
| [load_capacity](load_capacity.md) | The maximum weight the robot can carry for extended work, recommended in kilo... |
| [manipulator](manipulator.md) | The robot's arm: the links and joints that perform tasks |
| [manipulator_position](manipulator_position.md) | Where the manipulator is mounted on the robot, a point in the robot's own fra... |
| [manufacturer](manufacturer.md) | Who makes the robot |
| [minimum_workspace](minimum_workspace.md) | The minimum space the robot needs to operate without collisions, recommended ... |
| [mobility](mobility.md) | How the robot moves from one place to another |
| [navigation](navigation.md) | Whether the robot can find its own position and plan a path to a destination |
| [network](network.md) | How the robot communicates and exchanges data |
| [object_detection_range](object_detection_range.md) | How far away the robot can detect and recognise objects, recommended in metre... |
| [offers](offers.md) | The capability types this robot offers |
| [operational_requirement_group](operational_requirement_group.md) | The Operational Requirement group holding the site conditions and people the ... |
| [operator_responsibilities](operator_responsibilities.md) | What the operator does while the robot performs its tasks |
| [physical_property_group](physical_property_group.md) | The Physical Property group holding the robot's dimensions, hardware, and per... |
| [pitch](pitch.md) | The manipulator's rotation range around the lateral axis, recommended in degr... |
| [power_source](power_source.md) | What supplies the robot's energy |
| [precision](precision.md) | How finely the robot repeats its work, recommended in millimetres |
| [productivity](productivity.md) | How much work the robot does per unit of time, in a unit that fits the activi... |
| [req_number_operators](req_number_operators.md) | How many people control the robot |
| [roll](roll.md) | The manipulator's rotation range around the longitudinal axis, recommended in... |
| [run_duration](run_duration.md) | How long the robot can run continuously on its power source, recommended in m... |
| [safe_distance](safe_distance.md) | The minimum distance to keep between humans and the robot while they work tog... |
| [safety_barrier](safety_barrier.md) | Whether the robot has a facility to avoid collisions with humans or objects |
| [safety_group](safety_group.md) | The Safety group holding how the robot protects the people and objects around... |
| [sensor_location](sensor_location.md) | Where the sensor sits on the robot, a point in the robot's own frame |
| [sensor_requirements](sensor_requirements.md) | What installing the sensor requires |
| [sensor_type](sensor_type.md) | What kind of sensor this is |
| [sensors](sensors.md) | The sensors mounted on or around the robot |
| [site_preparation](site_preparation.md) | What the site needs before the robot can work properly on it |
| [speed](speed.md) | How fast the robot travels, recommended in metres per second |
| [status](status.md) | The runtime state of one machine |
| [temperature](temperature.md) | The range of temperatures at which the robot works properly, recommended in d... |
| [worker_responsibilities](worker_responsibilities.md) | What the workers do while the robot performs its tasks |
| [worker_type](worker_type.md) | The kinds of worker who work with the robot |
| [yaw](yaw.md) | The manipulator's rotation range around the vertical axis, recommended in deg... |


## Enumerations

| Enumeration | Description |
| --- | --- |
| [RobotStatus](RobotStatus.md) | The runtime state of one machine |


## Types

| Type | Description |
| --- | --- |


## Subsets

| Subset | Description |
| --- | --- |
