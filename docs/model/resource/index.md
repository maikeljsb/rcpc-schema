# resource

Robots as resources. One RobotUnit entry per robot product, holding the four Construction Robot Schema groups and the capabilities the robot offers.

URI: https://rcpc.for5672/schema/resource

Name: resource



## Classes

| Class | Description |
| --- | --- |
| [Activity](Activity.md) | CRS group 4: the capabilities a robot offers and how it performs them |
| [PhysicalProperty](PhysicalProperty.md) | CRS group 1: the robot's physical dimensions, hardware, and performance |
| [RobotUnit](RobotUnit.md) | One robot product, entered from its Construction Robot Schema attributes |
| [Sensor](Sensor.md) | One sensor on or around the robot |



## Slots

| Slot | Description |
| --- | --- |
| [activity_group](activity_group.md) | The Activity group holding this robot's offered capabilities |
| [coordinate_reach](coordinate_reach.md) | How far the manipulator reaches along each of the robot's three axes, recomme... |
| [count](count.md) | How many identical machines this entry stands for |
| [degree_of_freedom](degree_of_freedom.md) | How many axes of the manipulator can rotate or extend |
| [end_effector](end_effector.md) | The tools the robot's manipulator can attach, such as a bucket or gripper |
| [level_of_autonomy](level_of_autonomy.md) | How independently the robot performs its tasks |
| [lifting_capacity](lifting_capacity.md) | The maximum weight the manipulator can lift during operation, recommended in ... |
| [load_capacity](load_capacity.md) | The maximum weight the robot can carry for extended work, recommended in kilo... |
| [manipulator](manipulator.md) | The robot's arm: the links and joints that perform tasks |
| [manipulator_position](manipulator_position.md) | Where the manipulator is mounted on the robot, a point in the robot's own fra... |
| [manufacturer](manufacturer.md) | Who makes the robot |
| [mobility](mobility.md) | How the robot moves from one place to another |
| [navigation](navigation.md) | Whether the robot can find its own position and plan a path to a destination |
| [network](network.md) | How the robot communicates and exchanges data |
| [offers](offers.md) | The capability types this robot offers |
| [physical_property](physical_property.md) | The Physical Property group holding the robot's dimensions, hardware, and per... |
| [pitch](pitch.md) | The manipulator's rotation range around the lateral axis, recommended in degr... |
| [power_source](power_source.md) | What supplies the robot's energy |
| [roll](roll.md) | The manipulator's rotation range around the longitudinal axis, recommended in... |
| [run_duration](run_duration.md) | How long the robot can run continuously on its power source, recommended in m... |
| [sensor_location](sensor_location.md) | Where the sensor sits on the robot, a point in the robot's own frame |
| [sensor_requirements](sensor_requirements.md) | What installing the sensor requires |
| [sensor_type](sensor_type.md) | What kind of sensor this is |
| [sensors](sensors.md) | The sensors mounted on or around the robot |
| [speed](speed.md) | How fast the robot travels, recommended in metres per second |
| [status](status.md) | The runtime state of one machine |
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
