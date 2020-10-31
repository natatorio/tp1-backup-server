import sys
import os
from threading import Lock
from backup_registry_controller import *
sys.path.append(os.path.dirname(os.path.abspath('main.py')))
from tools.socket import *
from tools.protocol import *

MAX_CLIENTS = 1
BACKUP_REGISTRY_ROOTDIR = "BackupRegistry"

backupServerSocket = ServerSocket(os.environ["BACKUP_SERVER_IP"], int(os.environ["BACKUP_SERVER_PORT"]), MAX_CLIENTS)
client, addr = backupServerSocket.accept()

registryLock = Lock()
registryController = BackupRegistryController(BACKUP_REGISTRY_ROOTDIR, registryLock)

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
