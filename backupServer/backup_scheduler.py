import time
from multiprocessing import Pool, Manager

from backup_registry_controller import *
import backup_controller

BACKUP_CONTROLLERS = 5

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
    def __init__(self, pool, taskQueue):
        self.tasks = []
        self.pool = pool
        self.taskQueue = taskQueue

    def update(self, registry):
        updatedTasks = []
        for entry in registry:
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
        res = self.pool.apply_async(backup_controller.main, args = (self.taskQueue,))
        self.taskQueue.put(task)
        res.get()
        task.reschedule()

def main(registryLock):
    registryController = BackupRegistryController(registryLock)
    with Pool(processes = BACKUP_CONTROLLERS) as pool:
        taskQueue = Manager().Queue()
        scheduler = Scheduler(pool, taskQueue)
        while True:
            registry = registryController.fetch()
            scheduler.update(registry)
            time.sleep(1)
            scheduler.advance()

if __name__ == "__main__":
    main()
