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
        self.master = Subject("my name", "127.0.0.1", 5555, None)
        self.recv_con_pool = ConnectPool()
        self.send_con_pool = ConnectPool()
        self.order_plus_queue = []
        self.cur_client = None
        self.order_parse = OrderPlus()

    def start_listen_thread(self):
        self.master.sock = socket.socket()
        self.master.sock.setblocking(False)
        self.master.sock.bind((self.master.ip, self.master.port))
        self.master.sock.listen(5)

        while True:
            try:
                (sock, ip) = self.master.sock.accept()
                src_master = Subject(None, ip, None, sock)
                src_master.sock.setblocking(False)
                src_master.name = src_master.sock.recv(1024)
                self.recv_con_pool.add_subject(src_master)
            except:
                time.sleep(2)
                try:
                    for subject in self.recv_con_pool.pool:
                        message = subject.sock.recv(1024)


            else:

    def parse_thread_start(self):
        pass

    def start_conn_thread(self):
        pass