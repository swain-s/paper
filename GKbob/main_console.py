import socket
import time
import os
import struct
import sys
import getopt
import config as cfg
from thread_pool import *

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
        return None

class MainConsole(object):
    def __init__(self):
        self.my_role = None
        self.recv_con_pool = ConnectPool()
        self.send_con_pool = ConnectPool()
        self.order_plus_queue = []
        self.cur_client = None
        self.conn_pool = []
        #self.order_parse = OrderPlus()
        self.order_list = []
        self.has_open_file = False
        self.thread_pool = ThreadPool()

    def start_up(self):
        is_user_working = (cfg.order_file != None)
        if is_user_working:
            if not cfg.is_single_node:
                for subject in cfg.subject_list:
                    if subject.status is on:
                        if not self.my_role:
                            self.my_role = subject
                        else:
                            self.conn_pool.append(subject)
                self.start_conn_thread()
                self.start_listen_thread()

            self.start_read_order_thread(cfg.order_file)
            self.parse_thread_start()
        else:
            self.start_listen_thread()

    def start_conn_thread(self):
        for subject in self.conn_pool:
            try:
                subject.sock.connect((subject.ip, int(subject.port)))
                subject.status = on
            except:
                print("Failed to connect %s." % subject.name)

    def start_listen_thread(self):
        self.thread_pool.apply_thread("listen thread", self.listen_thread, None)

    def listen_thread(self):
        self.my_role.sock = socket.socket()
        self.my_role.sock.setblocking(False)
        self.my_role.sock.bind((self.my_role.ip, self.my_role.port))
        self.my_role.sock.listen(5)

        print("server start listening ", end="")
        while True:
            try:
                print(".", end="")
                (sock, ip) = self.my_role.sock.accept()
                print("\nconnect from : ", ip)
                src_master = Subject(None, ip, None)
                src_master.sock = sock
                src_master.sock.setblocking(False)
                src_master.name = src_master.sock.recv(1024)
                self.recv_con_pool.add_subject(src_master)
            except:
                time.sleep(2)
                try:
                    for subject in self.recv_con_pool.pool:
                        message = subject.sock.recv(1024)
                except:
                    pass
            else:
                pass

    def send_cmd_to(self, subj_name, cmd_list):
        subj = self.recv_con_pool.find_subject(subj_name)
        if subj == None:
            subj = Subject(subj_name, None, None)
            self.recv_con_pool.add_subject(subj)

        cmd_cnt = len(cmd_list)
        subj.sock.send(str(cmd_cnt))

        for cmd in cmd_list:
            subj.sock.send(cmd)

        '''
        pkg_cmd_list = self.pack_cmd_list(cmd_list)
        if pkg_cmd_list == None:
            return

        for pkg_cmd in pkg_cmd_list:
            subj.sock.send(pkg_cmd)
        '''

    def send_file_to(self, src_path, dest_subj, dest_path):
        for line in open(src_path):
            dest_subj.sock.send(line)

    def recv_file_from(self, src_subj, dest_path):
        file = open(dest_path, 'wb')
        while True:
            data = src_subj.sock.recv(1024)
            file.write(data)
            if not data:
                break
        file.close()

    def pack_cmd_list(self, cmd_list):
        # [ header = 4 ][    1016     ][tail = 4]
        total_len = 0
        has_next = 0
        cur_buf = ""
        extern_buf = ""
        buff_list = []

        for cmd in cmd_list:
            cur_cmd_len = len(cmd)
            if cur_cmd_len > 1016:
                print("ERROR: the length of cmd should in range [0:1016].")
                return None

            if total_len + cur_cmd_len <= 1016:
                cur_buf += cmd
                total_len += cur_cmd_len
            elif total_len + cur_cmd_len > 1016:
                total_len = 1016
                cur_buf += cmd[0:(1016 - total_len)]
                has_next += 1
                extern_buf += cmd[(1016 - total_len):]
                cur_pkg = struct.pack("!B254sB", total_len, cur_buf, has_next)
                buff_list.append(cur_pkg)

                total_len = 0
                has_next -= 1
                cur_buf = ""

                cur_buf += extern_buf
                total_len += len(extern_buf)

        return buff_list

    def start_read_order_thread(self, file_name):
        pass

    def get_an_order(self):
        if not self.has_open_file:
            for order in open("file/order_plus.op"):
                self.order_list.append(order)

        return self.order_list.pop(0)

    def exec_cmd(self, cmd):
        res = os.system(cmd)
        print(res)

    def parse_thread_start(self):
        pass

    def parse_cmdline(self):
        argv = sys.argv[1:]
        try:
            opts, args = getopt.getopt(argv, "f:")
        except:
            print("try 'gkbob -h' for more info.")
        else:
            for key, val in opts:
                if key == '-f':
                    has_order_file = True
                    order_file = val



if __name__ == "__main__":
    #print('程序名称为：{}，第一个参数为：{}，第二个参数为：{}'.format(sys.argv[0], sys.argv[1], sys.argv[2]))
    M = MainConsole()
    M.start_up()