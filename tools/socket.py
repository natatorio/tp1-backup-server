import socket


class Socket:
    def __init__(self, sock = None):
        if sock:
            self.socket = sock
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, msg):
        return self.socket.sendall(msg.encode())

    def receive(self):
        return self.socket.recv(4096).decode()


class ServerSocket(Socket):
    def __init__(self, ip, port, max_connections):
        super(ServerSocket, self).__init__()
        self.socket.bind((ip, port))
        self.socket.listen(max_connections)

    def accept(self):
        socket, address = self.socket.accept()
        return Socket(socket), address


class ClientSocket(Socket):
    def __init__(self):
        super(ClientSocket, self).__init__()

    def connect(self, ip, port):
        self.socket.connect((ip, port))
