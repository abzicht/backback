import sys, os

try:
    import backback.backup as backup
    from backback.util import run_cmd
    from backback.util import mkdirs
except ImportError:
    import backup
    from util import run_cmd
    from util import mkdirs

class Local(backup.Backup):

    def __init__(self, rank: int, from_: str, to_: str, options:list=['-avrtlzzp']):
        super().__init__(rank)
        self.from_ = from_ 
        self.to_   = to_
        self.options = options if options is not None else ['-avrtlzzp']

    @staticmethod
    def init(config_dict: dict):
        return Local(
                rank       = config_dict['rank'],
                from_      = config_dict['from'],
                to_        = config_dict['to'],
                options    = config_dict['options'] if 'options' in config_dict else None,
                )

    def __backup__(self):
        args = ['rsync']
        args += self.options
        args.append(self.from_)
        args.append(self.to_)
        cmd = (args)
        mkdirs(self.to_)
        return run_cmd(cmd)

    def __str__(self):
        return "LOCAL: {} -> {}".format(self.from_, self.to_)
