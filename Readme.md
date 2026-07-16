# Autonomous Package Delivery via ROS 2 Actions

## 📖 Project Overview
This repository contains a complete ROS 2 workspace designed to execute a 3-phase autonomous delivery mission. By leveraging the asynchronous power of ROS 2 Actions, the system allows a robot (such as a TurtleBot) to receive a complex goal, execute sequential kinematics, stream real-time progress feedback, and handle preemptive cancellations or timeouts safely.

### **The Two Packages:**
1. **`delivery_mission_interfaces` (CMake):** The contract. Defines the custom `DeliveryMission.action` interface containing the precise floats and booleans for the Goal, Result, and Feedback parameters.
2. **`delivery_mission_controller` (Python):** The executor. A node that acts as an Action Server. It translates the mission parameters into actionable `Twist` commands on `/cmd_vel`, driving the robot through the pickup, pause, and delivery phases while monitoring strict timeout constraints.

---

## 📂 Repository Structure

```text
turtlebot_delivery_youssef_ahmed/
├── delivery_mission_controller/
│   ├── delivery_mission_controller/
│   │   ├── __init__.py
│   │   └── delivery_mission_node.py       # Main Action Server logic
│   ├── package.xml
│   ├── setup.py
│   └── setup.cfg
└── delivery_mission_interfaces/
    ├── action/
    │   └── DeliveryMission.action         # Custom interface definition
    ├── CMakeLists.txt                     # Configured with rosidl_default_generators
    └── package.xml
```

---

## ⚙️ 1. Step-by-Step Setup Instructions


### Workspace Setup
1. **Prepare the workspace:**
   ```bash
   mkdir -p ~/workspaces/ros2_ws/src
   cd ~/workspaces/ros2_ws/src
   ```
2. **Clone/Place the repository:**
   Place the `turtlebot_delivery_youssef_ahmed` folder directly inside the `src` directory.

3. **Build the packages:**
   Always run `colcon build` from the **root** of the workspace, never from inside the source folders.
   ```bash
   cd ~/workspaces/ros2_ws
   colcon build --packages-select delivery_mission_interfaces delivery_mission_controller
   ```

4. **Source the installation:**
   ```bash
   source ~/workspaces/ros2_ws/install/setup.bash
   ```
   *(Note: Ensure you do not accidentally append a `~` to the end of this command, or Linux will look for a hidden backup file instead of the executable script).*

---

## 💻 2. ROS 2 Commands (And What They Do)

* `ros2 pkg create --build-type ament_cmake delivery_mission_interfaces`: Generates a C++ package environment. This is absolutely mandatory for creating custom interfaces (`.action`, `.msg`, `.srv`) because ROS 2 uses CMake generators to compile these text files into usable C++ and Python libraries.
* `ros2 pkg create --build-type ament_python delivery_mission_controller`: Generates a pure Python package environment for our node logic, keeping the workspace modular.
* `colcon build --packages-select [package_name]`: Compiles only the specified packages. This is much faster than building an entire workspace and prevents cross-contamination of cache files.
* `source install/setup.bash`: Overlays the newly built workspace onto your terminal's path. Without this, ROS 2 will not know your custom action or node exists.
* `ros2 run [package] [executable]`: Starts a specific compiled node.
* `ros2 action send_goal [action_name] [action_type] [YAML_data] --feedback`: Spawns a temporary Action Client in the terminal. It parses the YAML string into the Goal structure, transmits it to the Action Server, and actively prints the feedback stream.

---

## 🚀 3. How to Test Your Nodes

You will need two separate terminal windows. **Remember to source the workspace in both terminals** before running the commands.

**Terminal 1: Start the Mission Controller (Server)**
```bash
source ~/workspaces/ros2_ws/install/setup.bash
ros2 run delivery_mission_controller delivery_mission_node
```

**Terminal 2: Dispatch the Mission (Client)**
```bash
source ~/workspaces/ros2_ws/install/setup.bash
ros2 action send_goal /delivery_mission delivery_mission_interfaces/action/DeliveryMission "{speed: 0.5, pickup_duration: 4.0, delivery_duration: 6.0, timeout: 20.0}" --feedback
```

---

## 📊 4. Expected Output

### Server Terminal
When the server starts, it will idle. Once the goal is dispatched from Terminal 2, you will see a real-time log of the kinematics phases:
```text
[INFO] [delivery_mission_node]: Delivery Mission Controller is ready.
[INFO] [delivery_mission_node]: Executing delivery mission...
[INFO] [delivery_mission_node]: Phase 1: Driving to pickup for 4.0s at 0.5m/s
[INFO] [delivery_mission_node]: Phase 2: Stopping for pickup simulation.
[INFO] [delivery_mission_node]: Phase 3: Driving to delivery for 6.0s
[INFO] [delivery_mission_node]: Mission Completed Successfully!
```

### Client Terminal
The client will acknowledge the accepted goal and immediately begin printing the feedback array, culminating in the final Boolean result:
```text
Goal accepted with ID: [...]
Feedback:
    remaining_time: 12.9
    pickup_progress: 0.0
...
Feedback:
    remaining_time: 7.5
    pickup_progress: 50.0
...
Result:
    success: true
    message: "Delivery mission executed successfully."
```

---

## 🤖 5. Demo: Video

https://drive.google.com/file/d/1IoqMXwlYh_utkgfWcQhaELDhdzM0Fv4r/view?usp=sharing

