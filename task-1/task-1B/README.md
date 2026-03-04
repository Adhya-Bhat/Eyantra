# Task 1B – Drone Pattern Drawing using ROS2 (Turtlesim)

## Overview

In this task, I implemented a ROS2 node to control the turtlesim and draw a drone-like structure. The drawing consists of:

* Four circular propellers
* A square frame
* Four diagonal connector lines
* Final repositioning of the turtle to the centre

The node uses publishers, service clients, timers, and futures to coordinate the complete drawing sequence.

---
## Implementation Video 
Here is the implementation video
https://youtu.be/lO66zRaP6rY

## Node Details

**Node Name:** `DrawCommandNode`
**Class Name:** `DroneDraw`

### Topics Used

* `/turtle1/cmd_vel` → Publishing `Twist` messages to draw circles

### Services Used

* `/turtle1/set_pen` → To control pen state (on/off, color, width)
* `/turtle1/teleport_absolute` → To reposition the turtle precisely

---

## Implementation Logic

### 1. Drawing Circles (Propellers)

Each propeller is drawn using velocity commands:

* Linear velocity: `10.0`
* Angular velocity: `10.0`
* Timer period: `0.1s`
* Drawing duration: ~0.7 seconds

A timer is created for each circle, and once the required time is reached:

* The timer is destroyed
* Velocity is set to zero
* A `Future` object is completed to move to the next circle

I used four separate `Future` objects (`circle1Future`, `circle2Future`, etc.) to ensure that circles are drawn sequentially.

Circle positions:

* (2.0, 1.0)
* (2.0, 7.0)
* (8.0, 7.0)
* (8.0, 1.0)

---

### 2. Drawing the Frame (Rectangle)

The frame is created using teleportation between points:

* (3.0, 5.0)
* (5.0, 7.0)
* (7.0, 5.0)
* (5.0, 3.0)

Pen state is toggled appropriately to avoid unwanted lines.

---

### 3. Drawing Connector Lines

Diagonal connectors are drawn from inner square corners to the outer circle centres:

* (4,4) → (2,2)
* (4,6) → (2,8)
* (6,6) → (8,8)
* (6,4) → (8,2)

Each connector is drawn by teleporting with pen enabled.

---

### 4. Centre Positioning

At the end of execution, the turtle is teleported back to:

(5.0, 5.0)

This ensures the drone drawing is centred and the turtle finishes at the middle.

---

## Issue Faced

Initially, I forgot to reposition the turtle back to the centre at the end of execution.

Because of that, my output did not match the expected final state, and I ended up submitting multiple times before realizing the mistake. After debugging the sequence carefully, I added the `centreDrone()` function call at the end to fix the issue.

---

## Key Concepts Used

* ROS2 Node creation (`rclpy`)
* Publishers and message handling
* Service clients and asynchronous calls
* `Future` objects for synchronization
* Timers for controlled motion
* Sequential task execution

---

## How to Run

1. Start turtlesim:

   ```bash
   ros2 run turtlesim turtlesim_node
   ```

2. Run this node:

   ```bash
   ros2 run <your_package_name> <your_python_file_name>
   ```

---

## Final Output

The turtle draws:

* Four circular propellers
* A square frame
* Four diagonal connectors
* Returns to the centre

This completes the drone structure.

---