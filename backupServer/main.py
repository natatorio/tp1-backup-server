import sys
import os
from multiprocessing import Lock, Process
from backup_registry_controller import *
import backup_scheduler
sys.path.append(os.path.dirname(os.path.abspath('main.py')))
from tools.socket import *
from tools.protocol import *

MAX_CLIENTS = 1

def main():
    backupServerSocket = ServerSocket(os.environ["BACKUP_SERVER_IP"], int(os.environ["BACKUP_SERVER_PORT"]), MAX_CLIENTS)
    client, addr = backupServerSocket.accept()

    registryLock = Lock()
    registryController = BackupRegistryController(registryLock)
    backupScheduler = Process(target = backup_scheduler.main , args = (registryLock,))
    backupScheduler.start()

    msg = client.receive()
    while msg:
        request = Request(msg)
        if(request.is_query()):
            response = "ERROR: Query not implemented"
        else:
            try:
                registryController.persist(request)
                response = "SUCCESS: Registered properly"
            except:
                response = "ERROR: Path no registrado"
        # server = ClientSocket()
        # server.connect(request.get_ip(), request.get_port())
        # server.send(request.to_json())
        # response = server.receive()
        # server.close()
        client.send(response)
        msg = client.receive()

    client.close()
    backupServerSocket.close()
    backupScheduler.join()


if __name__ == "__main__":
    main()
