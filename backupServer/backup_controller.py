import os
import sys
import json
from backup_log_controller import *
from backup_storage_controller import *
sys.path.append(os.path.dirname(os.path.abspath('backup_controller.py')))
from tools.socket import *

def main(taskQueue, logLock):
    task = taskQueue.get()
    logController = BackupLogController(logLock)
    server = ClientSocket()
    server.connect(task.ip, task.port)
    server.send(task.path)
    response = json.loads(server.receive())
    serverAvailable = response["available"]
    if serverAvailable:
        if response["size"] > 0:
            server.send("Send me the file")
            storageController = BackupStorageController(task.ip, task.path)
            f = storageController.open()
            data = server.receive_bin()
            while data:
                f.write(data)
                data = server.receive_bin()
            storageController.close(f)
        logController.log(task.ip, response["datetime"], task.path, response["size"])
    server.close()
    return serverAvailable

if __name__ == "__main__":
    main()
