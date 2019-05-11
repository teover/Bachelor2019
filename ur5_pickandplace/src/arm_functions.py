import roslib; roslib.load_manifest('ur_driver')
import rospy
import actionlib
from control_msgs.msg import *
from trajectory_msgs.msg import *
from sensor_msgs.msg import JointState
from std_msgs.msg import Bool
import config as c # Config file used for parameters


# Imports SetIO.srv from /ur_msgs/srv/
from ur_msgs.srv import SetIO
from ur_msgs.msg import IOStates


# Joint array definition
JOINT_NAMES = ['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint',
               'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']

# arm.move(waypoint, duration)          - move to waypoint in duration seconds
# arm.readpos()                         - returns postion of arm in radians per joint
# arm.vacCtrl(state, portOn, portOff):  - If state is True, turns portOn high and portOff low,
#                                         if state is False, turns portOn low and portOff high
# arm.readCamdetectStatus()             - reads file object_status in working directory


# Moves to waypoint over duration seconds
def move(waypoint, duration):
    global joints_pos
    g = FollowJointTrajectoryGoal()
    g.trajectory = JointTrajectory()
    g.trajectory.joint_names = JOINT_NAMES
    client = actionlib.SimpleActionClient('follow_joint_trajectory', FollowJointTrajectoryAction)
    try:
		# wait for joint_states to be available
        joint_states = rospy.wait_for_message("joint_states", JointState)
        joints_pos = joint_states.position
        g.trajectory.points = [
            JointTrajectoryPoint(positions=joints_pos, velocities=[0]*6, time_from_start=rospy.Duration(0.0)),
            JointTrajectoryPoint(positions=waypoint, velocities=[0]*6, time_from_start=rospy.Duration(duration)),]
        client.send_goal(g) # execute trajectory goal command
        # debug print "waiting for result"
        client.wait_for_result() # wait for result

    except KeyboardInterrupt:
        client.cancel_goal()
        raise
    except:
        raise

# Prints joint states to command line and log file
def readpos(pos, dura):
    #log = open("joint_pos_log.txt","a+")
    joint_states = rospy.wait_for_message("joint_states", JointState)
    c.pos = joint_states.position
    rospy.loginfo(joint_states.position)
    #log.write(pos + " = " + str(joint_states.position) + "\n")
    #log.close()


SetIO = rospy.ServiceProxy('/ur_driver/set_io', SetIO)

def vacCtrl(state, portOn, portOff):
    if state == True:
        SetIO(1, portOff, 0)
        SetIO(1, portOn, 1)
        rospy.loginfo("Vacuum turned on")
    else:
        SetIO(1, portOff, 1)
        SetIO(1, portOn, 0)
        rospy.loginfo("Vacuum turned off")

def readCamdetectStatus():
    status = rospy.wait_for_message('object_status', Bool)
    return status.data
