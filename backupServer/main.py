import sys
import os
sys.path.append(os.path.dirname(os.path.abspath('main.py')))
from tools.socket import *
from tools.protocol import *

MAX_CLIENTS = 1
MAX_PERSISTORS = 5
PERSISTOR_PORT = 12346

backupServerSocket = ServerSocket(os.environ["BACKUP_SERVER_IP"], int(os.environ["BACKUP_SERVER_PORT"]), MAX_CLIENTS)

#persistorSocket = ServerSocket(os.environ["BACKUP_SERVER_IP"], PERSISTOR_PORT, MAX_PERSISTORS)
returnAdress = (os.environ["BACKUP_SERVER_IP"], PERSISTOR_PORT)

client, addr = backupServerSocket.accept()

msg = client.receive()
while msg:
    request = OrderRequest(msg, returnAdress)
    server = ClientSocket()
    server.connect(request.get_ip(), request.get_port())
    server.send(request.to_json())
    response = server.receive()
    server.close()
    client.send(response)
    msg = client.receive()

client.close()
backupServerSocket.close()
