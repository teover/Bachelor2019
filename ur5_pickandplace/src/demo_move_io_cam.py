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


# Waypoints for joints, in radians from -2pi to 2pi
wp_camscan_pos = [0.055668491948991025, -0.5564994408951534, -0.08150869494341745, 0.29173569854442066, -1.9691452619485772, -1.9631221663273448]
wp_approach_pickup = [4.165284636099243, 3.967309336139688, 1.063860097506497, 0.6143518686294556, -4.1326398849487305, -10.228209495544434]
wp_pickup = [-2.43530713631358e-18, -20.37429549271156, -26.055663930994044, -4.62443288744048, 0.014444307435431934, 0.0]
wp_approach_place = [-0.5822938124286097, -1.3992627302752894, 1.7505531311035156, -1.9894331137286585, -1.5869553724872034, -0.7160523573504847]
wp_place = [0.0, 0.0, 5.474e-321, 712.928, -0.5822699705706995, -1.3992388884173792]


# IO Ports for vacuum control
port_Succ = 5
port_noSucc = 6



def main(): #Here is the main function.
    global client
    try:
        rospy.init_node("test_move", anonymous=True, disable_signals=True) # Initialize ROS node
        client = actionlib.SimpleActionClient('follow_joint_trajectory', FollowJointTrajectoryAction)
        print "Waiting for server..."
        client.wait_for_server()
        print "Connected to server"

        # Pickup counter
        counter = 0

        while True:
            print "Entering camscan position"
            arm.move(wp_camscan_pos, 10)

            while(arm.readCamdetectStatus() != True):
                time.sleep(1)
                print "Waiting for case.."
                print arm.readCamdetectStatus()

            print "Case detected!"

            print "Enter pickup approach position"
            arm.move(wp_approach_pickup, 10)

            print "Entering pickup position"
            arm.move(wp_pickup, 5)

            print "Turning on vacuum"
            arm.vacOn(port_Succ, port_noSucc)

            print "Entering approach place position"
            arm.move(wp_approach_place, 10)

            print "Entering place position"
            arm.move(wp_place, 5)

            print "Turning off vacuum"

            counter += 1
            print "Cases delivered: " + str(counter)

            arm.vacOff(port_Succ, port_noSucc)



	# CTRL+C check
    except KeyboardInterrupt:
        rospy.signal_shutdown("KeyboardInterrupt")
        raise

if __name__ == '__main__': main()
