import socket
import json
import threading
import cv2
import time
import os
from help.ApiCMS import detect_face_fake
from datetime import date, datetime

HOST = "0.0.0.0"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

class main_process:
    def __init__(self):
        self.data_return ='{"message": "received"}'

        self.list_data_read = []
        self.detect_status = False
    
    def run_data_json(self, data_json):
        detect = detect_face_fake(model_dir = "model/phone_9_9.pt")
        data_time = datetime.now()
        ret, data_detect = detect.run(data_json)
        if ret == True:
            today = date.today()
            with open("log/" + str(today) + ".txt", 'a') as wf:
                wf.write(str(data_time) + '\n')
                for data in data_detect:
                    wf.write(str(data) + '\n' + '\n')
                wf.write('\n')
        data_detect = ""

    def thread_function(self):
        try:
            while(1):
                if self.detect_status == True:
                    print("start")
                    while len(self.list_data_read):
                        # print("list_data_read",list_data_read)
                        # print("len:",len(list_data_read))
                        self.run_data_json(self.list_data_read[0])
                        self.list_data_read.pop(0)
                    self.detect_status = False
                    print("end")
        except:
            pass
    def process_data_json(self, data_rec, conn):
        try:
            json_str = data_rec.decode()
            data_json_read = json.loads(json_str.replace("<EOF>", ""))
        
            print("data_json", data_json_read) 
            self.send_to_client(conn, self.data_return)
            self.list_data_read.append(data_json_read)
            if self.detect_status == False:
                self.detect_status = True
        except:
            self.data_return["message"] = "data error"
            self.send_to_client(conn, self.data_return)

    def send_to_client(conn, data_json):
        conn.sendall(( data_json + "<EOF>" + "\n").encode())
        # print( str(data_json)+ "<EOF>" + "\n")
    def __del__(self): 
        print('deleted class main_process') 

def process_socket():
    while(True):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                print("Ready")
                s.bind((HOST, PORT))
                s.listen()
                conn, addr = s.accept()
                with conn:
                    while True:
                        print(addr)
                        data_rec = conn.recv(1000)
                        if not data_rec:
                            break
                        # print("data_rec", data_rec)
                        process_data_json(data_rec, conn)
            except:
                print("socket infomation:", conn)
                print("data received:", data_rec)
            finally:
                print("Closed socket, there is a problem with the socket")