import sys, os

try:
    from backback.backup import Backup
    from backback.util import run_cmd
except ImportError:
    from backup import Backup
    from util import run_cmd

class Remote(Backup):

    def __init__(self,
                 user:       str,
                 address:    str,
                 passphrase: str,
                 folders:    list,
                 target:     str,
                 port:       int=22):
        self.user       = user
        self.address    = address
        self.passphrase = passphrase
        self.folders    = folders
        self.target     = target
        self.port       = port

    def __backup__(self):
        cmd = []
        if self.passphrase is not None:
            cmd  = ["sshpass"]
            cmd += ["-P", "passphrase",
                    "-p", self.passphrase]
        cmd += ["rsync", "-avrtlzp"]
        for folder in self.folders:
            cmd.append("{}@{}:{}".format(self.user, self.address, folder))
        cmd.append(self.target)
        cmd = ' '.join(cmd)
        return run_cmd(cmd, shell=True)

    def __str__(self):
        return "REMOTE: {} -> {}".format(self.folders, self.target)
