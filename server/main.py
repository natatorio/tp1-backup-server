import sys
import os
import json
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath('main.py')))
from tools.socket import *

MAX_CLIENTS = 1

s = ServerSocket(os.environ["SERVER_IP"], os.environ["SERVER_PORT"], MAX_CLIENTS)

while True:
    backupServer, addr = s.accept()
    request = backupServer.receive()
    #   generate backup
    dtime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    size = "10MB"
    tgz = None
    response = {"datetime": dtime, "size": size, "tgz": tgz}
    backupServer.send(json.dumps(response))
    backupServer.close()
