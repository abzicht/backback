try:
    import backback.backup as backup
    from backback.util import run_cmd
except ImportError:
    import backup
    from util import run_cmd

class Deja(backup.Backup):

    def __init__(self, config_dict: dict):
        super().__init__(config_dict['rank'])

    def __backup__(self):
        cmd = (["deja-dup", "--backup"])
        return run_cmd(cmd)

    def __str__(self):
        return "DEJA-DUP: deja-dup --backup"
