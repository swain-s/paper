import threading
import datetime

class TheadInfo(object):
    def __init__(self, thread_name, func, args):
        self.name = thread_name
        self.start_time = None
        self.reply_time = None
        self.thread = self.init_thread(thread_name, func, args)

    def init_thread(self, thread_name, func, args):
        thread = threading.Thread(name=thread_name, target=func, args=())
        thread.start()
        self.start_time = datetime.datetime.now()
        self.reply_time = datetime.datetime.now()
        return thread

class ThreadPool(object):
    def __init__(self):
        self.thread_pool = []

    def apply_thread(self, thread_name, func, args):
        new_thread = TheadInfo(thread_name, func, args)
        self.thread_pool.append(new_thread)

