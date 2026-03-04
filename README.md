
# Krishi Drone – KD_1136

## e-Yantra Robotics Competition 2025 – Simulation Round

This repository contains the implementation of **Task 1A, Task 1B, and Task 1C** for the Krishi Drone theme.

Technologies used:

* Python 3
* ROS 2 (rclpy)
* OpenCV
* Turtlesim
* WhyCon (simulation-based pose estimation)

---

#  Repository Structure

```
KD_1136/
│
├── KD_1136_task_1a/
│   ├── pico_controller.py
│   └── README.md
│
├── KD_1136_task_1b/
│   ├── KD_1136_task_1b.py
│   ├── README.md
│   └── metadata.yaml
│
├── KD_1136_task_1c/
│   ├── draw_command_node.py
│   ├── README.md
│   └── images/
│
└── README.md
```

---

# Task 1A – ROS 2 Based PID Control of Swift Pico Drone

### Objective

Design and implement a ROS 2 node to stabilize and hold the position of the Swift Pico drone using a PID controller in simulation.

### Implementation Highlights

* Subscribes to `/whycon/poses` for position feedback
* Computes PID corrections for:

  * Roll
  * Pitch
  * Throttle
* Publishes RC commands to `/drone_command`
* Publishes error topics for monitoring and tuning
* Implements arming/disarming logic
* Applies output saturation limits (1000–2000 range)

### Control Details

* Sampling time: **0.033 seconds**
* State stored as indexed lists for modular PID computation
* Control output added to neutral RC value (1500)
* Integral, derivative and proportional terms implemented explicitly

 **Note:**
While the PID control pipeline is correctly implemented, full stability was not achieved due to incomplete tuning. Oscillations and deviations remain in simulation, especially during hover stabilization.

 Demo Video:
[https://youtu.be/ow1ocCcIfL0](https://youtu.be/ow1ocCcIfL0)

 Detailed explanation available in:
`KD_1136_task_1a/README.md`

---

#  Task 1B – Image Processing

### Objective

Detect specific colored regions from the given image using HSV thresholding.

### Approach

* Convert image to HSV
* Apply color threshold
* Generate mask
* Extract required regions

 Detailed explanation available in:
`KD_1136_task_1b/README.md`

---

#  Task 1C – Drone Pattern Drawing using ROS 2

### Objective

Control turtlesim to draw a drone-like structure.

### Implementation Highlights

* Four circular propellers using velocity commands
* Square frame using teleport service
* Diagonal connector lines
* Final repositioning to centre

 Initial issue:
The turtle was not repositioned to the centre in early submissions, leading to repeated incorrect outputs before debugging the execution sequence.

 Detailed explanation available in:
`KD_1136_task_1c/README.md`

---

#  Overall Challenges

* PID tuning for stable hover
* Managing sign conventions for control axes
* Preventing oscillations and integral wind-up
* Coordinating sequential execution using ROS2 timers and futures
* Ensuring final state consistency for evaluation

---

#  Execution Instructions

## Task 1A

```
ros2 run <your_package_name> pico_controller
```

## Task 1B

```
python3 KD_1136_task_1b.py -i <input_image>
```

## Task 1C

```
ros2 run turtlesim turtlesim_node
ros2 run <your_package_name> <executable_name>
```

---

# Learning Outcome

This repository demonstrates:

* Closed-loop control using PID in ROS 2
* Real-time feedback processing
* Topic-based error monitoring
* Service-client architecture
* Simulation-based robotics workflow

---

