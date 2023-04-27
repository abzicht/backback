import sys
from subprocess import run, PIPE
from prompt_toolkit import prompt

def mkdirs(directory: str, shell: bool=False):
    cmd = (["mkdir", "-p", directory])
    run_cmd(cmd)

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

def prompt_(question, is_password:bool=False, default:bool=True):
    if not is_password:
        if default:
            question += ' (Y/n) '
        else:
            question += ' (y/N) '
    else:
        question += ' '
    answer = prompt(question, is_password=is_password)
    if is_password:
        return answer
    if default:
        return True  if len(answer) == 0 or answer.lower() == 'y' else False
    else:
        return False if len(answer) == 0 or answer.lower() == 'n' else True
