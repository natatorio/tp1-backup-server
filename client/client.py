import sys
import os
sys.path.append(os.path.dirname(os.path.abspath('client.py')))
from tools.socket import *
from tools.protocol import *


class Client:
    def __init__(self):
        self.socket = ClientSocket()

    def run(self):
        try:
            self.socket.connect(os.environ["BACKUP_SERVER_IP"], os.environ["BACKUP_SERVER_PORT"])
        except:
            print("Error connecting to backup server")
            self.socket.close()
            exit()

        print("Connected to server")
        print("Listening request of one of the following types:")
        print("query [server id] [path]")
        print("register [server id] [path] [rate]")
        print("unregister [server id] [path]")
        request = ClientRequest(input())
        while not request.is_exit():
            if request.is_valid():
                self.socket.send(request.to_json())
                print(self.socket.receive())
            else:
                print("Invalid request. Try again")
            request = ClientRequest(input())
        socket.close()
