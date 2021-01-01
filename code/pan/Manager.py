#线程池管理线程

import threading
import ThreadingPool

class Event(object):
    def __init__(self):
        self.sender_id = ""
        self.event_type = ""

        #type = new_conneciton
        self.client_socket = None
        self.client_ip_port = None

        self.is_running = 0


class Manager(object):
    def __init__(self):
        self.manager_thread = None
        self.semaphore = threading.Semaphore(0)

        self.event_pool = []
        self.MyThreadingQueue = None

    def manager_func(self):
        print("Manager: init success")
        while True:
            self.semaphore.acquire()

            if len(self.event_pool) > 0:
                handle_event = self.event_pool.pop(0)

                if handle_event.event_type == "init_threading_pool":
                    # 初始化进程池, self.threading_queue = 整个线程池对象，进程池的操作封装在该对象中
                    self.MyThreadingQueue = ThreadingPool.ThreadingQueue()
                    self.MyThreadingQueue.init_threading_pool()
                    print("Manager: threading_pool init success!")
                elif handle_event.event_type == "new_connection":
                    #线程回收
                    collect_cnt = self.MyThreadingQueue.threading_collect()
                    thread_struct = self.MyThreadingQueue.threading_pool_pop()
                    if thread_struct:
                        print("Manager: threading_pool pop: %s" % thread_struct.thread_id)
                        #未实现的功能一
                        #thread_struct.thread_info.finished_func = self.add_connection_finished
                        thread_struct.thread_info.client_fd = handle_event.client_socket
                        thread_struct.thread_info.client_ip_port = handle_event.client_ip_port
                        thread_struct.thread_info.is_running = 1
                        self.MyThreadingQueue.threading_start_run(thread_struct)
                        self.MyThreadingQueue.running_threading_push(thread_struct)
                    else:
                        print("Manager: there is no thread")
                #未实现的功能一，无法实现回调函数
                elif handle_event.event_type == "connection_finished":
                    for pos in self.MyThreadingQueue.running_threading:
                        if self.MyThreadingQueue.running_threading[pos].thread_id == handle_event.sender_id:
                            finished_thread = self.MyThreadingQueue.running_threading.pop(pos)
                            self.MyThreadingQueue.threading_pool_push(finished_thread)
                            print("Manager: %s finished running" % finished_thread.thread_id)
                            info = self.MyThreadingQueue.threading_pool_info()
                            print(info)
                            break
            else:
                print("no event")

    def manager_init(self):
        self.manager_thread = threading.Thread(name="manager", target=self.manager_func)
        self.manager_thread.start()

    def add_init_theading_pool(self, sender_id):
        event = Event()
        event.sender_id = sender_id
        event.event_type = "init_threading_pool"
        self.event_pool.append(event)
        self.semaphore.release()

    def add_new_connection(self, sender_id, client_socekt, client_ip_port):
        event = Event()
        event.sender_id = sender_id
        event.event_type = "new_connection"
        event.client_socket = client_socekt
        event.client_ip_port = client_ip_port
        self.event_pool.append(event)
        self.semaphore.release()

    #未实现的功能一
    def add_connection_finished(self, sender_id):
        event = ()
        event.send_id = sender_id
        event.event_type = "end_connection"
        self.event_pool.append(event)
        self.semaphore.release()
        return self.add_connection_finished