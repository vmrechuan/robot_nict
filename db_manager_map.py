from aux import *
from db_manager import *
# All Chanes Are Made into the database
# To Apply the changes to a robot use robot_map_config.py

def get_virtual_wall(map_id):
    conf = get_config()
    #index = find_id_position_in_list(conf["maps"]["maps_structure"],map_id,"id")
    return conf["maps"]["maps_structure"][map_id]["virtual_walls"]

def set_virtual_wall(map_id, virtual_walls):
    conf = get_config()
    #index = find_id_position_in_list(conf["maps"]["maps_structure"],map_id,"id")
    conf["maps"]["maps_structure"][map_id]["virtual_walls"] = virtual_walls
    edit_config(conf)

def add_virtual_wall(map_id, waypoint):
    edit_config(get_virtual_wall(map_id).append(waypoint))

def get_landmarks(map_id):
    conf = get_config()
    #index = find_id_position_in_list(conf["maps"]["maps_structure"],map_id,"id")
    return conf["maps"]["maps_structure"][map_id]["points"]

def get_landmark_position(map_id, landmark_name):
    conf = get_config()
    #index_map = find_id_position_in_list(conf["maps"]["maps_structure"],map_id,"id")
    landmarks = conf["maps"]["maps_structure"][map_id]["points"]
    index = find_id_position_in_list(landmarks,landmark_name,"name") 
    return landmarks[index]["pose"]

def add_landmark(map_id, landmark):
    conf = get_config()
    #index = find_id_position_in_list(conf["maps"]["maps_structure"],map_id,"id")
    found = find_id_position_in_list(conf["maps"]["maps_structure"][map_id]["points"],landmark["name"],"name")
    ## NewPoint
    if found == -1:
        conf["maps"]["maps_structure"][map_id]["points"].append(landmark)
    ## Overwrite
    conf["maps"]["maps_structure"][map_id]["points"][found] = landmark
    edit_config(conf)

def get_special_regions(map_id):
    conf = get_config()
    #index = find_id_position_in_list(conf["maps"]["maps_structure"],map_id,"id")
    return conf["maps"]["maps_structure"][map_id]["special_regions"]

def set_special_regions(map_id, special_regions):
    conf = get_config()
    #index = find_id_position_in_list(conf["maps"]["maps_structure"],map_id,"id")
    conf["maps"]["maps_structure"][map_id]["special_regions"] = special_regions
    edit_config(conf)

def reset_special_region_speed(region_name,speed):
    conf = get_config()
    #index_map = find_id_position_in_list(conf["maps"]["maps_structure"],get_current_map_id(),"id")
    map_id = get_current_map_id()
    index_region = find_id_position_in_list(conf["maps"]["maps_structure"][map_id]["special_regions"],region_name,"name")
    conf["maps"]["maps_structure"][map_id]["special_regions"][index_region]["speed"] = speed
    edit_config(conf)

def add_special_regions(map_id, polygon):
    edit_config(get_virtual_wall(map_id).append(polygon))

def get_current_map_id():
    conf = get_config()
    return conf["maps"]["current_map"]

def post_current_map_id(map_id):
    conf = get_config()
    conf["maps"]["current_map"] = map_id
    edit_config(conf)

def set_reloc_landmak_name(map_id, reloc_landmark):
    conf = get_config()
    #index = find_id_position_in_list(conf["maps"]["maps_structure"],map_id,"id")
    conf["maps"]["maps_structure"][map_id]["reloc"] = reloc_landmark
    edit_config(conf)

def get_map_index(map_id):
    conf = get_config()
    index= find_id_position_in_list(conf["maps"]["maps_structure"],map_id,"id")
    return index

def get_reloc_landmak_name(map_id=""):
    conf = get_config()
    if map_id == "":
        map_id = get_current_map_id()
    #index = find_id_position_in_list(conf["maps"]["maps_structure"],map_id,"id")
    return map_id,conf["maps"]["maps_structure"][map_id]["reloc"]


###############################
##############################
#################################
def position(pose_x, pose_y, pose_t):
    return {"t":pose_t,"x":pose_x,"y":pose_y}

def pose(pose_x, pose_y, pose_t):
    return {"pose":position(pose_x, pose_y, pose_t)}

def landmark(name, pose_x, pose_y, pose_t,landmak_type="NORMAL"):
    return {"name":name,"pose":position(pose_x, pose_y, pose_t),"type":landmak_type}

def landmarks(landmarks):
    points = {"points":[]}
    for landmak in landmarks:
        points["points"].append(landmak)
    return points

def restric_layer(pose_x_1,pose_y_1, pose_x_2, pose_y_2):
    return {"pose":
                {
                "point1":
                    {"x":pose_x_1,"y":pose_y_1},
                "point2":
                    {"x":pose_x_2,"y":pose_y_2}
                }
            }

def restric_layers(restric_layers):
    waypoints = {"waypoints":[]}
    for restric_layer in restric_layers:
        waypoints["points"].append(restric_layer)
    return waypoints

def special_polygon(name,speed, polygon): ## Polygon [[x0,y0],[x1,y2],...,[x0,y0]]
    return {
        "name": name,
        "speed": speed,
        "polygon":polygon,
        "type": 0
    }

def map_image(width,height,resolution,origin_x,origin_y):
    return {
    "map_image": {
        "width": width,
        "height": height,
        "resolution": resolution,
        "origin_x": origin_x,
        "origin_y": origin_y
    }
    }