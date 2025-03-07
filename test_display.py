import cv2
from threading import Thread
import time
import queue
url='rtmp://127.0.0.1/live/test2'


class ThreadedCamera(object):
    def __init__(self, src=0):
        self.capture = cv2.VideoCapture(src)
        #self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        self.capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        # print(self.capture.get(cv2.CAP_PROP_BUFFERSIZE))# self.capture.set(3, 300)
        # self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640);
        # self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480);
        # FPS = 1/X
        # X = desired FPS
        self.FPS = 1 / 20
        self.FPS_MS = int(self.FPS * 1000)

        #create image queue
        self.q = queue.Queue()

        # Start frame retrieval thread
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()
                if not self.status:
                    break
                if not self.q.empty():
                    try:
                        self.q.get_nowait()  # discard previous (unprocessed) frame
                    except queue.Empty:
                        pass
                self.q.put(self.frame)
            #time.sleep(self.FPS_MS)
    def get(self):
        return self.q.get()

    def show_frame(self):
        self.frame = self.get()
        if self.status:
            self.frame = cv2.resize(self.frame, (680, 540))
            cv2.imshow('frame', self.frame)
        # cv2.waitKey(self.FPS_MS)

threaded_camera = ThreadedCamera(url)
while True:
    try:
        threaded_camera.show_frame()
    except AttributeError:
        pass
    if cv2.waitKey(1) == ord('q'):
        break

threaded_camera.capture.release()
cv2.destroyAllWindows()