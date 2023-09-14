from subprocess import run
from time import sleep
from subprocess import Popen
import subprocess
# Path and name to the script you are trying to start
file_path = "/home/pi/project/elevator/elevator_main.py" 

restart_timer = 2
while True:
    #run("python3.exe "+file_path, check=True) 
    process = Popen(['python3', file_path],shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate() 
    
    #Nếu close App chủ động - không phải do crash thì dừng Auto restart
    #process.returncode=0: App đưc close bình thường, nếu process.returncode <0: App bị close bởi 1 tac nhan khac->crash
    #Neu ko phai restart app thi moi close autostart
    if process.returncode == 0 and str(out).find('RESTART APP'):
        # SaveLogCrash('CLOSE APP')
        break
    else: #Neu close app do crash hoac ngoai le
        indexErr = str(err).find('Traceback')
        if indexErr != -1: #Neu co Traceback -> co loi~ -> show tu vi tri loi
            data = str(err)[indexErr:]


