import threading
import time

class Thd(object):
    def __init__(self):
        self.a = [0]
        self.threads = []

    def func(self):
        for i in range(20):
            self.a[0] +=1
            print(self.a[0])
            time.sleep(1)

    def change(self):
        time.sleep(5)
        for th in self.threads:
            th.destroy()

    def add_a_thread(self):
        t = threading.Thread(target=self.func)
        self.threads.append(t)
        tc = threading.Thread(target=self.change)
        t.start()
        tc.start()

T = Thd()
T.add_a_thread()