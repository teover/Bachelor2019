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
import numpy as np
import sys
import mir_interface as mir
import config as c # Config file used for parameters

# Safety check if waypoints are within -2pi to 2pi
wp = np.array([c.wp_camscan_pos, c.wp_approach_pickup, c.wp_pickup, c.wp_approach_place, c.wp_place1], np.float)
for row in wp:
  for column in row:
    if(column > 2*np.pi or column < -2*np.pi):
        rospy.logfatal('Waypoints contains values larger 2pi or smaller than -2pi: ' + str(column)))
        sys.exit()
def main():
    global client
    try:
        rospy.init_node("ur5pickandplace", disable_signals=True) # Initialize ROS node
        client = actionlib.SimpleActionClient('follow_joint_trajectory', FollowJointTrajectoryAction)
        rospy.loginfo("Waiting for server...")
        client.wait_for_server()
        rospy.loginfo("Connected to server")

        #Check MiR200 battery
        battery = mir.checkMiRBattery()
        rospy.loginfo("MiR200 Battery percentage: " + str(battery))

        # Pickup counter
        counter = 1
        counter_tot = 0

        while not rospy.is_shutdown():

            if mir.checkIfAtPosition(c.festo_coords) == False:
                mir.addMissionToQueue(c.go_to_festo)
            # Check MiR200 position
            while mir.checkIfAtPosition(c.festo_coords) == False:
                rospy.loginfo("Waiting for MiR200")
                time.sleep(1)

            rospy.loginfo("Entering camscan position")
            arm.move(c.wp_camscan_pos, c.time_between_wp)
            joint_states = rospy.wait_for_message("joint_states", JointState)

            while(arm.readCamdetectStatus() != True):
                time.sleep(1)
                rospy.loginfo("Waiting for case..")

            rospy.loginfo("Case detected!")

            rospy.loginfo("Enter pickup approach position")
            arm.move(c.wp_approach_pickup, c.time_between_wp)

            rospy.loginfo("Entering pickup position")
            arm.move(c.wp_pickup, c.time_between_wp)

            rospy.loginfo("Turning on vacuum")
            arm.vacCtrl(True, c.portOn, c.portOff)

            counter_tot += 1
            counter += 1

            rospy.loginfo("Enter pickup approach position")
            arm.move(c.wp_approach_pickup, c.time_between_wp)

            rospy.loginfo("Entering approach place position")
            arm.move(c.wp_approach_place, c.time_between_wp)

            # Code for stacking cases. Should be replaced by something better.
            if counter == 1:
                rospy.loginfo("Entering place position 1")
                arm.move(c.wp_place1, c.time_between_wp)
            elif counter == 2:
                rospy.loginfo("Entering place position 2")
                arm.move(c.wp_place2, c.time_between_wp)
            elif counter == 3:
                rospy.loginfo("Entering place position 3")
                arm.move(c.wp_place3, c.time_between_wp)

            rospy.loginfo("Turning off vacuum")
            arm.vacCtrl(False, c.portOn, c.portOff)

            rospy.loginfo("Returning to approach place position")
            arm.move(c.wp_approach_place, c.time_between_wp)


            rospy.loginfo("Cases until delivery to storage: " + (str(c.deliveries_before_go_to_storage - counter)))
            rospy.loginfo("Total cases delivered: " + str(counter_tot))

            if counter >= c.deliveries_before_go_to_storage:
                counter = 0
                mir.addMissionToQueue(c.go_to_storage)
                time.sleep(c.pause_delivery)

	# CTRL+C check
    except KeyboardInterrupt:
        rospy.signal_shutdown("KeyboardInterrupt")
        raise

if __name__ == '__main__': main()
