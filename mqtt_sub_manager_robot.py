from connect_mqtt import *
from db_manager_map import *
from db_manager_robot import *
import json

def on_message_robot(client, userdata, message):
    topic_name = message.topic
    payload = json.loads(message.payload.decode("utf-8"))
    if topic_name == "/frutera/notify":
        if payload["notify"] == "status":
            add_robot_status_database(payload['from'],
                                      telemetry(
                                            payload['robot_status']['pose']["x"],
                                            payload['robot_status']['pose']["y"],    
                                            payload['robot_status']['pose']["t"],
                                            payload['robot_status']['battery']['level'],
                                            payload['robot_status']['battery']['charge'],
                                            payload['robot_status']['map']['id'],
                                            payload['time']
                                        )
                                    )
            return
    if topic_name == "/frutera/response":
        with open("robot/databases/status.txt", "a+") as file:
            file.write(json.dumps(payload)+"\n")
        return
    #if topic_name == "/frutera/stream":
    #    with open("robot/databases/status.csv", "a+") as file:
    #        file.write(json.dumps(payload)+";\n")
    #    return
    return

def publisher_request_restrict_layers(robot_name,request="restrict_layer"):
    broker_address = get_ip_from_robot_name(robot_name)
    return api_get_robot('http://'+broker_address+'/reeman/'+request)

def publisher_request_special_polygons(robot_name,request="special_polygon"):
    broker_address = get_ip_from_robot_name(robot_name)
    return api_get_robot('http://'+broker_address+'/reeman/'+request)

##########################################
########################################## TELEMETRY STRUCTURE
##########################################

def telemetry(pose_x,pose_y,pose_t,battery_level,charging_status,map_id,timestamp):
    return {
        "pose_x":pose_x,
        "pose_y":pose_y,
        "pose_t":pose_t,
        "battery_level":battery_level,
        "charging_status":charging_status,
        "map_id": map_id,
        "timestamp":timestamp
    }

def connection_event(robot_id,event_type,timestamp):
    return {"event_type":event_type,"timestamp":timestamp}

"""     if topic_name == "/frutera/response":
        try:
            if payload["type"] == "notify":
            manage_notify(payload)
        except:
            return """

##########################################
########################################## TELEMETRY COMMANDS
##########################################


def post_telemenetry(robot_name,pose_x,pose_y,pose_t,battery_level,charging_status,map_id,timestamp):
    db = get_database()
    #robot_index = find_id_position_in_list(db["robots"],robot_name,"id")
    db['robots'][robot_name]['telemetry'].insert(0,telemetry(pose_x,pose_y,pose_t,battery_level,charging_status,map_id,timestamp))
    edit_database(db)
    return

def add_connection_status(robot_name,timestamp,connection):
    db = get_database()
    #robot_index = find_id_position_in_list(db['robots'],robot_name,"id")
    db['robots'][robot_name]["connected"] = True
    db['robots'][robot_name]["events"].insert(0,connection_event(timestamp,timestamp_now()))
    edit_database(db)
    return 