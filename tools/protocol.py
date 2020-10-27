import json
import os

MAX_ARGS = 4
EXIT_REQUEST = "exit"
QUERY_REQUEST = "query"
REGISTER_REQUEST = "register"
UNREGISTER_REQUEST = "unregister"

class Request:
    def __init__(self, json):
        self.type = json["type"]
        self.ip = json["ip"]
        self.port = json["port"]
        self.path = json["path"]
        self.rate = json["rate"]

    def to_json(self, ret = {}):
        ret["type"] = self.type
        ret["ip"] = self.ip
        ret["port"] = self.port
        ret["path"] = self.path
        ret["rate"] = self.rate
        return json.dumps(ret)

    def get_ip(self):
        return self.ip

    def get_port(self):
        return int(self.port)

class OrderRequest(Request):
    def __init__(self, argJson, returnAdress):
        self.returnIp = returnAdress[0]
        self.returnPort = returnAdress[1]
        super(OrderRequest, self).__init__(json.loads(argJson))
        if self.type == UNREGISTER_REQUEST:
            self.rate = "0"

    def returnIp(self):
        return self.returnIp

    def returnPort(self):
        return int(self.returnPort)

    def to_json(self):
        ret = {}
        ret["returnIp"] = self.returnIp
        ret["returnPort"] = self.returnPort
        return super(OrderRequest, self).to_json(ret)

class ClientRequest(Request):
    def __init__(self, str):
        args = str.split()
        args += [''] * MAX_ARGS
        args = args[:MAX_ARGS]
        self.type = args[0]
        try:
            self.ip = os.environ["SERVER_{}_IP".format(args[1])]
            self.port = os.environ["SERVER_{}_PORT".format(args[1])]
        except:
            self.ip = None
        self.path = args[2]
        self.rate = args[3]

    def is_valid(self):
        if self.type not in [EXIT_REQUEST, QUERY_REQUEST, REGISTER_REQUEST, UNREGISTER_REQUEST]: return False
        if not self.ip: return False
        if not self.path: return False
        if self.type == REGISTER_REQUEST:
            if (not self.rate.isdigit()) or int(self.rate) < 1: return False
        return True

    def is_exit(self):
        return self.type == EXIT_REQUEST
