import sys
import time
import os
import platform

class Logger(object):
    def __init__(self):
        self.CWD = os.getcwd()
        self.OS_NAME = platform.system()
        if self.OS_NAME == 'Windows':
            self.filepath = f"{self.CWD}\logs\output.log"
            self.log_directory_path = f"{self.CWD}\logs"
        else:
            self.filepath = f"{self.CWD}/logs/output.log"
            self.log_directory_path = f"{self.CWD}/logs"

        if not os.path.exists(self.log_directory_path):
            os.mkdir(self.log_directory_path)
        if not os.path.exists(self.filepath):
            f1 = open(self.filepath, 'w+')
            f1.close()
            
        self.terminal = sys.stdout
        self.log = open(self.filepath, "w+")

    def write(self, message):
        # self.terminal.write(message)
        self.log.write(message)  
        self.terminal.flush()
        self.log.flush()

    def close_file(self):
        self.log.close()     