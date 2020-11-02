import os
from pathlib import Path

BACKUP_LOG_ROOTDIR = "BackupLog"
LOGFILE_NAME = "log.txt"

class BackupLogController:
    def __init__(self, lock, root = BACKUP_LOG_ROOTDIR):
        self.rootDir = root
        self.lock = lock

    def log(self, ip, datetime, path, size):
        filePath = self.__get__filepath(ip, path)
        self.lock.acquire()
        Path(os.path.dirname(filePath)).mkdir(parents = True, exist_ok = True)
        f = open(filePath, "a+")
        f.write(datetime + " " + str(size) + "\n")
        f.close()
        self.lock.release()

    def query(self, ip, path):
        filePath = self.__get__filepath(ip, path)
        if not os.path.exists(filePath): raise
        self.lock.acquire()
        f = open(filePath, "r")
        response = f.read()
        f.close()
        self.lock.release()
        return response

    def __get__filepath(self, ip, path):
        return os.path.join(self.rootDir, ip, path, LOGFILE_NAME)
