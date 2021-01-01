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
class Subject(object):
    def __init__(self):
        self.name = None
        self.ip = None
        self.port  = None
        self.sock = None

# struct : order plus
class OrderPlus(object):
    def __init__(self):
        self.exec_client = None
        self.type = None # OrderType
        self.exec_type = None # ExecType
        self.order_list = None
        self.tans_order_list = None
        self.gsql_path = None
        self.gsql_arg = None

# struct : event
class Event(object):
    def __init__(self):
        self.type = None
        self.status_list = []
        self.timestamp_list = []
        self.src_obj = None # Subject
        self.order_plus = None # OrderPlus
        self.result_list = None