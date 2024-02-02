#############################################
# Object detection - YOLO - OpenCV
# Author : Arun Ponnusamy   (July 16, 2018)
# Website : http://www.arunponnusamy.com
############################################

#python3 yolo_opencv.py --image dog.jpg --config yolov3.cfg --weights yolov3.weights --classes yolov3.txt
import cv2
import numpy as np
from func_obj import *
import time


def get_output_layers(net):
    layer_names = net.getLayerNames()
    try:
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    except:
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    return output_layers


def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h, COLORS, classes):
    label = str(classes[class_id])
    color = COLORS[class_id]
    cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)
    cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

def setup_net():
    classes = load_classes()
    COLORS = np.random.uniform(0, 255, size=(len(classes), 3))
    box_detection_conf = get_box_detection_config()
    return cv2.dnn.readNet(PATH_WEIGHTS_OBJ, PATH_CONFIG_OBJ), COLORS, classes, box_detection_conf

def get_new_boxes(outs,box_detection,objects):
    objects["class_ids"] = []
    objects["confidences"] = []
    objects["boxes"] = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > box_detection["conf_threshold"]:
                center_x = int(detection[0] * box_detection["Width"])
                center_y = int(detection[1] * box_detection["Height"])
                w = int(detection[2] * box_detection["Width"])
                h = int(detection[3] * box_detection["Height"])
                x = center_x - w / 2
                y = center_y - h / 2
                objects["class_ids"].append(class_id)
                objects["confidences"].append(float(confidence))
                objects["boxes"].append([x, y, w, h])
    return objects

def construct_new_boxes(box_detection,image,COLORS, classes,objects):
    indices = cv2.dnn.NMSBoxes(objects["boxes"], objects["confidences"], box_detection["conf_threshold"], box_detection["nms_threshold"])
    memory_box = {"objects": [],"timestamp":0}
    for i in indices:
        try:
            box = objects["boxes"][i]
        except:
            i = i[0]
            box = objects["boxes"][i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        #draw_prediction(image, objects["class_ids"][i],  objects["confidences"][i], round(x), round(y), round(x+w), round(y+h),COLORS, classes)
        memory_box["objects"].append(box_stucture(objects["class_ids"][i],objects["confidences"][i],round(x), round(y), round(w), round(h)))
    memory_box["timestamp"] = timestamp_now()
    save_new_boxes(memory_box)
    print("image")
    return# image

def run_trough_network(image,scale,net):
    blob = cv2.dnn.blobFromImage(image, scale, (320,320), (0,0,0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(get_output_layers(net))
    return outs

def apply_model(image, net, COLORS, classes,box_detection):
    # Getting in new boxes will be processed
    objects = {"class_ids":[],"confidences":[],"boxes":[]}
    outs = run_trough_network(image,box_detection["scale"],net)
    get_new_boxes(outs,box_detection,objects)
    construct_new_boxes(box_detection, image, COLORS, classes,objects)
    return #construct_new_boxes(box_detection, image, COLORS, classes,objects)

def main(frame, net, COLORS, classes, box_detection):
    apply_model(frame, net, COLORS, classes, box_detection)


#local_test()