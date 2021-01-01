import socket
import time

from type import *

class ListenThread(object):
    def __init__(self):
        pass

class ConnectPool(object):
    def __init__(self):
        self.pool = []

    def add_subject(self, new_subj):
        for subj in self.pool:
            if subj.name == new_subj.name:
                print("ERROR: %s has exists." % new_subj.name)
                new_subj.sock.send("double connect")
                new_subj.sock.close()
                return
        self.pool.append(new_subj)

    def find_subject(self, subj_name):
        for subj in self.pool:
            if subj.name == subj_name:
                return subj

class MainConsole(object):
    def __init__(self):
        self.ip = None
        self.port = None
        self.listener = None

        self.connect_pool = ConnectPool()

    def start(self):
        self.listener = socket.socket()
        self.listener.setblocking(False)
        self.listener.bind((self.ip, self.port))
        self.listener.listen(5)

        while True:
            try:
                (sock, ip) = self.listener.accept()
                master = Subject()
                master.sock = sock
                master.sock.setblocking(False)
                master.ip = ip
                master.name = master.sock.recv(1024)
                self.connect_pool.add_subject(master)
            except:
                time.sleep(2)
            else:
                try:
                    for conn in self.connect_pool.pool:
                        message = conn.sock.recv(1024)
                        order_plus = OrderPlus()
                        order_plus =


