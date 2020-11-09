import sys
import os
from multiprocessing import Manager, Process
from request_controller import *
import backup_scheduler
sys.path.append(os.path.dirname(os.path.abspath('backup_server.py')))
from tools.socket import *
from tools.protocol import *

class BackupServer:
    def __init__(self):
        manager = Manager()
        logLock = manager.Lock()
        registryLock = manager.Lock()
        self.requestController = RequestController(logLock, registryLock)
        self.backupScheduler = Process(target = backup_scheduler.main , args = (registryLock,logLock,))

    def run(self):
        self.backupScheduler.start()
        self.requestController.start()
        self.backupScheduler.join()
        self.requestController.join()
