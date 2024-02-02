from func_obj import *
from mqtt_pub_manager_robot import *

import time

for i in range(0,10000):
    for robot_name in ["fruteratera#1","wbot002"]:
        time.sleep(0.5)
        print("Update "+robot_name)
        update_last_status(robot_name)
        waypoints = get_points(define_wall_over_obj())
        publisher_set_restrict_layers(robot_name, waypoints,request="restrict_layer")
        #draw_map_restric_layers(waypoints)
