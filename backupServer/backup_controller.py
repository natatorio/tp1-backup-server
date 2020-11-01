import os
import sys
import json
from backup_log_controller import *
sys.path.append(os.path.dirname(os.path.abspath('backup_controller.py')))
from tools.socket import *

def main(taskQueue, lock):
    task = taskQueue.get()
    logController = BackupLogController(lock)
    server = ClientSocket()
    server.connect(task.ip, task.port)
    server.send(task.path)
    response = json.loads(server.receive())
    server.close()
    logController.log(task.ip, response["datetime"], task.path, response["size"])

if __name__ == "__main__":
    main()
