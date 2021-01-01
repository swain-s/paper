import threading
import time

class P(object):
    def __init__(self):
        self.thread = None

    def func(self):
        cnt = 1
        while True:
            print("++++++", cnt)
            time.sleep(2)
            cnt += 1

    def start(self):
        self.thread = threading.Thread(target=self.func)
        self.thread.start()

        c = C()
        c.start()


class C(object):
    def __init__(self):
        self.thread = None
        self.se = threading.Semaphore(0)

    def func(self):
        cnt = 1
        while True:
            self.se.acquire()
            print("------", cnt)
            time.sleep(2)
            cnt += 1

    def start(self):
        self.thread = threading.Thread(target=self.func)
        self.thread.start()

p = P()
p.start()

#监听模块：接收连接，并为线程池分配连接


import socket
import threading

import Manager

class Receiver(object):
    def __init__(self):
        self.sever_threaing = None
        self.sever_threaing = None
        self.hostname = ""
        self.ip = ""
        self.port = 0

        self.sever_socket = None
        self.listen_cnt = 0

        self.semaphore_m2r = threading.Semaphore(1)

    def config(self):
        #self.hostname = socket.getfqdn(socket.gethostname())
        #self.ip = socket.gethostbyname(self.hostname)
        self.ip = "192.168.1.100"
        self.port = 559
        self.listen_cnt = 5

        return 0

    def init_sever(self):
        if self.config() != 0:
            print("socket_init_error")

        self.sever_threaing = threading.Thread(name="sever", target=self.sever_start())
        self.sever_threaing.start()

        return self.sever_socket

    def sever_start(self):
        self.sever_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sever_socket.bind((self.ip, self.port))

        self.sever_socket.listen(self.listen_cnt)
        print("Sever: sever start, ip: %s, port: %d" % (self.ip, self.port))

        MyManager = Manager.Manager()
        MyManager.manager_init()
        print("start...")
        MyManager.add_init_theading_pool("sever")
        MyManager.semaphore.release()

        while True:
            client_socket, client_ip = self.sever_socket.accept()
            MyManager.add_new_connection("sever", client_socket, client_ip)
            MyManager.semaphore.release()

R = Receiver()
R.init_sever()
R.sever_start()