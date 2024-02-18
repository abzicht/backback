try:
    from backback.shell import Rankshell
    from backback.util import sort_by_rank
except ImportError:
    from shell import Rankshell
    from util import sort_by_rank

class ShellManager:
    """
    A manager for multiple Rankshells of different ranks.
    Provides functions for sorting procedures into the correct rank and
    executing shells by the order of their rank.
    """

    def __init__(self):
        self.shells = []

    def add(self, procedure):
        """
        Adds a new procedure to the shell with the correct rank.
        """
        for shell in self.shells:
            if shell.rank == procedure.rank:
                shell.add_procedure(procedure)
                return
        shell = Rankshell(procedure.rank)
        shell.add_procedure(procedure)
        self.shells.append(shell)

    def execute(self):
        """
        Runs all shells in order of their rank.
        """
        self.shells = sort_by_rank(self.shells)
        for shell in self.shells:
            shell.run()

    def verbose_list(self) -> str:
        """
        Gives an overview of all shells, ranked.
        """
        str_ = '┌Scheduled procedures (ordered by execution order)\n'
        self.shells = sort_by_rank(self.shells)
        for i, shell in enumerate(self.shells):
            char = '├'
            if i == len(self.shells) - 1:
                char = '└'
            shell_lines = str(shell).splitlines()
            if len(shell_lines)<=1:
                continue
            str_ += char + shell_lines[0] + '\n'
            if i == len(self.shells) - 1:
                char = ' '
            else:
                char = '│'
            for line in shell_lines[1:]:
                str_ += char + line + '\n'
        return str_
