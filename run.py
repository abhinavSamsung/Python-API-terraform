import subprocess
import sys
import os
import platform

CWD = os.getcwd()
OS_NAME = platform.system()

if OS_NAME == 'Windows':
    filepath = f"{CWD}\logs\output.log"
    log_directory_path = f"{CWD}\logs"
else:
    filepath = f"{CWD}/logs/output.log"
    log_directory_path = f"{CWD}/logs"

if not os.path.exists(log_directory_path):
    os.mkdir(log_directory_path)
if not os.path.exists(filepath):
    f1 = open(filepath, 'w+')
    f1.close()

with open(filepath, 'wb+') as file:
    p = subprocess.Popen('uvicorn app:app --reload', stdout=subprocess.PIPE, bufsize=1)
    for line in iter(p.stdout.readline, b''):
        file.write(line)
        print(line)
    file.close()    
    p.stdout.close()
    p.wait()