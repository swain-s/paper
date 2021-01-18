import time

#**************** TYPE ***************************
# type : order plus type
class OrderType(object):
    def __init__(self):
        self.unknown = 0
        self.sql = 1
        self.shell = 2
        self.ex_sql = 3
        self.config = 4
        self.my_order = 5
        self.formal = 6

# type : exec type
class ExecType(object):
    def __init__(self):
        self.parallel = 0
        self.serial = 1

#***************** Event **********************
# struct : subject

on = 1
off = 0
class Subject(object):
    def __init__(self, name, ip, port, status):
        self.name = name
        self.ip = ip
        self.port  = port
        self.status = status
        self.sock = None

# struct : order plus
class OrderPlus(object):
    def __init__(self, src_order_type, src_order):
        self.src_order_type = src_order_type
        self.src_order = src_order
        self.next = None
        self.dest_order_type = None
        self.dest_orde_list = None
        self.exec_type = None # ExecType
        self.gsql_path = None
        self.gsql_arg = None

# struct : status
class Status(object):
    def __init__(self):
        self.status_list = []
        self.timestamp_list = []

    def refresh(self, status):
        self.status_list.append(status)
        self.timestamp_list.append(time.strftime("%Y:%m:%d", time.localtime()))

# struct : event
class Event(object):
    def __init__(self):
        self.type = None
        self.status = None
        self.src_obj = None # Subject
        self.dest_obj = None
        self.order_plus = None # OrderPlus
        self.result_list = None