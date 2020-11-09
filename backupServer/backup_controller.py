import os
import sys
import json
from backup_log_controller import *
from backup_storage_controller import *
sys.path.append(os.path.dirname(os.path.abspath('backup_controller.py')))
from tools.socket import *

class BackupController:
    def __init__(self, taskQueue, logLock, solvedTasks):
        self.taskQueue = taskQueue
        self.solvedTasks = solvedTasks
        self.logController = BackupLogController(logLock)

    def run(self):
        task = self.taskQueue.get()
        server = ClientSocket()
        try:
            server.connect(task.ip, task.port)
        except:
            self.solvedTasks.append((task, False))
            return
        server.send(task.path)
        response = json.loads(server.receive())
        print(response, task.ip, task.path)
        if response["size"] > 0:
            server.send("Ready to receive file")
            storageController = BackupStorageController(task.ip, task.path)
            f = storageController.open()
            data = server.receive_bin()
            while data:
                f.write(data)
                data = server.receive_bin()
            storageController.close(f)
        self.logController.log(task.ip, response["datetime"], task.path, response["size"])
        server.close()
        self.solvedTasks.append((task, True))

def main(taskQueue, logLock, solvedTasks):
    BackupController(taskQueue, logLock, solvedTasks).run()

if __name__ == "__main__":
    main()
