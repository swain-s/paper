#监听模块：接收连接，并为线程池分配连接


import socket
import threading

import Manager

class Receiver(object):
    def __init__(self):
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

    def init_sever(self):
        self.sever_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sever_socket.setblocking(False)
        self.sever_socket.bind((self.ip, self.port))
        self.sever_threaing = threading.Thread(name="sever", target=self.sever_thread_func)

    def sever_thread_func(self):
        self.sever_socket.listen(self.listen_cnt)
        print("Sever: sever start, ip: %s, port: %d" % (self.ip, self.port))

        MyManager = Manager.Manager()
        MyManager.manager_init()
        MyManager.add_init_theading_pool("sever")

        while True:
            try:
                client_socket, client_ip = self.sever_socket.accept()
            except:
                pass
            else:
                client_socket.setblocking(False)
                MyManager.add_new_connection("sever", client_socket, client_ip)

    def sever_start(self):
        self.sever_threaing.start()

R = Receiver()
R.init_sever()
R.sever_start()