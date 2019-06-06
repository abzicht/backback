
class Backup():

    def __init__(self, rank):
        self.rank = rank

    def backup(self) -> (str, str):
        try:
            return self.__backup__()
        except KeyboardInterrupt as err:
            return None, "KILLED by SIGINT"

    def __backup__(self) -> (str, str):
        return None, None

    def __repr__(self):
        return 'backup #{}'.format(self.rank)
