import time
from multiprocessing import Pool, Manager

from backup_registry_controller import *
import backup_controller

BACKUP_CONTROLLERS = 5
MIN_LENGTH_SIMULATION = 1

class Task:
    def __init__(self, entry):
        self.ip = entry.ip
        self.port = entry.port
        self.path = entry.path
        self.rate = entry.rate
        self.remaining = entry.rate

    def advance(self, other = None):
        if other:
            self.remaining = other.remaining
        else:
            self.remaining = max(0, self.remaining - 1)

    def __eq__(self, other):
        return self.ip == other.ip and self.port == other.port and self.path == other.path

    def needs_to_be_executed(self):
        return self.remaining == 0

    def reschedule(self):
        self.remaining = self.rate

class Scheduler:
    def __init__(self, poolBackupControllers, taskQueue, logLock, registryLock):
        self.tasks = []
        self.poolBackupControllers = poolBackupControllers
        self.taskQueue = taskQueue
        self.logLock = logLock
        self.registryController = BackupRegistryController(registryLock)

    def update(self):
        updatedTasks = []
        for entry in self.registryController.fetch():
            uTask = Task(entry)
            for task in self.tasks:
                if uTask == task:
                    uTask.advance(task)
                    self.tasks.remove(task)
            updatedTasks.append(uTask)
        self.tasks = updatedTasks

    def advance(self):
        for task in self.tasks:
            task.advance()
            self.__attempt_to_exec_task(task)

    def __attempt_to_exec_task(self, task):
        if not task.needs_to_be_executed():
            return
        res = self.poolBackupControllers.apply_async(backup_controller.main, args = (self.taskQueue, self.logLock,))
        self.taskQueue.put(task)
        res.get()
        task.reschedule()

def main(registryLock, logLock):
    with Pool(processes = BACKUP_CONTROLLERS) as poolBackupControllers:
        taskQueue = Manager().Queue()
        scheduler = Scheduler(poolBackupControllers, taskQueue, logLock, registryLock)
        while True:
            scheduler.update()
            time.sleep(MIN_LENGTH_SIMULATION)
            scheduler.advance()

if __name__ == "__main__":
    main()
