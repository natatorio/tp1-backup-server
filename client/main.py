import sys
import os
sys.path.append(os.path.dirname(os.path.abspath('main.py')))
from tools.socket import *

socket = ClientSocket()

socket.connect("127.0.0.1",12345)

while True:
    socket.send(input())
    print(socket.receive())
