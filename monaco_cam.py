from typing import Dict
from ultralytics import YOLO
from PIL import Image
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
urls = [url2]
caps = []
window_names = []
exits = {}
# Load the YOLO model
model = YOLO("yolov8n.pt")
classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]

# Load webcam
font = cv2.FONT_HERSHEY_SIMPLEX
starting_time = time.time()
frame_id = 0

def recognition(frame, frame_id):
    results = model.predict(frame)[0]
    for r in results:
        boxes = r.boxes
        for box in boxes:
            data=box.data.tolist()[0]
            #print(data)
            x, y, w, h, = int(data[0]), int(data[1]), int(data[2]), int(data[3])
            confidence = data[4]
            label = classNames[int(box.cls[0])]
            if confidence > 0.70:
                if label == "person":
                    frame = cv2.rectangle(frame, (x, y), (w, h), (192, 75, 50), 2)
                    frame = cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y + 30), font, 1, (192, 75, 50), 3)
    frame_id += 1
    return frame, frame_id

def print_image(frame, frame_id, name):
    elapsed_time = time.time() - starting_time
    fps = frame_id / elapsed_time
    frame = cv2.putText(frame, "FPS: " + str(round(fps, 2)), (200, 200), font, .7, (0, 255, 255), 1)
    frame = cv2.putText(frame, "press [esc] to exit", (40, 690), font, .45, (0, 255, 255), 1)
    out = exits.get(name)
    out.write(frame)
    cv2.imshow("Image"+str(name), frame)

for url in urls:
    caps.append(cv2.VideoCapture(url))
    window_names.append(url)
    returnvalue, frame = cv2.VideoCapture(url).read()
    exits[url] = cv2.VideoWriter(str(url)+'.avi', cv2.VideoWriter_fourcc(*"MJPG"), 15, (frame.shape[1], frame.shape[0]))

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