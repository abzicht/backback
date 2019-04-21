import sys
from subprocess import run, PIPE

def run_cmd(cmd, shell: bool=False) -> (str, str):
        result = run(cmd,
                     stderr = PIPE,
                     shell  = shell,
                     universal_newlines=True,
                     check  = False)
        output = result.stdout
        err    = result.stderr
        return output, err
