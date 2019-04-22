import sys, os

try:
    import backback.backup as backup
    from backback.util import run_cmd
except ImportError:
    import backup
    from util import run_cmd

class Local(backup.Backup):

    def __init__(self, rank: int, from_: str, to_: str):
        super().__init__(rank)
        self.from_ = from_ 
        self.to_   = to_

    @staticmethod
    def init(config_dict: dict):
        return Local(
                rank       = config_dict['rank'],
                from_      = config_dict['from'],
                to_        = config_dict['to'],
                )

    def __backup__(self):
        cmd = (["rsync", "-avrtlzp", self.from_, self.to_])
        return run_cmd(cmd)

    def __str__(self):
        return "LOCAL: {} -> {}".format(self.from_, self.to_)
