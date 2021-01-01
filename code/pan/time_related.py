import time

class Time(object):
    def __init__(self):
        pass

    def current_time(self):
        standard_time = time.time()
        local_time = time.asctime(time.localtime(standard_time))
        return local_time