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

data_return ='{"message": "received"}'

list_data_read = []
detect_status = False

def run_data_json(data_json):
    detect = detect_face_fake(model_dir = "model/phone_9_9.pt")
    data_time = datetime.now()
    ret, data_detect = detect.run(data_json)
    if ret == True:
        today = date.today()
        with open("log/" + str(today) + ".txt", 'a') as wf:
            wf.write(str(data_time) + '\n')
            wf.write(str(data_detect) + '\n' + '\n')

def thread_function():
    global detect_status
    while(1):
        if detect_status == True:
            print("start")
            while len(list_data_read):
                print("list_data_read",list_data_read)
                print("len:",len(list_data_read))
                run_data_json(list_data_read[0])
                list_data_read.pop(0)
            detect_status = False
            print("end")

def process_data_json(data_rec, conn):
    global detect_status
    try:
        json_str = data_rec.decode()
        data_json_read = json.loads(json_str.replace("<EOF>", ""))
        
        print("data_json", data_json_read) 
        send_to_client(conn, data_return)
        list_data_read.append(data_json_read)
        if detect_status == False:
            detect_status = True

    except:
        data_return["message"] = "data error"
        send_to_client(conn, data_return)

def send_to_client(conn, data_json):
    conn.sendall(( data_json + "<EOF>" + "\n").encode())
    # print( str(data_json)+ "<EOF>" + "\n")

def process_socket():
    global detect_status
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
        
if __name__ == '__main__':
    #  start threads
    p1 = threading.Thread(target=process_socket)
    p1.start()

    x = threading.Thread(target=thread_function, args=[])
    x.start()

