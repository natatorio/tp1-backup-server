import os
import sys
from threading import Lock
from pathlib import Path
sys.path.append(os.path.dirname(os.path.abspath('main.py')))
from tools.protocol import *

BACKUP_REGISTRY_ROOTDIR = "BackupRegistry"
REGISTRY_FILE_EXTENSION = ".txt"

class RegistryEntry:
    def __init__(self, item):
        self.rate = int(item[1])
        data = item[0].split(os.sep)
        self.ip = data.pop(0)
        self.port = data.pop(0)
        self.path = os.path.join(*data)

class BackupRegistryController:
    def __init__(self, lock, rootDir = BACKUP_REGISTRY_ROOTDIR):
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

    def fetch(self):
        rootDirPath = os.path.abspath(self.rootDir)
        registry = {}
        self.lock.acquire()
        for dir, _, files in os.walk(self.rootDir):
            for f in files:
                filePath = os.path.abspath(os.path.join(dir, f))
                file = open(filePath, "r")
                registry[os.path.relpath(filePath, rootDirPath)] = file.read()
                file.close()
        self.lock.release()
        return list(map(RegistryEntry, registry.items()))

    def __get_full_filepath(self, request):
        return os.path.join(self.rootDir, request.get_ip(), str(request.get_port()), request.get_path()) + REGISTRY_FILE_EXTENSION
