#!/usr/bin/env python
import roslib; roslib.load_manifest('ur_driver')
import rospy
import actionlib
from control_msgs.msg import *
from trajectory_msgs.msg import *
from sensor_msgs.msg import JointState
import arm_functions as arm
from sensor_msgs.msg import Image
from std_msgs.msg import Bool
import time


def main(): #Here is the main function.
    global client
    try:
        rospy.init_node("test_move", anonymous=True, disable_signals=True) # Initialize ROS node
        client = actionlib.SimpleActionClient('follow_joint_trajectory', FollowJointTrajectoryAction)
        print "Waiting for server..."
        client.wait_for_server()
        print "Connected to server"


        print "Entering camscan position"
        raw_input('Set robot to position, then press enter to continue. ')
        arm.readpos("wp_camscan_pos", 5)

        print "Enter pickup approach position"
        raw_input('Set robot to position, then press enter to continue. ')
        arm.readpos("wp_approach_pickup", 5)

        print "Entering pickup position"
        raw_input('Set robot to position, then press enter to continue. ')
        arm.readpos("wp_pickup", 5)

        print "Entering approach place position"
        raw_input('Set robot to position, then press enter to continue. ')
        arm.readpos("wp_approach_place", 5)

        print "Entering place position"
        raw_input('Set robot to position, then press enter to continue. ')
        arm.readpos("wp_place", 5)


	# CTRL+C check
    except KeyboardInterrupt:
        rospy.signal_shutdown("KeyboardInterrupt")
        raise

if __name__ == '__main__': main()
