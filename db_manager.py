import json
from connect_mqtt import *
import requests
from aux import *

PATH_PROJECT = "robot"   
PATH_CONFIG = PATH_PROJECT+"/databases/conf.json"
HISTORICAL_DATA = PATH_PROJECT+"/databases/historical_data.json"
ROBOT_STATUS = PATH_PROJECT+"/databases/robot_status.json"
PATH_ROBOT_NOTIFY = {"wbot002":PATH_PROJECT+"/databases/responses_wbot002.txt",
                     "fruteratera#1":PATH_PROJECT+"/databases/responses_fruteratera#1.txt"}
PATH_OBJECT_DETECTED = PATH_PROJECT+"/databases/object_detected.txt"
PATH_CLASSES_OBJ = PATH_PROJECT+"/databases/yolov3.txt"
PATH_CONFIG_OBJ = PATH_PROJECT+"/databases/yolov3.cfg"
PATH_WEIGHTS_OBJ = PATH_PROJECT+"/databases/yolov3.weights"
PATH_OBJECT_DETECTION_CONF =  PATH_PROJECT+"/databases/box_detection_config.json"



###################
################### CONFIG MANAGEMENT
###################

def get_config():
    conf = {}
    with open(PATH_CONFIG,'r') as f:
        conf = json.load(f)
    return conf 
def edit_config(json_content):
    with open(PATH_CONFIG,'w') as f:
        json.dump(json_content,f,indent=4)
    return

###################
################### DB MANAGEMENT
###################

def get_database():
    conf = {}
    with open(HISTORICAL_DATA,'r') as f:
        conf = json.load(f)
    return conf 
def edit_database(json_content):
    with open(HISTORICAL_DATA,'w') as f:
        json.dump(json_content,f,indent=4)
    return

###################
################### MQTT PUBLISH MANAGEMENT
###################

def publish_mqtt(client, payload,topic="/frutera/request"):
    mqtt_client = new_mqtt_client(client_name=client)
    mqtt_client.publish(topic,json.dumps(payload),qos=0,retain=False)
    return

###################
################### API MANAGEMENT
###################

def api_post_robot(endpoint,payload):
    req = requests.post(endpoint,data=json.dumps(payload))
    #print(req.text)
    return req.text

def api_get_robot(endpoint):
    req = requests.get(endpoint)
    #print(req.text)
    return req

###################
################### IMAGE MANAGEMENT
###################

""" 
def get_object_database():
    conf = {}
    with open(PATH_PROJECT+"/databases/object_detected.json",'r') as f:
        conf = json.load(f)
    return conf 

def edit_objects_database(json_content):
    with open(PATH_PROJECT+"/databases/object_detected.json",'w') as f:
        json.dump(json_content,f,indent=4)
    return
 """

###################
################### BOXES MANAGEMENT
###################

""" def add_objects_database(json_content):
    with open(PATH_OBJECT_DETECTED,'a+') as f:
        f.write(json.dumps(json_content)+'\n')
    return """

def pop_objects_database():
    with open(PATH_OBJECT_DETECTED,'r') as f:
        boxes = read_last_line(f)
    return json.loads(boxes.replace("\'","\""))

def save_memory_boxes(memory_box):
    with open(PATH_OBJECT_DETECTED,'a+') as f:
        f.write(json.dumps(memory_box)+"\n")
    return 

def load_classes():
    classes = None
    with open(PATH_CLASSES_OBJ, 'r') as f:
        classes = [line.strip() for line in f.readlines()]
    return classes

def get_box_detection_config():
    box_config = {}
    with open(PATH_OBJECT_DETECTION_CONF, 'r') as f:
        box_config = json.load(f)
    return box_config

###################
################### MQTT DB NOTIFY MANAGEMENT
###################

def pop_robot_status_database(robot_name):
    with open(PATH_ROBOT_NOTIFY[robot_name],'r') as f:
        boxes = read_last_line(f)
    return json.loads(boxes.replace("\'","\""))

def add_robot_status_database(robot_name,payload):
    with open(PATH_ROBOT_NOTIFY[robot_name],'a+') as f:
        f.write(json.dumps(payload)+"\n")
    return 


###################
################### ROBOT STATUS MANAGEMENT
###################

def get_robot_status_file():
    conf = {}
    with open(ROBOT_STATUS,'r') as f:
        conf = json.load(f)
    return conf 

def edit_robot_status_file(json_content):
    with open(ROBOT_STATUS,'w') as f:
        json.dump(json_content,f,indent=4)
    return

def read_last_line(file):
    try:
        line = file.readlines()[-1]
    except:
        line = "{}"
    return line