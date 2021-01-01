import socket
import threading

from subject_type import Master, Puppet, Server

master = Master("master")

puppet_list = [
    Puppet("puppet a", "127.0.0.1", "2222"),
    Puppet("puppet b", "127.0.0.1", "3333")
]

server = Server("server", "127.0.0.1", "4444", "127.0.0.1", "5555")


class MasterInfo(object):
    def __init__(self):
        self.name = None
        self.host = None

        self.sock = None
        self.order_list = []

class PuppetPlus(Puppet):
    def __init__(self, name, office, station):
        super(Puppet).__init__(name, office, station)
        self.sock = None
        self.env = None

        self.master_list = []
        self.max_master_num  = 5

    def start_work(self):
        self.init_env()

        self.sock = socket.socket()
        self.sock.listen(self.max_master_num)

        while True:
            master = MasterInfo()
            (master.sock, master.host) = self.sock.accept()


    def init_env(self):
        pass

    def open_ear(self):
        self.ear = socket.socket()
        self.ear.listen(self.max_master_num)

    def there_come_a_master(self):
        a_master = MasterInfo()
        (a_master.ear, a_master.addr) = self.ear.accept()
        return a_master

    def what_is_your_name(self, master):
        master.name = master.ear.recv(1024)

    def tell_me_what_to_do(self, master):
        kunkun = threading.Thread(name="kunkun", target=self.kunkun_task, args=(self.task_list))
        kunkun.start()

    def kunkun_task(self, master, task_list):
        while True:
            pass

    def _start_work(self):
        self.ear = socket.socket()
        self.ear.listen(self.max_master_num)
        while True:
            a_master = MasterInfo()
            (a_master.ear, a_master.addr) = self.ear.accept()

            a_master.name = self.what_is_your_name(a_master.ear)

            while True:
                message = self.ear.recv(1024)

    def _what_is_your_name(self, master_ear):
        my_name = master_ear.recv(1024)
        return my_name

class MasterPlus(Master):
    def __init__(self, name):
        super(Master).__init__(name)
        self.puppet_con = []

    def func(self):
        pass
