
import requests
import json
import config as c # Config file used for parameters

# Check battery status
def checkMiRBattery():
    r = requests.get(c.url_get_status, headers=c.headers).json()
    return r["battery_percentage"]

# Check if robot is at a position, input position is a dict with x and y
def checkIfAtPosition(position):
    r = requests.get(c.url_get_status, headers=c.headers).json()
    mir_pos_x = r["position"]["x"]
    mir_pos_y = r["position"]["y"]
    # Treshold for accepting the postion in meters
    t = c.threshold

    if (position["x"]-t < mir_pos_x < position["x"]+t and position["y"]-t < mir_pos_y < position["y"]+t):
        return True
    else:
        return False

# takes input string mission, mission is a mission
def addMissionToQueue(mission):
    r = requests.post(c.url_mission_queue, data=json.dumps(mission), headers=c.headers)
    if r.status_code == 201:
        return True
    else:
        print "Error: " + str(r.status_code)
        return False
