import cv2
import base64
import numpy as np
from connect_mqtt import *
from set_webcam import *
from yolo_opencv import *

def encode_frame_mqtt(frame, type):
    match type:
        case "png":
            return encode_png_frame_mqtt(frame)
        case "url_png":
            return encode_url_png_frame_mqtt(frame)
        case _:
            return encode_png_frame_mqtt(frame)

def encode_png_frame_mqtt(frame):
   return base64.b64encode(cv2.imencode('.png',frame)[1])

def encode_url_png_frame_mqtt(frame):
   return f"data:image/png;base64,{encode_png_frame_mqtt(frame).decode('utf-8')}"

def send_frame(topic,payload,mqtt_client):
    mqtt_client.publish(topic,payload=payload,qos=0,retain=False)

def get_frames(from_file=True):
    if from_file:
        video = f'project/yolo/D22T1/basicvideo0.mp4'
        cap = cv2.VideoCapture(video)
    else:
        cap = configure_cam()
    return cap

def process_frame(frame, net, COLORS, classes, box_detection):
    import multiprocessing as mp

    # Getting in new boxes will be processed
    if box_detection["detection_index"]%box_detection["detection_rate"] == 0:
        func_1 = mp.Process(target=apply_model,args=(frame, net, COLORS, classes, box_detection,))

        func_1.start()
        #apply_model(frame, net, COLORS, classes, box_detection)
        #return apply_model(frame, net, COLORS, classes, box_detection)
    #if not, applyold bxes to new images
    box_detection["detection_index"]+=1
    objects = get_last_boxes()
    for obj in objects["objects"]:
        draw_prediction(frame, 
                        obj["class"],
                        obj["confidence"], 
                        obj["box"]["x"], 
                        obj["box"]["y"], 
                        obj["box"]["x"]+obj["box"]["w"], 
                        obj["box"]["y"]+obj["box"]["h"],
                        COLORS, classes)
    return frame


def frame_publisher(mqtt_client):
    count = 0
    net, COLORS, classes, box_detection = setup_net()
    cap = get_frames(False)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = process_frame(frame,net, COLORS, classes, box_detection)
        send_frame('/frutera/stream',encode_frame_mqtt(frame, "png"),mqtt_client)
        cv2.imshow('stream',frame)
        key = cv2.waitKey(125) & 0xFF
        if key == ord('q'):
            break
        count+=1
    cap.release()
    cv2.waitKey(20000)
    cv2.destroyAllWindows()

#frame_publisher(new_mqtt_client(client_name="PC_sender",broker_adress="localhost"))
