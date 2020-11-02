import sys
import os
import json
import tarfile
import hashlib
import random
from datetime import datetime
from checksumdir import dirhash
sys.path.append(os.path.dirname(os.path.abspath('main.py')))
from tools.socket import *

MAX_CLIENTS = 1
BACKUP_FILENAME = "backup.tgz"
ONE_MB = 1024
DATA_ROOTDIR = "Data"
PROBABILITY = 0.5

s = ServerSocket(os.environ["SERVER_IP"], os.environ["SERVER_PORT"], MAX_CLIENTS)
hashes = {}
while True:
    backupServer, addr = s.accept()
    path = backupServer.receive()
    path = os.path.join(DATA_ROOTDIR, path)
    available = random.random() < PROBABILITY
    response = {'available': available}
    size = 0
    if available:
        if os.path.isdir(os.path.abspath(path)):
            hash = dirhash(path, 'md5')
        else:
            with open(os.path.abspath(path), "rb") as f:
                hash = hashlib.md5()
                while chunk := f.read(ONE_MB):
                    hash.update(chunk)
            hash = hash.hexdigest()
        if hash != hashes.get(path, ""):
            hashes[path] = hash
            if os.path.exists(BACKUP_FILENAME): os.remove(BACKUP_FILENAME)
            with tarfile.open(BACKUP_FILENAME, "w:gz") as tar:
                tar.add(path, arcname=os.path.basename(path))
            size = os.path.getsize(BACKUP_FILENAME)
        response["datetime"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        response["size"] = size
    backupServer.send(json.dumps(response))
    if size > 0:
        backupServer.receive()
        with open(BACKUP_FILENAME, "rb") as f:
            data = f.read(ONE_MB)
            while (data):
                backupServer.send_bin(data)
                data = f.read(ONE_MB)
    backupServer.close()
