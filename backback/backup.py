
class Backup:
    
    def __init__(self):
        pass

    def backup(self) -> (str, str):
        try:
            return self.__backup__()
        except KeyboardInterrupt as err:
            return None, "KILLED by SIGINT"

    def __backup__(self) -> (str, str):
        return None, None
