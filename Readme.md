# Autonomous Package Delivery via ROS 2 Actions

This repository contains two ROS 2 packages that execute a 3-phase autonomous delivery mission using ROS 2 Actions.

## 1. Step-by-Step Setup Instructions
1. Navigate to your ROS 2 workspace `src` folder: `cd ~/workspaces/ros2_ws/src`
2. Clone or place the `turtlebot_delivery_[YOUR-NAME]` repository here.
3. Build the workspace using colcon: `cd ~/workspaces/ros2_ws && colcon build`
4. Source the setup file so the packages are recognized: `source install/setup.bash`

## 2. ROS 2 Commands Used (And What They Do)
* `ros2 pkg create --build-type ament_cmake [name]`: Creates a C++ based package structure, which is required for generating custom ROS 2 message/action interfaces.
* `ros2 pkg create --build-type ament_python [name]`: Creates a Python based package structure for running node logic.
* `colcon build`: Compiles the custom action definitions and builds the Python scripts.
* `source install/setup.bash`: Overlays the newly built packages onto your terminal's path.
* `ros2 run delivery_mission_controller delivery_mission_node`: Starts the Action Server node.
* `ros2 action send_goal /delivery_mission [ActionType] [Data] --feedback`: Acts as an Action Client via the terminal, sending the mission parameters and streaming the feedback to the console.

## 3. How to Test Your Nodes
Open two terminal windows and source the workspace in both (`source ~/workspaces/ros2_ws/install/setup.bash`).

**Terminal 1:** Start the server.
```bash
ros2 run delivery_mission_controller delivery_mission_node