import sys
import os
import time
import random
from multiprocessing import Manager, Pool
import backup_agent_controller
sys.path.append(os.path.dirname(os.path.abspath('main.py')))
from tools.socket import *

SECS_OF_UNAVAILABILITY = 10
MAX_BACKUPS_UNTIL_UNAVAILABILITY = 5
N_BACKUP_AGENTS = 2

manager = Manager()
hashes = manager.dict()
queue = manager.Queue()
while True:
    # Server not available for backups
    time.sleep(SECS_OF_UNAVAILABILITY)
    # Server available
    s = ServerSocket(os.environ["SERVER_IP"], os.environ["SERVER_PORT"], N_BACKUP_AGENTS)
    with Pool(processes = N_BACKUP_AGENTS) as poolBackupAgents:
        agentsResponses = []
        for _ in range(random.randint(1, MAX_BACKUPS_UNTIL_UNAVAILABILITY)):
            backupServer, addr = s.accept()
            agentsResponses.append(poolBackupAgents.apply_async(backup_agent_controller.main, args = (queue,hashes,)))
            queue.put(backupServer)
        [res.get() for res in agentsResponses]
    s.close()
