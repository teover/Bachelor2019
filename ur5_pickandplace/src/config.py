
###################
### UR5 Config ####
###################

# Default time between waypoints
time_between_wp = 5


# IO Ports for vacuum control
portOn = 4
portOff = 5


# Waypoints for joints, in radians from -2pi to 2pi. Use read_positions.py to aquire. Joints will be in joint_pos_log.txt

wp_camscan_pos = (1.239990234375, -1.9598611036883753, 1.1943764686584473, -1.174025837575094, -1.4531014601336878, -1.0338519255267542)
wp_approach_pickup = (1.3435384035110474, -1.5038569609271448, 0.831939697265625, -1.0730202833758753, -1.5369332472430628, -2.9068904558764856)
wp_pickup = (1.3439817428588867, -1.6583827177630823, 1.3403606414794922, -1.4269002119647425, -1.5368369261371058, -2.906938378010885)
wp_approach_place = (4.536683082580566, -1.09007436433901, 1.0197811126708984, -1.4896839300738733, -1.569953743611471, -2.906123940144674)
wp_place1 = (4.53765344619751, -0.6305869261371058, 1.528613567352295, -2.4578426519977015, -1.572869602833883, -2.906794611607687)
wp_place2 = (4.5375213623046875, -0.6575730482684534, 1.5328874588012695, -2.435272518788473, -1.5726173559771937, -2.906699244176046)
wp_place3 = (4.537581443786621, -0.6966517607318323, 1.536874771118164, -2.4000070730792444, -1.57253343263735, -2.906675163899557)

# Time to wait when cases are delivered
pause_delivery = 5

#####################
### MiR200 Config ###
#####################

# Coordinates for festo lab on mir map, used for position checking
deliveries_before_go_to_storage = 3

# MiR200 position treshold
threshold = 0.1

festo_coords = {
    "x": 13.8,
    "y": 9.45
}

# Coordinates for storage on mir map
storage_coords = {
    "x": 15.9,
    "y": 18.85
}

# Festo mission ID for MiR200
go_to_festo = {
    "mission_id": "18c6b8a4-6747-11e9-baa0-94c69118fd1e",
    "message": "Go to festo",
    "parameters": [],
    "priority": 0
}

# Storage mission ID
go_to_storage = {
    "mission_id": "71a734fa-674c-11e9-baa0-94c69118fd1e",
    "message": "Go to storage",
    "parameters": [],
    "priority": 0
}

# API URL
url_mission_queue = "http://mir.com/api/v2.0.0/mission_queue"
url_get_status = "http://mir.com/api/v2.0.0/status"


headers = {
        'accept': 'application/json',
        'Authorization': 'Basic ZGlzdHJpYnV0b3I6NjJmMmYwZjFlZmYxMGQzMTUyYzk1ZjZmMDU5NjU3NmU0ODJiYjhlNDQ4MDY0MzNmNGNmOTI5NzkyODM0YjAxNA==',
        'Accept-Language': 'en_US',
        'Content-Type': 'application/json'
        }
