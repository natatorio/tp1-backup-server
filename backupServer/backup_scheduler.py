import time
from multiprocessing import Pool, Manager
from backup_registry_controller import *
import backup_controller

N_BACKUP_CONTROLLERS = 5
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
    def __init__(self, poolBackupControllers, logLock, registryLock):
        manager = Manager()
        self.tasks = []
        self.solvedTasks = manager.list()
        self.poolBackupControllers = poolBackupControllers
        self.taskQueue = manager.Queue()
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
        for item in self.solvedTasks:
            task, solved = item[0], item[1]
            if solved:
                task.reschedule()
            self.__reschedule(task)
            self.solvedTasks.remove(item)
        for task in self.tasks:
            task.advance()
            if task.needs_to_be_executed():
                self.tasks.remove(task)
                self.poolBackupControllers.apply_async(backup_controller.main, args = (self.taskQueue, self.logLock, self.solvedTasks,))
                self.taskQueue.put(task)

    def __reschedule(self, task):
        for t in self.tasks:
            if t == task:
                self.tasks.remove(t)
        self.tasks.append(task)

def main(registryLock, logLock):
    with Pool(processes = N_BACKUP_CONTROLLERS) as poolBackupControllers:
        scheduler = Scheduler(poolBackupControllers, logLock, registryLock)
        while True:
            scheduler.update()
            time.sleep(MIN_LENGTH_SIMULATION)
            scheduler.advance()

if __name__ == "__main__":
    main()
