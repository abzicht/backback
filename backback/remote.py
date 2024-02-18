import sys, os

try:
    import backback.backup as backup
    from backback.util import run_cmd
    from backback.util import mkdirs
except ImportError:
    import backup
    from util import run_cmd
    from util import mkdirs

class Remote(backup.Backup):

    def __init__(self,
                 rank:       int,
                 user:       str,
                 address:    str,
                 passphrase: str,
                 folders:    list,
                 target:     str,
                 port:       int=22,
                 options:list = None):
        super().__init__(rank)
        self.user       = user
        self.address    = address
        self.passphrase = passphrase
        self.folders    = folders
        self.target     = target
        self.port       = port
        self.options    = options if options is not None else ['-avz', '--delete-during']

    @staticmethod
    def init(config_dict: dict, passphrase):
        return Remote(
                rank       = config_dict['rank'],
                user       = config_dict['user'],
                address    = config_dict['address'],
                passphrase = passphrase,
                folders    = config_dict['folders'],
                target     = config_dict['internal'],
                port       = config_dict['port'] if 'port' in config_dict else 22,
                options    = config_dict['options'] if 'options' in config_dict else None,
                )

    def __backup__(self):
        cmd = []
        if self.passphrase is not None:
            cmd  = ["sshpass"]
            cmd += ["-P", "passphrase",
                    "-p", self.passphrase]
        cmd += ["rsync"]
        cmd += self.options
        for folder in self.folders:
            cmd.append("{}@{}:{}".format(self.user, self.address, folder))
        cmd += [self.target]
        cmd += ["--rsh='ssh -p{}'".format(self.port)]
        cmd = ' '.join(cmd)
        mkdirs(self.target)
        return run_cmd(cmd, shell=True)

    def __str__(self):
        return "REMOTE: {}@{} {} -> {}".format(self.user, self.address, self.folders, self.target)
