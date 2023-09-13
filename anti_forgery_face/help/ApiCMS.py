
import requests
import json
# import the necessary packages
import numpy as np
import urllib.request
import cv2
import os
from help.my_yolo import YoloV8
from help.draw import plot

class ApiCMS():
    url = "http://192.168.1.205/stech/snvp/dashboard/public/api/account/"

    TIMEOUT = 3
    def GetHistoryCheckTimekeep(self, type_time = None, search_from = None, search_to = None):

        '''Lấy danh sách các lượt chấm công
        Json input: 
        Result:
        {
            "code": 0,
            "list": [
                {
                    "id": 46812,
                    "image": "timekeep/image_1694144956.8665.png",
                    "link_image": "http://192.168.1.205/stech/snvp/dashboard/public/storage/timekeep/image_1694144956.8665.png"
                }
            ],
            "message": "successful"
        }
        '''
        headers = { 'Content-Type': 'application/json' }
        #dinh dang content sang UTF-8
        try:
            print(ApiCMS.url + 'get-history-check-timekeep/' + str(type_time))
            response = requests.request("GET", ApiCMS.url + 'get-history-check-timekeep/' + str(type_time) , headers=headers, timeout = ApiCMS.TIMEOUT)
            obj = json.loads(response.content.decode('UTF-8'))

            # result = json.dumps(obj, ensure_ascii=False)
            if obj['code'] == 0:
                if len(obj['list']) > 0:
                    return obj['list']
                else:
                    return None
            else:
                return None
        except:
            return None
    def UpdateHistoryCheckTimekeep(self, data_detected):
        '''Cập nhật dữ liệu lượt điểm danh lên server
        Json input: 
        {
            "list": [
                {
                    "id": 46812,
                    "threshold_fake":0.5
                }
            ]
        }
        Result:
        {
            "code": 0,
            "message": "successful"
        }
        '''
        # body = json.dumps({
        #     "list": [
        #         {
        #             "id": 46812,
        #             "threshold_fake":0.6
        #         }
        #     ]
        # })
        body = json.dumps({
            "list": data_detected
        })
        # print(body)
        headers = { 'Content-Type': 'application/json' }
        #dinh dang content sang UTF-8

        try:
            response = requests.request("POST", ApiCMS.url + 'update-history-check-timekeep', headers=headers, data=body, timeout = ApiCMS.TIMEOUT)
            obj = json.loads(response.content.decode('UTF-8'))
            # result = json.dumps(obj, ensure_ascii=False)
            if obj['code'] == 0:
                return True
            else:
                return False
        except:
            return False

class detect_face_fake():
    def __init__(self, model_dir = "yolov8n.pt"):
        self.yolo_detect_phone = YoloV8(model= model_dir)
        self.yolo_detect_face = YoloV8(model= "model/yolov8n-face.pt")
        self.api = ApiCMS()
        self.data_post ={
            "id": 46812,
            "threshold_fake":0.6
            }
    def url_to_image(self,url):
	    # download the image, convert it to a NumPy array, and then read
	    # it into OpenCV format
        resp = urllib.request.urlopen(url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        # return the image
        return image

    def detect_image(self, image):
        results = self.yolo_detect_phone.predict(image, conf = 0.7)
        name = "real"
        img_size = image.shape # (h,w,z)
        threshold = ''
        if results:
            # try:
                for result in results:
                    w = result[2] - result[0]
                    h = result[3] - result[1]
                    if (img_size[1]*0.3) < w < (img_size[1]*0.9)and (img_size[0]*0.3)<h:
                        img_crop = image[result[1]:result[3], result[0]:result[2]]  
                
                        if result[4] == "phone":
                            box_face = self.yolo_detect_face.predict(img_crop)
                            print("box_face", box_face)
                            if box_face:
                                image = plot(img = image, bbox = result, text = "phone")
                                name = "phone"
                                threshold = result[5]
            # except:
            #     print("anh loi:", path_img)
                return image, name, threshold
        else:
            return "unknow", "unknow", "unknow"

    def run(self, data_received):
        
        if data_received["search_time"]:
            response = self.api.GetHistoryCheckTimekeep(type_time = data_received["search_time"], search_from = data_received["search_from"], search_to = data_received["search_to"])
            if response != None:
                # print(response)
                list_data_post = []
                for i in range(0, len(response)):
                    if response[i]['link_image']:
                        print(i+1, response[i]['link_image'])
                        image = self.url_to_image(response[i]['link_image'])

                        image, name, threshold = self.detect_image(image)
                        # name = "phone"
                        # threshold = 0.5
                        list_buffer = {}
                        list_buffer = self.data_post
                        list_buffer['id'] = response[i]['id']
                        if name == "phone":
                            list_buffer['threshold_fake'] = threshold
                            # if os.path.isdir("phone") == False:
                            #     os.mkdir("phone")
                            # cv2.imwrite("phone/"+ str(response[i]['id']) +".jpg", image)
                        else:
                            # if os.path.isdir("unknow") == False:
                            #     os.mkdir("unknow")
                            # cv2.imwrite("unknow/"+ str(response[i]['id']) +".jpg", image)
                            list_buffer['threshold_fake'] = 0
                        # print(list_buffer)
                        list_data_post.append(json.loads(json.dumps(list_buffer)))

                print(list_data_post)
                response = self.api.UpdateHistoryCheckTimekeep(list_data_post)
                if response == True:
                    print("nhan dang thanh cong, da gui len server")
        return True, list_data_post

    def __del__(self):
        print('Destructor called, Employee deleted.') 
    def __exit__(self, exc_type, exc_value, traceback):
        pass
if __name__ == '__main__':
    # detect_face_fake(type_time_d= "today")
    pass
    


