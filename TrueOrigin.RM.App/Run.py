from dbm import error
import subprocess
import time
from src.utils import get_project_root

def SaveLogCrash(response):
    path = get_project_root() + '/Log/LogCritical/Critical.log'
    with open(path, 'a') as outfile:
        outfile.writelines(time.strftime("%m/%d/%Y, %H:%M:%S",time.localtime()) + ' : ' + str(response))
        outfile.write('\n')

#Auto restart GUI nếu như bị crash, đồng thời lưu log
while True:
    SaveLogCrash('START APP')
    process = subprocess.Popen(['python3', get_project_root() + '/main.py'],shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate() #Chờ main close- thực tế là chờ Main kết thúc, nhưng Main ch kết thuc khi crash
    
    #Nếu close App chủ động - không phải do crash thì dừng Auto restart
    #process.returncode=0: App đưc close bình thường, nếu process.returncode <0: App bị close bởi 1 tac nhan khac->crash
    #Neu ko phai restart app thi moi close autostart

    if process.returncode == 0 and str(out).find('RESTART APP') == -1:
        SaveLogCrash('CLOSE APP')
        break
    else: #Neu close app do crash hoac ngoai le
        indexErr = str(err).find('Traceback')
        if indexErr != -1: #Neu co Traceback -> co loi~ -> show tu vi tri loi
            data = str(err)[indexErr:]
            SaveLogCrash(data)
   