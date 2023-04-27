import sys, os

try:
    import backback.backup as backup
    from backback.util import run_cmd
except ImportError:
    import backup
    from util import run_cmd
    from util import mkdirs

class Manual(backup.Backup):

    def __init__(self, rank: int, cmd:list=[]):
        super().__init__(rank)
        self.cmd = cmd

    @staticmethod
    def init(config_dict: dict):
        return Manual(
                rank = config_dict['rank'],
                cmd  = config_dict['cmd'],
                )

    def __backup__(self):
        cmd = (self.cmd)
        return run_cmd(cmd)

    def __str__(self):
        return "MANUAL: {}".format(' '.join(self.cmd))
