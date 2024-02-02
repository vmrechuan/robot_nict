from aux import *
from db_manager import *

def update_last_status(robot_name):
    update_telemetry = pop_robot_status_database(robot_name)
    previous_json = get_robot_status_file()
    #index = find_id_position_in_list(previous_json["robots"],robot_name,"id")
    if update_telemetry == previous_json["robots"][robot_name]["telemetry"]:
    #if  sub_timestamps(timestamp_now(),previous_json["robots"][robot_name]["telemetry"]["timestamp"]) > 2:
        previous_json["robots"][robot_name]["connected"] = False
    else:
        previous_json["robots"][robot_name]["connected"] = True
        previous_json["robots"][robot_name]["telemetry"] = update_telemetry
    edit_robot_status_file(previous_json)
    return 

def get_last_position(robot_name):
    db = get_robot_status_file()
    #index = find_id_position_in_list(db["robots"],robot_name,"id")
    return db["robots"][robot_name]["telemetry"]["pose_x"],db["robots"][robot_name]["telemetry"]["pose_y"],db["robots"][robot_name]["telemetry"]["pose_t"]

def get_last_speed(robot_name):
    db = get_robot_status_file()
    #index = find_id_position_in_list(db["robots"],robot_name,"id")
    return db["robots"][robot_name]["telemetry"]["speed"]

def get_last_battery_status(robot_name):
    db = get_robot_status_file()
    #index = find_id_position_in_list(db["robots"],robot_name,"id")
    return db["robots"][robot_name]["telemetry"]["battery_level"],db["robots"][robot_name]["telemetry"]["charging_status"]

def get_broker_from_robot_name(robot_name):
    conf = get_config()
    #index = find_id_position_in_list(conf['brokers'],robot_name,"id")
    return conf['brokers'][robot_name]["router"]["host"]

def get_ip_from_robot_name(robot_name):
    conf = get_config()
    #index = find_id_position_in_list(conf['brokers'],robot_name,"id")
    return conf['brokers'][robot_name]["robot"]["host"]

# to be reviewd
def get_connected_robots():
    connected_robots = []
    db = get_robot_status_file()
    for robot in db["robots"].keys():
        if robot["connected"]:
            connected_robots.append(robot)
    return connected_robots

def get_robot_status(robot_name):
    db = get_robot_status_file()
    return db["robots"][robot_name]["connected"]

def get_ip_from_robot_list(connected_robots):
    ips = []
    config = get_config()
    for robot in connected_robots:
        ips.append(config["brokers"][robot])
    return ips
