#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import TwistStamped
from std_msgs.msg import Header

class EdgeAvoidanceBot(Node):
    def __init__(self):
        super().__init__('edge_avoidance_bot')
        
        self.publisher = self.create_publisher(TwistStamped, '/wheel_controller/cmd_vel', 10)
        self.subscription = self.create_subscription(LaserScan, '/scan', self.lidar_callback, 10)
        self.timer = self.create_timer(0.1, self.control_loop)
        self.cmd_vel = TwistStamped()
        self.cmd_vel.header.frame_id = 'base_link'

        self.up = 0.0
        self.down = 0.0
        self.flag = False

        self.get_logger().info('Edge Avoidance Bot with TwistStamped started.')

    def lidar_callback(self, msg):
        # Extract ranges
        ranges = msg.ranges
        valid_ranges = [r if 0.05 < r < 4.0 else 4.0 for r in ranges]

        self.up = valid_ranges[6]
        self.down = valid_ranges[2]

        self.get_logger().info(f"Distances - U: {self.up:.2f}, D: {self.down:.2f}")

    def control_loop(self):
        self.cmd_vel.header.stamp = self.get_clock().now().to_msg()

        # Default forward motion
        self.cmd_vel.twist.linear.x = 0.4
        self.cmd_vel.twist.angular.z = 0.0

        # Edge Detection Logic
        if self.down > 0.50:
            self.flag = True  # Edge Detected

        if self.flag and self.up > 0.60:
            self.cmd_vel.twist.linear.x = -0.4
            self.cmd_vel.twist.angular.z = -1.65 #-1.65
            self.get_logger().info("Edge ahead! Reversing and turning.")
        else:
            self.flag = False

        # Publish message
        self.publisher.publish(self.cmd_vel)

def main(args=None):
    rclpy.init(args=args)
    node = EdgeAvoidanceBot()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
