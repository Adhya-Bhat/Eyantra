# Task 1A – ROS 2 Based PID Control of Swift Pico Drone

## Overview
This task was completed as part of the simulation round of the e-Yantra Krishi Drone theme. Pls note that the PID tuning wasnt properly achieved though the PID algorithm and pipeline is correctly implemented.

The objective of Task 1A was to implement a ROS 2 node that stabilizes and holds the position of the Swift Pico drone using a PID controller.

The node:

* Subscribes to position data from WhyCon which you can assume as a webcam looking overlooking the scene. 
* Computes PID corrections for roll, pitch and throttle
* Publishes control commands to the drone
* Publishes error values for monitoring and tuning

All testing was performed in simulation.

---

# Demo Video

Here is a video of the simulation demonstrating the current implementation:

https://youtu.be/ow1ocCcIfL0

# Node Description

The ROS 2 node is named:
pico_controller

It performs closed-loop control to hold the drone at a desired position.

# Subscribed Topics

* `/whycon/poses` → Current drone position
* `/throttle_pid` → PID tuning for altitude
* `/pitch_pid` → PID tuning for pitch
* `/roll_pid` → PID tuning for roll

# Published Topics

* `/drone_command` → RC control commands
* `/roll_error` → Roll axis error
* `/pitch_error` → Pitch axis error
* `/alt_error` → Altitude error


# Control Strategy

### 1. State Representation

Instead of using separate variables for x, y and z, I used list-based indexing:

self.current_state = [x, y, z]
self.desired_state = [x_d, y_d, z_d]


This improves modularity and makes PID computation cleaner.

# 2. PID Implementation

For each axis (roll, pitch, throttle), the following were computed:

* Proportional Error
* Derivative Error
* Integral Error

The control output was calculated as:

Output = Kp * error + Ki * sum_error + Kd * derivative_error

The output was added to the neutral RC value (1500) to generate control signals.

# 3. Sampling Time

PID runs at a fixed sample time of:
0.033 seconds

This ensures stable and predictable control updates.

# 4. Output Limiting

To prevent unsafe command values:

* Maximum values were limited to 2000
* Minimum values were limited to 1000 (with a higher lower bound for throttle)

This ensures the drone receives bounded RC commands.

# 5. Arming and Disarming Logic

Before starting control:

* Drone is first disarmed
* Then armed with proper RC initialization

This ensures safe startup behavior.

---
# PID Tuning and Limitations

PID parameters were tuned through simulation using the `/drone_pid_tuner`.

While the controller logic is implemented correctly, I was not able to fully tune the PID gains to achieve perfect stability some oscillations and deviations still remain in the simulation.

The tuning process I used was:

1. Increase Kp gradually until the response increased
2. Add Kd to reduce oscillations
3. Add Ki to reduce steady-state error

However, due to time constraints and simulation behavior, the response was not completely stable in all axes.

This remains a limitation of the current implementation, and further tuning can improve performance.


# Challenges Faced

* Achieving stable hover without oscillation
* Selecting correct sign conventions for control outputs
* Balancing responsiveness and damping
* Preventing integral wind-up
* Fine-tuning throttle PID for altitude stability

Since this task was simulation-based, no hardware-related noise was involved.

# Assumptions

* WhyCon provides accurate position feedback
* Sampling interval remains consistent
* Drone dynamics are consistent within simulation

---

# Key Learnings

Through this task, I gained practical understanding of:

* ROS 2 publisher–subscriber architecture
* Implementing real-time PID control
* Tuning control parameters
* Error monitoring through topic publishing

This task helped bridge theoretical control systems knowledge with implementation in a ROS-based drone simulation.

If anybody has a good understanding of PID tuning I would love to hear your opinions or advice on it. You can connect with me via Linkedin or gmail.