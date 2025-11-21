import rclpy                    # import the ROS Client Library for Python (RCLPY)
from rclpy.node import Node     # from RCLPY, import the Node Class used to create ROS 2 nodes
from std_msgs.msg import String # from standard messages, import the String message

# import os
# include_dir = os.path.dirname(os.path.realpath(__file__)) + "/../../../../../../src/include/"
# import sys
# sys.path.append(include_dir)
# from hat_library import *

# import RPi.GPIO as GPIO

include_path = '/home/rpi/git/sensor-node-Trey-mckenna/src/include'
import sys
sys.path.append(include_path)

import hat_library
from hat_library import *
import RPi.GPIO as GPIO


class SensorNode(Node):   # Create a new class called MinimalPublisher that inherits variables & functions from Node

    def __init__(self):
        super().__init__('sensor_node')                               # Initialize the Node with the name 'minimal_publisher'
        self.publisher_ = self.create_publisher(String, 'ir_data', 10)     # Create a publisher for String type messages on the topic 'my_topic'
        self.declare_parameter('sensor_data', 0)                           # Creates a parameter for sensor_input
        self.declare_parameter('publish_rate', 1)                          # Creates a parameter for publish_rate

        publish_rate = self.get_parameter('publish_rate').value            # Reads the publish rate value and assigns to a variable

        self.timer = self.create_timer(publish_rate, self.timer_callback)   # Create a timer that calls 'timer_callback' every 0.5 seconds


    def timer_callback(self):
        sensor_param = self.get_parameter('sensor_data').value

        if sensor_param == 1:
            ir1Value = get_ir_state(IR1_INPUT_PIN)
            if(ir1Value == LIGHT):
                msg = String()                                          # Create a new String message
                msg.data = 'LIGHT'                                        # Assign text to msg.data
                self.publisher_.publish(msg)                            # Publish the message to the topic
                self.get_logger().info('Publishing: "%s"' % msg.data)   # Log the published message for debugging  
            elif(ir1Value == DARK):
                msg = String()
                msg.data = 'DARK'                                     # Assign text to msg.data
                self.publisher_.publish(msg)                            # Publish the message to the topic
                self.get_logger().info('Publishing: "%s"' % msg.data)   # Log the published message for debugging    
            elif(ir1Value == INVALID):
                msg.data = str(ir1Value)
                self.get_logger().info('Invalid input recieved, not publishing irvalue: "{msg.data}"')   # Log the published message for debugging         
        elif sensor_param == 2:
            ir2Value = get_ir_state(IR2_INPUT_PIN)
            if(ir2Value == LIGHT):
                msg = String()                                          # Create a new String message
                msg.data = 'LIGHT'                                        # Assign text to msg.data
                self.publisher_.publish(msg)                            # Publish the message to the topic
                self.get_logger().info('Publishing: "%s"' % msg.data)   # Log the published message for debugging  
            elif(ir2Value == DARK):
                msg = String()
                msg.data = 'DARK'                                     # Assign text to msg.data
                self.publisher_.publish(msg)                            # Publish the message to the topic
                self.get_logger().info('Publishing: "%s"' % msg.data)   # Log the published message for debugging    
            elif(ir2Value == INVALID):
                msg = String()
                msg.data = str(ir1Value)
                self.get_logger().info('Invalid input recieved, not publishing irvalue: "{msg.data}"')   # Log the published message for debugging 
        else:
            self.get_logger().info('invalid parameter recieved')


            
def main(args=None):
    print ("Beginning to talk...")          # Print a starting message
    rclpy.init(args=args)                   # Initialize the ROS 2 Python client library

    sensor_node = SensorNode()  # Create an instance of the MinimalPublisher class

    try:
        rclpy.spin(sensor_node)       # Keep the node active and processing callbacks until interrupted

    except KeyboardInterrupt:   # Handle a keyboard interrupt (Ctrl+C)
        print("\n")             # Print a newline for better format
        print("Stopping...")    # Print a stopping message
 
    finally:
        # Destroy the node explicitly
        # (optional - otherwise it will be done automatically
        # when the garbage collector destroys the node object)
        sensor_node.destroy_node()
        if rclpy.ok():                      # Check if the rclpy library is still running
            rclpy.shutdown()                # Shut down the ROS 2 client library, cleanly terminating the node



if __name__ == '__main__':
    main()                  # Call the main function to execute the code when the script is run