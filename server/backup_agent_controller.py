import sys
import os
import json
import hashlib
import tarfile
from datetime import datetime
from checksumdir import dirhash
sys.path.append(os.path.dirname(os.path.abspath('main.py')))
from tools.socket import *

BACKUP_FILENAME = "backup.tgz"
DATA_ROOTDIR = "Data"

def main(queue, hashes):
    backupServer = queue.get()
    path = backupServer.receive()
    path = os.path.join(DATA_ROOTDIR, path)
    size = 0
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
    response = {"datetime" : datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
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
