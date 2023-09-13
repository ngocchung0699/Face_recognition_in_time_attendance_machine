from ultralytics import YOLO
import time
import cv2

class YoloV8:
    def __init__(self, model = "yolov8n.pt", gpu = "cuda"):
        # Load a model
        self.model = YOLO(model)  # load a pretrained model (recommended for training)
        self.results: any
        self.img: any
        self.conf = 0.25
        self.iou = 0.1
        self.imgsz: any
        self.list_result = []
    def predict(self, img, imgsz = 480, conf = 0.25, iou = 0.1):
        self.conf = conf
        self.imgsz = imgsz
        self.iou = iou
        self.list_result = []
        self.results = self.model.predict(img, save = False, imgsz = self.imgsz, conf = self.conf, iou = self.iou)
        for r in self.results:
            self.img =  r.orig_img
            boxes = r.boxes
            list_c = []
            for box in boxes:
                b = box.xyxy[0].tolist() # get box coordinates in (top, left, bottom, right) format
                b = [round(x) for x in b]
                list_c = b
                list_c.append(self.model.names[int(box.cls)])
                list_c.append(round(box.conf[0].tolist(), 2))
                self.list_result.append(list_c)
        return self.list_result

    def image(self):
        return self.img

if __name__ == "__main__" :
    yolo = YoloV8(model= "yolov8/help/ocr_s.pt")
    yolo.predict("xe.png", conf = 0.25, iou = 0.1)
    cv2.imshow("plot",yolo.plot())
    cv2.waitKey()

