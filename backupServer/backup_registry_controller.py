import os
import sys
from threading import Lock
from pathlib import Path
sys.path.append(os.path.dirname(os.path.abspath('main.py')))
from tools.protocol import *


class BackupRegistryController:

    def __init__(self, rootDir, lock):
        self.rootDir = rootDir
        self.lock = lock

    def persist(self, request):
        filePath = self.__get_full_filepath(request)
        fileExists = os.path.exists(filePath)
        if request.is_unregister():
            if not fileExists: raise
            self.lock.acquire()
            os.remove(filePath)
            self.lock.release()
        else:
            dir = os.path.dirname(filePath)
            self.lock.acquire()
            Path(dir).mkdir(parents = True, exist_ok = True)
            if fileExists:
                os.remove(filePath)
            file = open(filePath, "w")
            file.write(request.get_rate())
            file.close()
            self.lock.release()


    def __get_full_filepath(self, request):
        return '/'.join((self.rootDir, request.get_ip(), str(request.get_port()), request.get_path()))
