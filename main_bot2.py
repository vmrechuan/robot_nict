from func_obj import *
from mqtt_pub_manager_robot import *
from mqtt_sub_manager_robot import *
from mqtt_sub_manager_robot import *
import time

#reset_map_config(["wbot002"])
#ove_to_landmark("wbot002","21")
def mqtt_robot(robot_name):
    print(get_broker_from_robot_name(robot_name))
    mqtt_client = new_mqtt_client(broker_address=get_broker_from_robot_name(robot_name),client_name="PC"+robot_name)
    mqtt_client.on_message = on_message_robot
    mqtt_client.subscribe("#")
    return mqtt_client
mqtt_client_1 =  mqtt_robot("wbot002")
mqtt_client_1.loop_forever()
#for i in range(0,10000):
#    time.sleep(1)
#    update_last_status("wbot002")
#    #publisher_set_restrict_layers("wbot002",(get_points(define_wall_over_obj())),request="restrict_layer")