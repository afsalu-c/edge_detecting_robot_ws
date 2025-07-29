#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import TwistStamped
from geometry_msgs.msg import Twist
# from time import sleep
from std_msgs.msg import Header

class EdgeAvoidanceBot(Node):
    def __init__(self):
        super().__init__('edge_avoidance_bot')
        
        self.cmd_vel_pub_ = self.create_publisher(Twist, '/wheel_controller/cmd_vel', 10)
        self.timer_ = self.create_timer(0.1, self.control_loop)
        self.laser_scan_sub_ = self.create_subscription(LaserScan, '/scan', self.lidar_callback, 10)

        # self.cmd_vel_ = TwistStamped()
        self.cmd_vel_ = Twist()
        self.flag = False

        self.up = 0.0
        self.down = 0.0

        #ed

    def control_loop(self):
        # Default forward motion
        self.cmd_vel_.linear.x = 0.3
        self.cmd_vel_.angular.z = 0.0
        # self.cmd_vel_.header.stamp.sec = 0
        # self.cmd_vel_.header.stamp.nanosec = 0
        # self.cmd_vel_.header.frame_id = 'base_link'
        # self.cmd_vel_.twist.linear.x = 0.3
        # self.cmd_vel_.twist.angular.z = 0.0

        #Edge detection
        if self.down > 0.50:
            self.flag = True #Edge detected
        
        if self.flag == True > 0.60:
            # self.cmd_vel_.twist.linear.x = -0.4
            # self.cmd_vel_.twist.angular.z = -1.65
            self.cmd_vel_.linear.x = -0.4
            self.cmd_vel_.angular.z = -1.65
            self.get_logger().info("Edge ahead! Reversing and Turning.")
        else:
            self.flag = False
        
        self.cmd_vel_pub_.publish(self.cmd_vel_)

    def lidar_callback(self, msg):
        # Extract ranges
        ranges = msg.ranges
        valid_ranges = [r if r > 0.05 and r < 4.0 else 4.0 for r in ranges]

        self.up = valid_ranges[6]
        self.down = valid_ranges[2]
        #print(len(valid_ranges))

        # Log the regions
        self.get_logger().info(f"Distances - U: {self.up:.2f}, - D: {self.down:.2f}")


def main(args=None):
    rclpy.init(args=args)
    bot = EdgeAvoidanceBot()
    rclpy.spin(bot)
    rclpy.shutdown()

if __name__ == '__main__':
    main()