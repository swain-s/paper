#强制访问控制模块

class AccessEvent(object):
    def __init__(self):
        self.thread_level = 0

        self.date_base = ""
        self.table = ""

        self.operation = ""
        self.date = ""

class AccessControl(object):
    def __init__(self):
        self.access_threading = None

        self.access_queue = []
        self.MySQL = None

    def add_insert_event(self):
        pass

    def add_select_event(self):
        pass