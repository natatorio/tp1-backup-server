import sys
import os
from multiprocessing import Manager, Process
from request_controller import *
import backup_scheduler
sys.path.append(os.path.dirname(os.path.abspath('main.py')))
from tools.socket import *
from tools.protocol import *

def main():
    manager = Manager()
    logLock = manager.Lock()
    registryLock = manager.Lock()
    backupScheduler = Process(target = backup_scheduler.main , args = (registryLock,logLock,))
    backupScheduler.start()
    RequestController(logLock, registryLock).start()
    backupScheduler.join()

if __name__ == "__main__":
    main()
