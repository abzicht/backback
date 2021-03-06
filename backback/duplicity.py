import sys, os

try:
    import backback.backup as backup
    from backback.util import run_cmd
    from backback.util import mkdirs
except ImportError:
    import backup
    from util import run_cmd
    from util import mkdirs

class Duplicity(backup.Backup):

    def __init__(self, rank: int, to_:str, from_:str=None, options:list=[]):
        super().__init__(rank)
        self.from_ = from_
        self.to_   = to_
        self.options = options

    @staticmethod
    def init(config_dict: dict):
        return Duplicity(
                rank       = config_dict['rank'],
                from_      = config_dict['from'] if 'from' in config_dict else None,
                to_        = config_dict['to'],
                options    = config_dict['options'],
                )

    def __backup__(self):
        args = ['duplicity']
        args += self.options
        if self.from_:
            args.append(self.from_)
        args.append(self.to_)
        cmd = (args)
        mkdirs(self.to_)
        return run_cmd(cmd)

    def __str__(self):
        return "DUPLICITY: {} {} -> {}".format(' '.join(self.options), self.from_, self.to_)
