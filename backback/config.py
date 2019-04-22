import os
import json
from pathlib import Path
from prompt_toolkit import prompt

class Config:

    def __init__(self, passphrase:str, external: bool=False, deja: bool=True):
        self.external = external
        self.passphrase = passphrase
        self.deja = deja
        with open(os.path.join(str(Path.home()), '.backback/config.json'), 'r') as config_file:
            self.d = json.load(config_file)

    @staticmethod
    def init():
        deja       = prompt('Run deja-dup? (Y/n) ')
        external   = prompt('Backup to external storage? (y/N) ')
        passphrase = prompt('Enter ssh passphrase (~/.ssh/id_rsa or similar): ', is_password=True)

        deja       = True if len(deja) == 0 or deja.lower() == 'y' else False
        external   = False if len(external) == 0 or external.lower() == 'n' else True
        passphrase = None if passphrase is None or len(passphrase) == 0 else passphrase
        return Config(passphrase, external=external, deja=deja)
