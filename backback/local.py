import sys, os
from subprocess import run, Popen, PIPE

try:
    from backback.backup import Backup
    from backback.util import run_cmd
except ImportError:
    from backup import Backup
    from util import run_cmd

class Local(Backup):

    def __init__(self, folder: str, target: str):
        self.folder  = folder
        self.target  = target

    def __backup__(self):
        cmd = (["rsync", "-avrtlzp", self.folder, self.target])
        return run_cmd(cmd)

    def __str__(self):
        return "LOCAL: {} -> {}".format(self.folder, self.target)
