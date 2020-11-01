import sys
import os
from backup_registry_controller import *
from backup_log_controller import *
sys.path.append(os.path.dirname(os.path.abspath('request_controller.py')))
from tools.socket import *
from tools.protocol import *

MAX_CLIENTS = 1
QUERY_ERROR_MSG = "ERROR: Backups not found for that path"
REG_ERROR_MSG = "ERROR: Path not registered"
REG_SUCCESS_MSG = "SUCCESS: Registered properly"

class RequestController:
    def __init__(self, logLock, registryLock):
        self.backupServerSocket = ServerSocket(os.environ["BACKUP_SERVER_IP"], os.environ["BACKUP_SERVER_PORT"], MAX_CLIENTS)
        self.logController = BackupLogController(logLock)
        self.registryController = BackupRegistryController(registryLock)

    def start(self):
        while True:
            client, addr = self.backupServerSocket.accept()
            msg = client.receive()
            while msg:
                response = process_request(Request(msg))
                client.send(response)
                msg = client.receive()

            client.close()
        self.backupServerSocket.close()

    def process_request(self, request):
        if(request.is_query()):
            return __process_query(request)
        return __process_reg_order(request)

    def __process_query(self, query):
        try:
                return self.logController.query(query.get_ip(), query.get_path())
        except:
            return QUERY_ERROR_MSG

    def __process_reg_order(self, order):
        try:
            self.registryController.persist(request)
            return REG_SUCCESS_MSG
        except:
            return REG_ERROR_MSG
