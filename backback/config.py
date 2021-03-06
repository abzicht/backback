import os
import json
import yaml
from pathlib import Path

try:
    from backback.util import prompt_
except ImportError:
    from util import prompt_

class Config:

    def __init__(self, duplicity:bool=True, remote: bool=False, passphrase:str=None, deja: bool=True):
        self.remote = remote
        self.passphrase = passphrase
        self.deja = deja
        self.duplicity = duplicity
        with open(os.path.join(str(Path.home()), '.backback/config.yml'), 'r') as config_file:
            self.d = yaml.load(config_file, Loader=yaml.SafeLoader)

    @staticmethod
    def init():
        duplicity  = prompt_('Run duplicity?',default=True)
        deja       = prompt_('Run deja-dup?',default=False)
        remote     = prompt_('Backup from external storage?',default=False)
        passphrase = None

        if remote:
            passphrase = prompt_('Enter ssh passphrase:', is_password=True)

        return Config(passphrase=passphrase, duplicity=duplicity, remote=remote, deja=deja)
