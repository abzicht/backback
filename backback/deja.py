try:
    from backback.backup import Backup
    from backback.util import run_cmd
except ImportError:
    from backup import Backup
    from util import run_cmd

class Deja(Backup):

    def __backup__(self):
        cmd = (["deja-dup", "--backup"])
        return run_cmd(cmd)

    def __str__(self):
        return "DEJA-DUP: deja-dup --backup"
