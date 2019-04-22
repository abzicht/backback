import sys
from subprocess import run, PIPE

def run_cmd(cmd, shell: bool=False) -> (str, str):
        result = run(cmd,
                     stdout = PIPE,
                     stderr = PIPE,
                     shell  = shell,
                     universal_newlines=True,
                     check  = False)
        output = result.stdout
        err    = result.stderr
        return output, err

def sort_by_rank(shells: list) -> list:
    return sorted(shells, key = lambda x: x.rank, reverse = False)
