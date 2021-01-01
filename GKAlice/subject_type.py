class Master(object):
    def __init__(self, name):
        self.name = name

class Puppet(object):
    def __init__(self, name, host, port):
        self.name = name
        self.host = host
        self.port = port

class Server(object):
    def __init__(self, name, host, port, db_host, db_port):
        self.name = name
        self.host = host
        self.host = port
        self.db_host = db_host
        self.db_port = db_port