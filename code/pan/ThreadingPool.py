#线程池模块

import threading
import struct

#避免调用过长，将两个结构体合并到ThreadInfo中
'''
class ThreadKeyInfo(object):
    def __init__(self):
        self.key_id = 0
        self.encrypt_key = b""
        self.public_key = b""
        self.private_key = b""

class ThreadClientInfo(object):
    def __init__(self):
        self.session_id = 0
        self.client_fd = None
        self.client_ip = ""
        self.cient_port = 0
'''

class ThreadInfo(object):
    def __init__(self, thread_id):
        self.thread_id = thread_id
        #未实现的功能一
        self.thread_finished = None
        #self.thread_key_info = ThreadKeyInfo()
        #self.thread_cilent_info = ThreadClientInfo()

        self.session_id = 0
        self.client_fd = None
        self.client_ip_port = None

        self.key_id = 0
        self.encrypt_key = b""
        self.public_key = b""
        self.private_key = b""


class ThreadStruct(object):
    def __init__(self, thread_id, thread_func, thread_info):
        self.thread_id = thread_id
        self.thread_info = thread_info
        self.thread = threading.Thread(name=thread_id, target=thread_func, args=(thread_info, ))


class ThreadingQueue(object):
    def __init__(self):
        self.threading_num = 5
        self.threading_id = ["alice", "bob", "cart", "david", "even"]

        self.threading_pool = []
        self.running_threading = []

    def threading_func(self, thread_info):
        print("Threading-%s, i am handing at: " %
              thread_info.thread_id, thread_info.client_ip_port)
        #ssl()
        while True:
            date = thread_info.client_fd.recv(1024)
            if not date:
                break
            if len(date) == 1024:
                record_type, record_lenth, record_message = struct.unpack("!II1016s", date)
                print("Thread-%s: receive:[ %d ][ %d ][ %s ]" %
                      (thread_info.thread_id, record_type, record_lenth, record_message))
                #关闭连接
                if record_type == 1:
                    break
            else:
                print("Thread-%s: recv date is not 1024 bytes" % thread_info.thread_id)
        print("Thread-%s: i am done" % thread_info.thread_id)
        thread_info.client_fd.close()
        thread_info.is_running = 0
        #未实现的功能一
        if thread_info.thread_finished:
            thread_info.thread_finished(thread_info.thread_id)

    def init_threading_pool(self):
        for cnt in range(self.threading_num):
            thread_info = ThreadInfo(self.threading_id[cnt])
            thread_struct = ThreadStruct(self.threading_id[cnt], self.threading_func, thread_info)
            self.threading_pool.append(thread_struct)

    def threading_start_run(self, thread_struct):
        thread_struct.thread.start()

    def threading_pool_info(self):
        pool = []
        for thread_struct in self.threading_pool:
            pool.append(thread_struct.thread_id)
        return pool

    def running_pool_info(self):
        pool = []
        for thread_struct in self.running_threading:
            pool.append([thread_struct.thread_id, thread_struct.thread_info.session_id, thread_struct.client_ip_port])
        return pool

    def threading_pool_pop(self):
        if len(self.threading_pool) == 0:
            print("Thread_Pool: there is no thread to pop!")
            return None
        else:
            return self.threading_pool.pop(0)

    def running_threading_push(self, thread_struct):
        self.running_threading.append(thread_struct)

    #从running_queue中添加到threading_pool中
    def threading_pool_push(self, thread_struct):
        thread_struct.thread_info = ThreadInfo(thread_struct.thread_id)
        thread_struct.thread = threading.Thread(name=thread_struct.thread_id,
                                                target=self.threading_func, args=(thread_struct.thread_info, ))
        self.threading_pool.append(thread_struct)

    def threading_collect(self):
        find_thread = 0
        for pos in range(len(self.running_threading)):
            if self.running_threading[pos].thread_info.is_running == 0:
                find_thread += 1
                #线程只能开始一次，所以需要把原线程销毁，新建线程
                finishend_thread = self.running_threading.pop(pos)
                new_thread_info = ThreadInfo(finishend_thread.thread_id)
                new_thread_struct = ThreadStruct(finishend_thread.thread_id, self.threading_func, new_thread_info)
                self.threading_pool.append(new_thread_struct)
                print("Manager: collect %s " % finishend_thread.thread_id)
        return find_thread