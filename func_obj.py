from db_manager_obj import *
from db_manager_map import *

#def box_as_str(index,class_type,confidence,x,y,w,h):
#    return json.dumps(box(index,class_type,confidence,x,y,w,h))

def box_stucture(class_type,confidence,x,y,w,h):
    return {
        "class" : int(class_type),
        "confidence":  confidence,
        "box" : {"x":x,"y":y,"w":w,"h":h}
    }
def objects_stucture(boxes):
    objects = {"objects:":[],"timestamp":timestamp_now()}
    for box in boxes:
        objects.append(box)
    return objects

def bounds_for_detection(x_pose, error, reference):
    return True if x_pose >= reference-error and x_pose <= reference+error else False

""" def save_boxes(index,class_type,confidence,x,y,w,h,reference=11):
    json_content = get_last_objects()
    for obj in json_content:
        if obj["index"] == index:
            reference =  obj["box"]["x"]
            break
        break
    if reference - int(x) <= 10:
        insert_box(box_stucture(index,class_type,confidence,x,y,w,h))
    return """

def save_new_boxes(boxes, reference=11):
    #last_box = get_last_boxes()
    #if (last_box["objects"] == boxes["objects"]):
    #    return
    save_memory_boxes(boxes)
    return
"""     json_content = get_last_boxes()
    #if (json_content["objects"][0]["box"] == boxes["objects"][0]["box"]):
        #return
    ## Check if the database is empty (there eists a scenario i which the incoming data is empty, stilll have to woork on it)
    try:
        if bounds_for_detection(json_content["objects"][0]["box"]["x"],4,boxes["objects"][0]["box"]["x"]):
            return
    except:
        save_memory_boxes(boxes)
        return """

# argin calculation for chairs
def define_boundries():
    reference_x = -1.137
    reference_y = 2.024
    positions = {"positions":[{"pose":{"point1":{"x":-1.431713634226564,"y":2.366568969755397},"point2":{"x":-0.8188640253798847,"y":2.370031396924022}}},
                        {"pose":{"point1":{"x":-0.8188640253798847,"y":2.370031396924022},"point2":{"x":-0.8171328117955721,"y":1.6550401866028963}}},
                        {"pose":{"point1":{"x":-0.8171328117955721,"y":1.6550401866028963},"point2":{"x":-1.4351760613951892,"y":1.6567105737639762}}},
                        {"pose":{"point1":{"x":-1.4386384885638144,"y":2.366568969755397},"point2":{"x":-1.436907274979502,"y":1.653308973018584}}}]}
    
    for pose in positions["positions"]:
        pose["pose"]["point1"]["x"] -= reference_x
        pose["pose"]["point1"]["y"] -= reference_y
        pose["pose"]["point2"]["x"] -= reference_x
        pose["pose"]["point2"]["y"] -= reference_y
    return positions

# add the bouding areas to the points n which objects are found
def get_points(block_points):
    map_id = get_current_map_id()
    waypoints =get_virtual_wall(map_id)
    points = get_landmarks(map_id)
    margins = define_boundries()
    print(block_points)
    for block_element in block_points:
        index = find_id_position_in_list(points,block_element,"name")
        for margin in margins["positions"]:
            waypoints["waypoints"].append(restric_layer(
                points[index]["pose"]["x"]+margin["pose"]["point1"]["x"],
                points[index]["pose"]["y"]+margin["pose"]["point1"]["y"],
                points[index]["pose"]["x"]+margin["pose"]["point2"]["x"],
                points[index]["pose"]["y"]+margin["pose"]["point2"]["y"]))
    return waypoints

# detect obj in positions
def define_wall_over_obj(error = 30):
    x_list = [56,201,356,504]
    point_list = ["11","111","12","122"]
    objects = get_last_boxes()#get_last_objects()
    block_points = []
    if len(objects) == 0: # No elements
        return block_points
    for obj in objects["objects"]:
        #print(obj)
        x_pose = obj["box"]["x"]
        for i,reference in enumerate(x_list):
            if bounds_for_detection(x_pose,error,reference):
                block_points.append(point_list[i])
    return block_points