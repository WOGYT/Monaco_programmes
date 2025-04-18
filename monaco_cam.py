from ultralytics import YOLO
import cv2
import numpy as np
import time
from sort import *
import random
import math
import sys

def random_color_list():
    rand_color_list = []
    for _ in range(100):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        rand_color_list.append((r, g, b))
    return rand_color_list


def recognition(frame, frame_id, memo, verbose):
    results = model.predict(frame, augment=True, iou=0.7, verbose=verbose) #stream_buffer=True
    dets_to_sort = np.empty((0,6))
    human_count = 0
    for r in results:
        boxes = r.boxes
        #print(f"boxes={boxes}")
        for box in boxes:
            data=box.data.tolist()[0]
            #print(data)
            x, y, w, h, = int(data[0]), int(data[1]), int(data[2]), int(data[3])
            confidence = data[4]
            label = classNames[int(box.cls[0])]
            #print(f"label={label}")
            if label == "person":
                if confidence > 0.50:
                    human_count += 1
                    dets_to_sort = np.vstack((dets_to_sort, np.array([x, y, w, h, confidence, int(box.cls[0])])))
                    #frame = cv2.rectangle(frame, (x, y), (w, h), (192, 75, 50), 2)
                    #frame = cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y + 30), font, 1, (192, 75, 50), 3)
    frame_id += 1
    tracked_dets = tracker.update(dets_to_sort)
    # print(f"dets_to_sort{dets_to_sort}")
    # print(f"tracked_dets={tracked_dets}")
    # print(f"human count={human_count}")

    if len(tracked_dets) > 0:
        bbox_xyxy = tracked_dets[:, :4]
        identities = tracked_dets[:, 4]
        frame , memo = process_objects(frame,bbox_xyxy, rand_color_list , identities, memo)
        frame , memo = draw_trajectoire2(frame, memo, rand_color_list)
    return frame, frame_id

def process_objects(frame ,bbox, colors, identities, dico):
    # print(f"enumerate boxes={len(bbox)}")
    # print(f"bbox={bbox}")
    mini_count = 0
    for i in range(len(bbox)):
        box = bbox[i]
        x1, y1, x2, y2 = [int(coord) for coord in box]
        id = int(identities[i]) if identities is not None else 0
        mini_count += 1
        # Dessiner la boite
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), colors[id%100], 2)
        
        # Calculer et ajouter le centre
        center_X = (x1 + x2) // 2
        center_Y = (y1 + y2) // 2
        if id not in dico:
            dico[id] = {"centers": [] }  
        PointDelai = math.trunc(time.time())
        dico[id]["centers"].append((center_X, center_Y , PointDelai))

    return frame , dico
    
def draw_trajectoire2(frame, dico, colors):
    """Dessine les trajectoires sur l'image de la vidéo."""
    current_time = math.trunc(time.time())

    for id in dico:
        id = int(id)
        centers = dico[id]["centers"]

        # Filtrer les points récents
        centers = [point for point in centers if point[2] + 70 >= current_time]

        # Mise à jour du dictionnaire
        dico[id]["centers"] = centers  

        if len(centers) > 1:
            # Conversion des coordonnées en un format compatible avec cv2
            points = np.array([point[:2] for point in centers])

            # Dessiner la ligne des trajectoires
            cv2.polylines(frame, [points], isClosed=False, color=colors[id%100], thickness=5)    
    return frame , dico        


def print_image(frame, name):
    # frame = cv2.putText(frame, "FPS: " + str(round(fps, 2)), (200, 200), font, .7, (0, 255, 255), 1)
    # frame = cv2.putText(frame, "press [esc] to exit", (40, 690), font, .45, (0, 255, 255), 1)
    out = exits.get(name)
    out.write(frame)
    cv2.imshow("Recognized"+str(name), frame)


if __name__ == "__main__":
    urls = []
    # get videos urls'
    if (sys.argv[-1]) == "--debug":
        last = 1
        verbose = True
    else:
        last = 0
        verbose = False
    if len(sys.argv)-last >= 1:
        if sys.argv[1].lower() == "-f":
            print("Retrieving files from the given path")
            for i in range(2, len(sys.argv)-last):
                urls.append(sys.argv[i])
        elif sys.argv[1].lower() == "-d":
            print("Retrieving files from path directory")
            L = os.listdir(sys.argv[2])
            for i in L:
                if i[-4:] == ".mp4":
                    urls.append(i)
        print(f"Retrieving successful urls={urls}")
    else:
        print("Error in the command: You must specify whether you are giving a directory or a list of files if either '-d' or '-f' ")
        exit(0)
    # init sort
    sort_max_age = 5
    sort_min_hits = 2
    sort_iou_thresh = 0.2
    tracker = Sort(max_age=sort_max_age, min_hits=sort_min_hits, iou_threshold=sort_iou_thresh)
    memo = {}
    rand_color_list = random_color_list()

    caps = []
    window_names = []
    exits = {}
    # Load the YOLO model
    model = YOLO("yolo11m.pt")
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
    frame_id = 0
    length = 0

    # init windows and video writers
    for url in urls:
        cap = cv2.VideoCapture(url)
        caps.append(cap)
        window_names.append(url)
        returnvalue, frame = cap.read()
        exits[url] = cv2.VideoWriter(str(url) + '.avi', cv2.VideoWriter_fourcc(*"MJPG"), 15,
                                     (frame.shape[1], frame.shape[0]))  # str(random.randint(0, 1000))+
        length += int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    j = 0
    timeleft = 0
    len_urls = len(urls)
    starting_time = time.time()
    while True:
        j += 1
        if j %5 == 0:
            print(f"Estimated time left: {round((timeleft/j) // 60)}m{round((timeleft/7) % 60)}s")
        frame_time = time.time()
        # Read webcam
        # imgResp = urllib.request.urlopen(url)
        # imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
        i = 0
        atleastonetrue = False
        for cap in caps:
            returnvalue, frame = cap.read()
            # imgNp = np.array(bytearray(image), dtype=np.uint8)
            #frame = cv2.imdecode(image, -1)
            # Detecting objects

            # image recognition
            if returnvalue:
                atleastonetrue = True
                frame, frame_id = recognition(frame, frame_id, memo, verbose)

                #image printing
                print_image(frame, window_names[i])
            i += 1
        if not atleastonetrue:
            break
        elapsed_time = time.time() - frame_time
        timeleft += elapsed_time*(length - (j*len_urls))
        key = cv2.waitKey(1)
        if key == 27:
            print("[button pressed] ///// [esc].")
            for cap in caps:
                cap.release()
                exits[window_names[0]].release()
            print("[feedback] ///// Videocapturing succesfully stopped")
            break

    total_time = time.time() - starting_time
    print(f"Total time: {round(total_time//60)}m {round(total_time%60)}s ")
    print(f"Number of frame detected: {j} which is equal to {round((j/30)//60)}m{round((j/30)%60)}s per video for a total of {len_urls} videos")
    cv2.destroyAllWindows()