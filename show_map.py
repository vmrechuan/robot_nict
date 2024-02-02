import cv2
from func_obj import *

map_content = {"map_image": {
    "width": 147,
    "height": 152,
    "resolution": 0.05000000074505806,
    "origin_x": -6.53402,
    "origin_y": -3.81471
}}


input_image = "maps/room303.png"
img_original = cv2.imread(input_image) # CV sees the image as BRG

def remap_restric_layers(waypoints):
    coord_1 = []
    coord_2 = []
    for waypoint in waypoints["waypoints"]:
        coord_1.append((transformation_to_map(waypoint["pose"]["point1"]["x"],"x"),transformation_to_map(waypoint["pose"]["point1"]["y"],"y")))
        coord_2.append((transformation_to_map(waypoint["pose"]["point2"]["x"],"x"),transformation_to_map(waypoint["pose"]["point2"]["y"],"y")))
    return coord_1,coord_2

def draw_lines(img_original,origins,destinations): 
    map_update = img_original.copy()
    for origin,dest in zip(origins,destinations):
        cv2.line(map_update,(origin[0],origin[1]),(dest[0],dest[1]),(0,0,255),1)
    return map_update

def transformation_to_robot(reference,resolution,point):
    return reference + resolution*point

def transformation_to_map(point,coordinate,reference=map_content["map_image"]["resolution"],resolution=map_content["map_image"]["resolution"]):#coordnate = y, subract tge height (top to bottom)
    value = 0
    if coordinate == "y":
        reference = map_content["map_image"]["origin_y"]
        offset = map_content["map_image"]["height"]
        value = offset - round((point-reference)/resolution)
    elif coordinate == "x":
        reference = map_content["map_image"]["origin_x"]
        value = round((point-reference)/resolution)
    return value


#img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
img_original = cv2.resize(img_original,(map_content["map_image"]["width"],map_content["map_image"]["height"]),interpolation=cv2.INTER_LINEAR)

while True:
    waypoints = get_points(define_wall_over_obj())
    origins,destinations = remap_restric_layers(waypoints)
    img = draw_lines(img_original,origins,destinations)
    img = cv2.resize(img,(720,900),interpolation=cv2.INTER_LINEAR)
    cv2.imshow("map",img)
    key = cv2.waitKey(2) & 0xFF
    if key == ord('q'):
        break
    
cv2.destroyAllWindows()
