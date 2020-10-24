import sys
import os
sys.path.append(os.path.dirname(os.path.abspath('main.py')))
from tools.socket import *

socket = ServerSocket("127.0.0.1",12345, 10)

conn, addr = socket.accept()

print("Got connection from ", addr)
while True:
    msg = conn.receive()
    print("Message form ", addr, " saying: ", msg)
    response = "Received: " + msg
    conn.send(response)
