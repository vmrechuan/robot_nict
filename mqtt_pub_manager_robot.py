from connect_mqtt import *
from db_manager_map import *
from db_manager_robot import *
import json 

def publisher(robot_name,topic = "/frutera/request",client_name = "request_robot", payload=""):
    broker_address = get_broker_from_robot_name(robot_name)
    if not get_robot_status(robot_name):
        print("Robot Disconnected----"+robot_name)
        return
    #print(broker_address)
    payload["from"] = client_name
    publish_mqtt = new_mqtt_client(client_name=client_name,broker_address=broker_address)
    publish_mqtt.publish(topic,json.dumps(payload),qos=0,retain=False)

def publisher_set_restrict_layers(robot_name, waypoints,request="restrict_layer"):
    broker_address = get_ip_from_robot_name(robot_name)
    if not get_robot_status(robot_name):
        print("Robot Disconnected----"+robot_name)
        return
    return api_post_robot('http://'+broker_address+'/cmd/'+request,waypoints)

def publisher_set_special_polygons(robot_name, polygons,request="special_polygon"):
    broker_address = get_ip_from_robot_name(robot_name)
    if not get_robot_status(robot_name):
        print("Robot Disconnected----"+robot_name)
        return
    return api_post_robot('http://'+broker_address+'/cmd/'+request,polygons)

### Get all landmarkin the map database and apply it
def add_point(map_id,point_name,x,y,t):
    return {"command":"add","id":map_id,"name":point_name,"x":x,"y":y,"t":t,"type":"NORMAL"}

def to_point(point_name):
    return {"point_name":point_name}

def get_robot_request_base(robot_name, request, client_name=""):
    return {
    "type":"request",
    "request":request,
    "from":client_name,
    "to":robot_name,
    "time":timestamp_now()
}

def publisher_reset_points(robot_name, request="set_point_info"):
    map_id = get_current_map_id()
    payload = get_landmarks(map_id)
    for point in payload:
        payload = get_robot_request_base(robot_name, request)
        payload["data"] = add_point(map_id,point["name"],point["pose"]["x"],point["pose"]["y"],point["pose"]["t"])
        publisher(robot_name,payload=payload)
                    
### Get position and define as new Ladmark
def publish_new_point_info(robot_name,point_name, request="set_point_info"):
    map_id = get_current_map_id()
    x,y,t = get_last_position(robot_name)
    payload = get_robot_request_base(robot_name, request)
    payload["data"] = add_point(map_id,point_name,x,y,t)

    new_landmark = landmark(point_name, x, y, t)
    add_landmark(map_id, new_landmark)
    publisher(robot_name,payload=payload)
    return

def reloc_from_point(robot_name,request="reloc"):
    map_id,landmak_name = get_reloc_landmak_name()
    payload = get_robot_request_base(robot_name, request)
    payload["data"] = get_landmark_position(map_id,landmak_name)
    publisher(robot_name,payload=payload)
    return 

def move_to_landmark(robot_name,landmark_name,request="move"):
    payload = get_robot_request_base(robot_name, request)
    payload["data"] = to_point(landmark_name)
    publisher(robot_name,payload=payload)
    return 

def reset_map_config(robots): # robots should be in array
    map_id = get_current_map_id()
    #robots = get_connected_robots()
    waypoints = get_virtual_wall(map_id)
    polygons = get_special_regions(map_id)
    for robot in robots:
        publisher_reset_points(robot)
        publisher_set_restrict_layers(robot, waypoints)
        publisher_set_special_polygons(robot, polygons)
    return 
