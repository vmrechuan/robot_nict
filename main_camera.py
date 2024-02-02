from func_obj import *
from mqtt_pub_manager_robot import *
from mqtt_sub_manager_robot import *
from stream_video_pub import *

frame_publisher(new_mqtt_client(client_name="PC_sender",broker_address="localhost"))
#reloc_froframe_publisherm_point("wbot002",request="reloc")
#reset_map_config(["wbot002"])
#move_to_landmark("wbot002","21")
#mqtt_client = new_mqtt_client()
#mqtt_client.on_message = on_message_robot
#mqtt_client.subscribe("#")
#mqtt_client.loop_forever()