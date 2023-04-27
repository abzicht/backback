import threading 
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s (%(levelname)s): %(message)s')

try:
    from backback.util import sort_by_rank 
except ImportError:
    from util import sort_by_rank 

class BackupThread(threading.Thread):
    def __init__(self, procedure):
        super().__init__()
        self.procedure = procedure

    def run(self):
        logging.info("Backup started: {}".format(self.procedure))
        output, err = self.procedure.backup()
        if output is not None and len(output) != 0:
            logging.debug(output)
        if err is not None and len(err) != 0:
            logging.warning(err)

    def __str__(self):
        return str(self.procedure)



class Rankshell:

    shells = []

    def __init__(self, rank: int):
        self.rank = rank
        self.procedures = []

    def add_procedure(self, procedure):
        if self.rank != procedure.rank:
            raise ValueError("Procedure rank {} does not match shell rank {}".format(procedure.rank, self.rank))
        self.procedures.append(procedure)

    def run(self):
        threads = []
        for procedure in self.procedures:
            thread = BackupThread(procedure)
            threads.append(thread)
            thread.start()
        for thread in threads:
            logging.info("Waiting for thread of rank {} to join: {}".format(self.rank, thread))
            try:
                thread.join()
            except KeyboardInterrupt:
                logging.warning("Waiting for thread KILLED by SIGINT. Thread becomes unmanaged")
            logging.info("Thread of rank {} has joined: {}".format(self.rank, thread))

    def __str__(self):
        str_ = '┬#{}\n'.format(self.rank)
        for i, procedure in enumerate(self.procedures):
            char = '├'
            newline = '\n'
            if i == len(self.procedures) - 1:
                char = '└'
                newline = ''
            str_+= char + str(procedure) + newline 
        return str_


    @staticmethod
    def add(procedure):
        for shell in Rankshell.shells:
            if shell.rank == procedure.rank:
                shell.add_procedure(procedure)
                return
        shell = Rankshell(procedure.rank)
        shell.add_procedure(procedure)
        Rankshell.shells.append(shell)

    @staticmethod
    def execute():
        Rankshell.shells = sort_by_rank(Rankshell.shells)
        for shell in Rankshell.shells:
            shell.run()

    @staticmethod
    def verbose_list() -> str:
        str_ = '┌Scheduled procedures (ordered by execution order)\n'
        Rankshell.shells = sort_by_rank(Rankshell.shells)
        for i, shell in enumerate(Rankshell.shells):
            char = '├'
            if i == len(Rankshell.shells) - 1:
                char = '└'
            shell_lines = str(shell).splitlines()
            if len(shell_lines)<=1:
                continue
            str_ += char + shell_lines[0] + '\n'
            if i == len(Rankshell.shells) - 1:
                char = ' '
            else:
                char = '│'
            for line in shell_lines[1:]:
                str_ += char + line + '\n'
        return str_
