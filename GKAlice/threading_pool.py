import threading

class TaskThread(object):
    def __init__(self):
        self.name = None
        self.func = None
        self.func_arg = None
        self.thread = None

class ThreadPool(object):
    def __init__(self):
        self.thread_cnt = 0
        self.thread_list = []

    def init_thread_pool(self):
