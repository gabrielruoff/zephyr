
class Service:
    def __init__(self):
        pass

    def __enter__(self):
        self.__init__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def _detect_running(self):
        return True

    def start(self):
        pass

    def stop(self):
        pass