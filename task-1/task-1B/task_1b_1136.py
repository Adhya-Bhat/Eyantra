import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from rclpy.task import Future
from turtlesim.srv import SetPen, TeleportAbsolute
from rclpy.qos import QoSProfile

class DroneDraw(Node):
    
    def __init__(self):

        super().__init__("DrawCommandNode")

        qos_profile = QoSProfile(depth = 10)

        self.pen_client = self.create_client(SetPen,'/turtle1/set_pen', qos_profile=qos_profile)
        self.teleport_client = self.create_client(TeleportAbsolute, '/turtle1/teleport_absolute', qos_profile=qos_profile)
        self.publishCircle = self.create_publisher(Twist,'/turtle1/cmd_vel',10)

        self.i = 0

        self.timer_state = True

        self.timer_period = 0.1
        
        self.circleNumber = 0

        self.circle1Future = Future()
        self.circle2Future = Future()
        self.circle3Future = Future()
        self.circle4Future = Future()
        

    def setPenState(self,offVal):
        req = SetPen.Request()
        req.r = 255
        req.g = 255
        req.b = 255
        req.width = 3
        req.off = offVal

        self.futurePenState = self.pen_client.call_async(req)
        rclpy.spin_until_future_complete(self,self.futurePenState)
    
    def setTeleportPoint(self, xTele, yTele, theta):
        req = TeleportAbsolute.Request()
        req.x = xTele
        req.y = yTele
        req.theta = theta
        
        self.futureTeleport = self.teleport_client.call_async(req)
        rclpy.spin_until_future_complete(self,self.futureTeleport)
    
    def circle1Ini(self):
        self.timer = self.create_timer(self.timer_period,self.drawCircle)

        rclpy.spin_until_future_complete(self, self.circle1Future)
    
    def circle2Ini(self):
        self.timer = self.create_timer(self.timer_period,self.drawCircle)

        rclpy.spin_until_future_complete(self, self.circle2Future)
    
    def circle3Ini(self):
        self.timer = self.create_timer(self.timer_period,self.drawCircle)

        rclpy.spin_until_future_complete(self, self.circle3Future)
    
    def circle4Ini(self):
        self.timer = self.create_timer(self.timer_period,self.drawCircle)

        rclpy.spin_until_future_complete(self, self.circle4Future)

    def rectangle(self):

        self.setPenState(1)
        self.setTeleportPoint(5.0,3.0,0.0)
        self.get_logger().info('Frame Initial Point Initialized')
        self.setPenState(0)
        self.setTeleportPoint(3.0,5.0,0.0)
        self.get_logger().info('Side 1 Done')
        self.setTeleportPoint(5.0,7.0,0.0)
        self.get_logger().info('Side 2 Done')
        self.setTeleportPoint(7.0,5.0,0.0)
        self.get_logger().info('Side 3 Done')
        self.setTeleportPoint(5.0,3.0,0.0)
        self.get_logger().info('Side 4 Done')
        self.setPenState(1)
        self.get_logger().info('Drone Frame Drawing Done')
    
    def connectorLines(self):

        self.setPenState(1)
        self.setTeleportPoint(4.0,4.0,0.0)
        self.setPenState(0)
        self.setTeleportPoint(2.0,2.0,0.0)
        self.get_logger().info('Connector 1 Done')
        
        self.setPenState(1)
        self.setTeleportPoint(4.0,6.0,0.0)
        self.setPenState(0)
        self.setTeleportPoint(2.0,8.0,0.0)
        self.get_logger().info('Connector 2 Done')

        self.setPenState(1)
        self.setTeleportPoint(6.0,6.0,0.0)
        self.setPenState(0)
        self.setTeleportPoint(8.0,8.0,0.0)
        self.get_logger().info('Connector 3 Done')

        self.setPenState(1)
        self.setTeleportPoint(6.0,4.0,0.0)
        self.setPenState(0)
        self.setTeleportPoint(8.0,2.0,0.0)
        self.get_logger().info('Connector 4 Done')

    def centreDrone(self):
        self.setPenState(1)
        self.setTeleportPoint(5.0,5.0,0.0)
        self.get_logger().info('The turtle is now at the centre')

    def drawCircle(self):
        self.i += self.timer_period

        twist = Twist()

        if self.i > 0.7:
            if self.timer_state:
                self.boolVal = self.destroy_timer(self.timer)
                if self.boolVal:
                    self.timer_state = False

            twist.linear.x = 0.0
            twist.linear.y = 0.0
            twist.linear.z = 0.0

            twist.angular.x = 0.0
            twist.angular.y = 0.0
            twist.angular.z = 0.0

            self.publishCircle.publish(twist)

            self.get_logger().info('Stopped Drawing Circle')
            
            self.i = 0
            self.timer_state = True

            if self.circleNumber == 0:
                self.circle1Future.set_result("successful")
                self.get_logger().info('Circle 1 complete')
                self.circleNumber += 1
           
            elif self.circleNumber == 1:
                self.circle2Future.set_result("successful")
                self.get_logger().info('Circle 2 complete')
                self.circleNumber += 1
            
            elif self.circleNumber == 2:
                self.circle3Future.set_result("successful")
                self.get_logger().info('Circle 3 complete')
                self.circleNumber += 1
            
            elif self.circleNumber == 3:
                self.circle4Future.set_result("successful")
                self.get_logger().info('Circle 4 complete')
                self.circleNumber += 1
            
            else:
                self.get_logger().info('Error')

        else:

            twist.linear.x = 10.0
            twist.linear.y = 0.0
            twist.linear.z = 0.0

            twist.angular.x = 0.0
            twist.angular.y = 0.0
            twist.angular.z = 10.0

            self.publishCircle.publish(twist)
            self.get_logger().info('Started Drawing Circle')



def main(args=None):
    rclpy.init(args=args)
    DrawCommandNode = DroneDraw()
    
    DrawCommandNode.setPenState(1)
    DrawCommandNode.setTeleportPoint(2.0,1.0,0.0)
    DrawCommandNode.setPenState(0)
    DrawCommandNode.circle1Ini()

    DrawCommandNode.setPenState(1)
    DrawCommandNode.setTeleportPoint(2.0,7.0,0.0)
    DrawCommandNode.setPenState(0)
    DrawCommandNode.circle2Ini()
    
    DrawCommandNode.setPenState(1)
    DrawCommandNode.setTeleportPoint(8.0,7.0,0.0)
    DrawCommandNode.setPenState(0)
    DrawCommandNode.circle3Ini()

    DrawCommandNode.setPenState(1)
    DrawCommandNode.setTeleportPoint(8.0,1.0,0.0)
    DrawCommandNode.setPenState(0)
    DrawCommandNode.circle4Ini()
    
    DrawCommandNode.rectangle()

    DrawCommandNode.connectorLines()

    DrawCommandNode.centreDrone()

    rclpy.shutdown()

if __name__ == '__main__':
    main()


