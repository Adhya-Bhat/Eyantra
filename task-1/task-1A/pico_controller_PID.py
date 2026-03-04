#!/usr/bin/env python3

'''
This python file runs a ROS 2-node of name pico_control which holds the position of Swift Pico Drone on the given drone.
This node publishes and subsribes the following topics:

		PUBLICATIONS			SUBSCRIPTIONS
		/drone_command			/whycon/poses
		/pid_error				/throttle_pid
								/pitch_pid
								/roll_pid
					
Rather than using different variables, use list. eg : self.desired_state = [1,2,3], where index corresponds to x,y,z ...rather than defining self.x_desired_state = 1, self.y_desired_state = 2
CODE MODULARITY AND TECHNIQUES MENTIONED LIKE THIS WILL HELP YOU GAINING MORE MARKS WHILE CODE EVALUATION.	
'''

# Importing the required libraries


from swift_msgs.msg import SwiftMsgs
from geometry_msgs.msg import PoseArray
from controller_msg.msg import PIDTune
from error_msg.msg import Error
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64


class Swift_Pico(Node):
	def __init__(self):
		super().__init__('pico_controller')  # initializing ros node with name pico_controller

		# This corresponds to your current position of drone. This value must be updated in your whycon callback
		# [x,y,z]
		self.current_state = [0.0,0.0,0.0]
		
		# This corresponds to the setpoint you want the drone to reach or hold
		# [x_desired_state, y_desired_state, z_desired_state]
		self.desired_state = [-7.0, 0.0, 20.0]  # whycon marker at the position of the drone given in the scene. Make the whycon marker associated with position_to_hold drone renderable and make changes accordingly

		# Declaring a cmd of message type swift_msgs and initializing values
		self.cmd = SwiftMsgs()
		self.cmd.rc_roll = 0
		self.cmd.rc_pitch = 0
		self.cmd.rc_yaw = 0
		self.cmd.rc_throttle = 1100

		#initial setting of Kp, Kd and ki for [roll, pitch, throttle]. eg: self.Kp[2] corresponds to Kp value in throttle axis
		#after tuning and computing corresponding PID parameters, change the parameters

		self.Kp = [0.0, 0.0, 0.0]
		self.Ki = [0.0, 0.0, 0.0]
		self.Kd = [0.0, 0.0, 0.0]

		#-----------------------Add other required variables for pid here ----------------------------------------------

		self.error = [0,0,0]
		self.prev_error = [0,0,0]
		self.Perror = [0,0,0]
		self.Derror = [0,0,0]
		self.sum_error = [0,0,0]
		self.max_values = [2000,2000,2000]
		self.min_values = [1000,1000,1500]

		# Hint : Add variables for storing previous errors in each axis, like self.prev_error = [0,0,0] where corresponds to [pitch, roll, throttle]		#		 Add variables for limiting the values like self.max_values = [2000,2000,2000] corresponding to [roll, pitch, throttle]
		#													self.min_values = [1000,1000,1000] corresponding to [pitch, roll, throttle]
		#																	You can change the upper limit and lower limit accordingly. 
		#----------------------------------------------------------------------------------------------------------

		# # This is the sample time in which you need to run pid. Choose any time which you seem fit.
	
		self.sample_time = 0.033  # in seconds
		
		# Publishing /drone_command, /pid_error
		self.command_pub = self.create_publisher(SwiftMsgs, '/drone_command', 10)
		self.pos_error_pub = self.create_publisher(Error, '/pos_error', 10)

		#------------------------Add other ROS 2 Publishers here-----------------------------------------------------
		self.roll_error_pub = self.create_publisher(Error, '/roll_error', 10)
		self.pitch_error_pub = self.create_publisher(Error, '/pitch_error', 10)
		self.throttle_error_pub = self.create_publisher(Error, '/alt_error', 10)

		# Subscribing to /whycon/poses, /throttle_pid, /pitch_pid, roll_pid
		self.create_subscription(PoseArray, '/whycon/poses', self.whycon_callback, 1)
		self.create_subscription(PIDTune, "/throttle_pid", self.altitude_set_pid, 1)

		#------------------------Add other ROS Subscribers here-----------------------------------------------------
		self.create_subscription(PIDTune,"/pitch_pid",self.pitch_pid,1)
		self.create_subscription(PIDTune,"/roll_pid",self.roll_pid,1)
		self.arm()  # ARMING THE DRONE

		# Creating a timer to run the pid function periodically, refer ROS 2 tutorials on how to create a publisher subscriber(Python)
		self.timer = self.create_timer(self.sample_time, self.pid)

	def disarm(self):
		self.cmd.rc_roll = 1000
		self.cmd.rc_yaw = 1000
		self.cmd.rc_pitch = 1000
		self.cmd.rc_throttle = 1000
		self.cmd.rc_aux4 = 1000
		self.command_pub.publish(self.cmd)
		

	def arm(self):
		self.disarm()
		self.cmd.rc_roll = 1500
		self.cmd.rc_yaw = 1500
		self.cmd.rc_pitch = 1500
		self.cmd.rc_throttle = 1500
		self.cmd.rc_aux4 = 2000
		self.command_pub.publish(self.cmd)  # Publishing /drone_command


	# Whycon callback function
	# The function gets executed each time when /whycon node publishes /whycon/poses 
	def whycon_callback(self, msg):
		self.current_state[0] = msg.poses[0].position.x 
		#--------------------Set the remaining co-ordinates of the drone from msg----------------------------------------------
		self.current_state[1] = msg.poses[0].position.y
		self.current_state[2] = msg.poses[0].position.z
		#---------------------------------------------------------------------------------------------------------------

	# Callback function for /throttle_pid
	# This function gets executed each time when /drone_pid_tuner publishes /throttle_pid
	def altitude_set_pid(self, alt):
		self.Kp[2] = alt.kp * 0.03  # This is just for an example. You can change the ratio/fraction value accordingly
		self.Ki[2] = alt.ki * 0.008
		self.Kd[2] = alt.kd * 0.6		

	#----------------------------Define callback function like altitide_set_pid to tune pitch, roll--------------
	def pitch_pid(self, alt):
		self.Kp[1] = alt.kp * 0.03  # This is just for an example. You can change the ratio/fraction value accordingly
		self.Ki[1] = alt.ki * 0.008
		self.Kd[1] = alt.kd * 0.6
		
	def roll_pid(self, alt):
		self.Kp[0] = alt.kp * 0.03  # This is just for an example. You can change the ratio/fraction value accordingly
		self.Ki[0] = alt.ki * 0.008
		self.Kd[0] = alt.kd * 0.6
	#----------------------------------------------------------------------------------------------------------------------


	def pid(self):
	#-----------------------------Write the PID algorithm here--------------------------------------------------------------

	# Steps:
	# 	1. Compute error in each axis. eg: error[0] = self.current_state[0] - self.desired_state[0] ,where error[0] corresponds to error in x...
		self.error[0] = self.current_state[0] - self.desired_state[0]
		self.error[1] = self.current_state[1] - self.desired_state[1]
		self.error[2] = self.current_state[2] - self.desired_state[2]
	#	2. Compute the error (for proportional), change in error (for derivative) and sum of errors (for integral) in each axis. Refer "Understanding PID.pdf" to understand PID equation.
		self.Perror[0] = self.error[0]
		self.Perror[1] = self.error[1]
		self.Perror[2] = self.error[2]
		
		self.Derror[0] = (self.error[0] - self.prev_error[0])/self.sample_time
		self.Derror[1] = (self.error[1] - self.prev_error[1])/self.sample_time
		self.Derror[2] = (self.error[2] - self.prev_error[2])/self.sample_time
		
		#self.sum_error[0] += self.error[0]*self.sample_time
		#self.sum_error[1] += self.error[1]*self.sample_time
		#self.sum_error[2] += self.error[2]*self.sample_time
		
	#	3. Calculate the pid output required for each axis. For eg: calcuate self.out_roll, self.out_pitch, etc.
		self.out_roll = (self.Perror[0] * self.Kp[0] + self.sum_error[0]*self.Ki[0] + self.Derror[0] * self.Kd[0])
		self.out_pitch = (self.Perror[1] * self.Kp[1] + self.sum_error[1]*self.Ki[1] + self.Derror[1] * self.Kd[1])
		self.out_throttle = (self.Perror[2] * self.Kp[2] + self.sum_error[2]*self.Ki[2] + self.Derror[2] * self.Kd[2])
		
	#	4. Reduce or add this computed output value on the avg value ie 1500. For eg: self.cmd.rcRoll = 1500 + self.out_roll. LOOK OUT FOR SIGN (+ or -). EXPERIMENT AND FIND THE CORRECT SIGN
		self.cmd.rc_roll = int(1500 + self.out_roll)
		self.cmd.rc_pitch = int(1500 + self.out_pitch)
		self.cmd.rc_throttle = int(1500 + self.out_throttle)
			
	#	5. Don't run the pid continously. Run the pid only at the a sample time. self.sampletime defined above is for this purpose. THIS IS VERY IMPORTANT.
		
	#	6. Limit the output value and the final command value between the maximum(2000) and minimum(1000)range before publishing. For eg : if self.cmd.rcPitch > self.max_values[1]:
	#																														self.cmd.rcPitch = self.max_values[1]
		if self.cmd.rc_roll > self.max_values[0]:
			self.cmd.rc_roll = self.max_values[0]
		if self.cmd.rc_pitch > self.max_values[1]:
			self.cmd.rc_pitch = self.max_values[1]
		if self.cmd.rc_throttle > self.max_values[2]:
			self.cmd.rc_throttle = self.max_values[2]
			
		if self.cmd.rc_roll < self.min_values[0]:
			self.cmd.rc_roll = self.min_values[0]
		if self.cmd.rc_pitch < self.min_values[1]:
			self.cmd.rc_pitch = self.min_values[1]
		if self.cmd.rc_throttle < self.min_values[2]:
			self.cmd.rc_throttle = self.min_values[2]
			
	#	7. Update previous errors.eg: self.prev_error[1] = error[1] where index 1 corresponds to that of pitch (eg)
		self.prev_error[0] = self.error[0]
		self.prev_error[1] = self.error[1]
		self.prev_error[2] = self.error[2]
		
	#	8. Add error_sum
		self.sum_error[0] += self.error[0] * self.sample_time
		self.sum_error[1] += self.error[1] * self.sample_time
		self.sum_error[2] += self.error[2] * self.sample_time
		
	#------------------------------------------------------------------------------------------------------------------------
		self.command_pub.publish(self.cmd)
		# calculate throttle error, pitch error and roll error, then publish it accordingly
		roll_err_msg = Error()
		roll_err_msg.roll_error = self.error[0]
		self.roll_error_pub.publish(roll_err_msg)

		# Create and publish Pitch Error
		pitch_err_msg = Error()
		pitch_err_msg.pitch_error = self.error[1]
		self.pitch_error_pub.publish(pitch_err_msg)

		# Create and publish Throttle Error (Altitude Error)
		throttle_err_msg = Error()
		throttle_err_msg.throttle_error = self.error[2]
		self.throttle_error_pub.publish(throttle_err_msg)



def main(args=None):
	rclpy.init(args=args)
	swift_pico = Swift_Pico()
 
	try:
		rclpy.spin(swift_pico)
	except KeyboardInterrupt:
		swift_pico.get_logger().info('KeyboardInterrupt, shutting down.\n')
	finally:
		swift_pico.destroy_node()
		rclpy.shutdown()


if __name__ == '__main__':
	main()
