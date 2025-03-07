from typing import Dict

import cv2
import urllib.request
import numpy as np
import time
#preferred version == 3.6.3
# this is working on 3.6.3  output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()] with CV 2
# this "SHOULD" work in python ==3.8 and higher [layer_name for layer_name in net.getUnconnectedOutLayersNames()]
from cv2 import VideoWriter

url1='rtmp://127.0.0.1/live/test2'
url2='rtmp://127.0.0.1/live/test'# base IP http://192.168.0.39/cam-hi.jpg
urls = [url1]
caps = []
window_names = []
exits = {}
# Load the YOLO model
net = cv2.dnn.readNet("./weights/yolov3.weights", "./configuration/yolov3.cfg")
classes = []
with open("./configuration/coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# Load webcam
font = cv2.FONT_HERSHEY_SIMPLEX
starting_time = time.time()
frame_id = 0

def recognition(frame, frame_id):
    height, width, channels = frame.shape
    labelv = ""
    # Visualising data
    class_ids = []
    confidences = []
    boxes = []
    w = 0
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.1:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.8, 0.3)
    if w < 1:
        F = (w * 42) / 8
        print(F)

    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            if class_ids[i] == 0:
                confidence = confidences[i]
                color = colors[class_ids[i]]
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                frame = cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y + 30), font, 1, color, 3)
                if label != labelv:
                    print(label)
                labelv = label
    frame_id += 1
    return frame, frame_id

def print_image(frame, frame_id, name):
    elapsed_time = time.time() - starting_time
    fps = frame_id / elapsed_time
    frame = cv2.putText(frame, "FPS: " + str(round(fps, 2)), (40, 670), font, .7, (0, 255, 255), 1)
    frame = cv2.putText(frame, "press [esc] to exit", (40, 690), font, .45, (0, 255, 255), 1)
    out = exits.get(name)
    out.write(frame)
    cv2.imshow("Image"+name, frame)

for url in urls:
    caps.append(cv2.VideoCapture(url))
    window_names.append(url)
    returnvalue, frame = cv2.VideoCapture(url).read()
    exits[url] = cv2.VideoWriter(url+'.avi', cv2.VideoWriter_fourcc(*"MJPG"), 20.0, (frame.shape[0], frame.shape[1]))

while True:
    # Read webcam
    # imgResp = urllib.request.urlopen(url)
    # imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
    i = 0
    for cap in caps:
        returnvalue, frame = cap.read()
        # imgNp = np.array(bytearray(image), dtype=np.uint8)
        #frame = cv2.imdecode(image, -1)
        # Detecting objects
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        # image recognition
        frame, frame_id = recognition(frame, frame_id)

        #image printing
        print_image(frame, frame_id, window_names[i])
        i += 1

    key = cv2.waitKey(1)
    if key == 27:
        print("[button pressed] ///// [esc].")
        j = 0
        for cap in caps:
            cap.release()
            exits[window_names[j]].release()
        print("[feedback] ///// Videocapturing succesfully stopped")
        break

cv2.destroyAllWindows()