from aux import *
from db_manager import *
""" 
# Insert box element as first from database
def insert_box(obj_box):
    json_content = get_object_database()
    json_content["objects"].insert(0,obj_box)
    edit_objects_database(json_content)
    return

# Return all objects deteceted in the last image
def get_last_objects():
    objects = []
    db = get_object_database()
    for obj in db["objects"]:
        if obj["index"] == 0:
            objects.append(obj)
            return objects
        objects.append(obj)
    return 

def insert_boxes(obj_box):
    add_objects_database(obj_box)
    return """

def get_last_boxes():
    last_boxes = pop_objects_database()
    return last_boxes