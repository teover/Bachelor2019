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

wp_camscan_pos = (1.268944501876831, -2.019967857991354, 1.3162450790405273, -1.1526301542865198, -1.516102139149801, -0.8196757475482386)
wp_approach_pickup = (1.3299074172973633, -1.307413403187887, 0.5601739883422852, -0.879674259816305, -1.5992415587054651, -0.7849109808551233)
wp_pickup = (1.3298715353012085, -1.4950774351703089, 1.1284489631652832, -1.260418717061178, -1.5990617910968226, -0.7855103651629847)
wp_approach_place = (4.440732955932617, -1.2501304785357874, 0.7147054672241211, -1.0875228087054651, -1.613842789326803, -0.6822336355792444)
wp_place1 = (4.472695350646973, -0.676950756703512, 1.707146167755127, -2.651966396962301, -1.6194575468646448, -0.6523321310626429)
wp_place2 = (4.472695350646973, -0.676950756703512, 1.707146167755127, -2.651966396962301, -1.6194575468646448, -0.6523321310626429)
wp_place3 = (4.472695350646973, -0.676950756703512, 1.707146167755127, -2.651966396962301, -1.6194575468646448, -0.6523321310626429)


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
        arm.readpos("wp_place1", 5)

        print "Entering place position"
        raw_input('Set robot to position, then press enter to continue. ')
        arm.readpos("wp_place2", 5)

        print "Entering place position"
        raw_input('Set robot to position, then press enter to continue. ')
        arm.readpos("wp_place3", 5)


	# CTRL+C check
    except KeyboardInterrupt:
        rospy.signal_shutdown("KeyboardInterrupt")
        raise

if __name__ == '__main__': main()
