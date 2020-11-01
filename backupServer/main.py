import sys
import os
from multiprocessing import Manager, Process
from backup_registry_controller import *
from backup_log_controller import *
import backup_scheduler
sys.path.append(os.path.dirname(os.path.abspath('main.py')))
from tools.socket import *
from tools.protocol import *

MAX_CLIENTS = 1

def main():
    backupServerSocket = ServerSocket(os.environ["BACKUP_SERVER_IP"], os.environ["BACKUP_SERVER_PORT"], MAX_CLIENTS)
    client, addr = backupServerSocket.accept()

    manager = Manager()
    logLock = manager.Lock()
    logController = BackupLogController(logLock)
    registryLock = manager.Lock()
    registryController = BackupRegistryController(registryLock)
    backupScheduler = Process(target = backup_scheduler.main , args = (registryLock,logLock,))
    backupScheduler.start()

    msg = client.receive()
    while msg:
        request = Request(msg)
        if(request.is_query()):
            try:
                response = logController.query(request.get_ip(), request.get_path())
            except:
                response = "ERROR: Backups not found for that path"
        else:
            try:
                registryController.persist(request)
                response = "SUCCESS: Registered properly"
            except:
                response = "ERROR: Path not registered"
        client.send(response)
        msg = client.receive()

    client.close()
    backupServerSocket.close()
    backupScheduler.join()


if __name__ == "__main__":
    main()
