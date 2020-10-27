import sys
import os
sys.path.append(os.path.dirname(os.path.abspath('main.py')))
from tools.socket import *

MAX_CLIENTS = 1

s = ServerSocket(os.environ["SERVER_IP"], int(os.environ["SERVER_PORT"]), MAX_CLIENTS)

while True:
    backupServer, addr = s.accept()
    request = backupServer.receive()
    #register back up order
    response = "Order {} registered OK".format(request)
    backupServer.send(response)
    backupServer.close()
