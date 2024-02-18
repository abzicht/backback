import threading
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s (%(levelname)s): %(message)s')

class BackupThread(threading.Thread):
    """
    Helper class for running single backup procedures in extra threads.
    """
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
        logging.info("Backup finished: {}".format(self.procedure))

    def __str__(self):
        return str(self.procedure)



class Rankshell:
    """
    This class represents all backup procedures of the same rank.
    Use "add_procedure" initially and use "run" to start all registered
    procedures in parallel. "str(Rankshell)" gives a visual overview of the
    registered procedures.
    """

    def __init__(self, rank: int):
        self.rank = rank
        self.procedures = []

    def add_procedure(self, procedure):
        """
        Add another procedure to the shell. The procedure class must implement
        a function of syntax "backup() -> output, error"
        """
        if self.rank != procedure.rank:
            raise ValueError("Procedure rank {} does not match shell rank {}".format(procedure.rank, self.rank))
        self.procedures.append(procedure)

    def run(self):
        """
        Run all procedures in parallel using the
        "BackupThread" class.
        """
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
