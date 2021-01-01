import time
import threading

class Timer():
    def __init__(self):
        self.current_time = 0
        self.nothing = 99
        self.fun = []

    def timer_funnc(self):
        for i in range(100):
            time.sleep(1)
            #print("+")
            #print(self.current_time)
            self.current_time += 1
            for f in self.fun:
                f()

    def put_time(self):
        return self.current_time

    def put_nothing(self):
        print(self.nothing)


    def timer_thread_start(self):
        self.timer_thread = threading.Thread(target=self.timer_funnc)
        print("timer start")
        self.timer_thread.start()

