from threading import Thread, Lock
import cv2

class VideoStream:
    def __init__(self, src = 0, width = 640, height = 480) :
        self.stream = cv2.VideoCapture(src)
        self.shape = [width, height]
        (self.ret, self.frame) = self.stream.read()
        self.started = False
        self.read_lock = Lock()

    def start(self) :
        if self.started :
            print ("already started!!")
            return None
        self.started = True
        self.thread = Thread(target=self.update, args=())
        self.thread.start()
        return self

    def update(self) :
        while self.started :
            (self.ret, self.frame) = self.stream.read()
            self.read_lock.acquire()
            self.read_lock.release()

    def read(self):
        self.read_lock.acquire()
        self.read_lock.release()
        self.frame = cv2.resize(self.frame, self.shape)
        return self.ret, self.frame

    def stop(self) :
        self.started = False
        self.thread.join()

    def __exit__(self) :
        self.stream.release()

if __name__ == "__main__" :
    url = "rtsp://admin:admin@192.168.1.10:554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif"
    vs = VideoStream(src= url).start()
    while True :
        ret, frame = vs.read()
        cv2.imshow('webcam', frame)
        if cv2.waitKey(1) == 27 :
            break
    vs.stop()
    cv2.destroyAllWindows()
