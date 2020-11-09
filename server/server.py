import sys
import os
import time
import random
from multiprocessing import Manager, Pool
import backup_agent_controller
sys.path.append(os.path.dirname(os.path.abspath('server.py')))
from tools.socket import *

SECS_OF_UNAVAILABILITY = 10
MAX_BACKUPS_UNTIL_UNAVAILABILITY = 5
N_BACKUP_AGENTS = 2

class Server:
    def __init__(self):
        manager = Manager()
        self.hashes = manager.dict()
        self.queue = manager.Queue()

    def run(self):
        while True:
            # Server not available for backups
            time.sleep(SECS_OF_UNAVAILABILITY)
            # Server available
            s = ServerSocket(os.environ["SERVER_IP"], os.environ["SERVER_PORT"], N_BACKUP_AGENTS)
            with Pool(processes = N_BACKUP_AGENTS) as poolBackupAgents:
                agentsResponses = []
                for _ in range(random.randint(1, MAX_BACKUPS_UNTIL_UNAVAILABILITY)):
                    backupServer, addr = s.accept()
                    agentsResponses.append(poolBackupAgents.apply_async(backup_agent_controller.main, args = (self.queue, self.hashes,)))
                    self.queue.put(backupServer)
                [res.get() for res in agentsResponses]
            s.close()
