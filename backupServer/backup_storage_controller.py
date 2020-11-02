import os
from pathlib import Path

BACKUP_STORAGE_ROOTDIR = "BackupStorage"
LAST_BACKUP_FILENAME = "last.txt"
BACKUP_FILENAME_EXTENSION = ".tgz"
N_BACKUPS = 10

class BackupStorageController:
    def __init__(self, ip, path, rootDir = BACKUP_STORAGE_ROOTDIR, nBackups = N_BACKUPS):
        self.nBackups = nBackups
        self.backupsDir = os.path.join(rootDir, ip, path)
        self.lastBackupRegisterFilename = os.path.join(self.backupsDir, LAST_BACKUP_FILENAME)
        Path(self.backupsDir).mkdir(parents = True, exist_ok = True)
        if os.path.exists(self.lastBackupRegisterFilename):
            with open(self.lastBackupRegisterFilename, "r") as f:
                self.last = f.read()
        else:
            self.last = str(self.nBackups - 1)

    def open(self):
        backupFilename = os.path.join(self.backupsDir, self.__next_in_cycle() + BACKUP_FILENAME_EXTENSION)
        return open(backupFilename, "wb")

    def close(self, f):
        f.close()
        with open(self.lastBackupRegisterFilename, "w") as f:
            f.write(self.__next_in_cycle())

    def __next_in_cycle(self):
        return str((int(self.last) + 1) % self.nBackups)
