import os
import json
import yaml
from pathlib import Path
import argparse

try:
    from backback.util import prompt_
except ImportError:
    from util import prompt_

class Config:

    def __init__(self, config_file, duplicity:bool=True, remote: bool=False, passphrase:str=None, deja: bool=True):
        config_file = config_file
        self.remote = remote
        self.passphrase = passphrase
        self.deja = deja
        self.duplicity = duplicity
        with open(config_file, 'r') as config_file:
            self.d = yaml.load(config_file, Loader=yaml.SafeLoader)

    @staticmethod
    def args():
        parser = argparse.ArgumentParser()
        parser.add_argument('--duplicity', dest='duplicity', help='Run duplicity. Default: True',
                action='store_true', default=True)
        parser.add_argument('--deja-dup', dest='deja_dup', help='Run Deja-Dup. Default: False',
                action='store_true', default=False)
        parser.add_argument('--remote', dest='remote', help='Backup from remote. Default: False',
                action='store_true', default=False)
        parser.add_argument('-c', '--config-file', dest='config_file',
                help='A backback config file. If not specified, ~/.backback/config.yml is used', type=str,
                default=os.path.join(str(Path.home()), '.backback/config.yml'))
        return parser.parse_args()

    @staticmethod
    def init():
        args = Config.args()
        passphrase = None

        if args.remote:
            passphrase = prompt_('Enter ssh passphrase:', is_password=True)

        return Config(config_file=args.config_file, passphrase=passphrase,
                duplicity=args.duplicity,
                remote=args.remote, deja=args.deja_dup)
