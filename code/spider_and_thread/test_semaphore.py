#生成者和消费者问题

import threading
import time
from test_time import *

#struct
class node(object):
    def __init__(self):
        self.thd = None
        self.start_time = 0

class test_semaphore(Timer):
    def __init__(self):
        super(Timer).__init__()
        self.current_time = 300
        self.fun = []
        self.event = []

        self.ga = [0]
        self.sad = threading.Semaphore(0)
        self.sda = threading.Semaphore(5)
        self.saa = threading.Semaphore(1)
        self.sdd = threading.Semaphore(1)

        self.sd5 = threading.Semaphore(0)

    def add1(self):
        for i in range(20):
            self.event[0].start_time = self.current_time
            print(self.event[0].start_time)
            time.sleep(5)

            self.saa.acquire() #-1  s - me
            self.sda.acquire()

            if self.ga[0] < 4:
                self.ga[0] += 1
                print("*1 ++ %d" % self.ga[0])
            elif self.ga[0] >= 4:
                self.sad.release()
                self.sad.release()
                self.sad.release()
                self.sad.release()
                self.sad.release()
                #sad.release()
                print("*1 sleep")
                #time.sleep(50)
            else:
                print("error")

            self.saa.release()     #+1  s - me -next

    def add2(self):
        for i in range(20):
            self.event[1].start_time = self.current_time
            print(self.event[1].start_time)
            time.sleep(10)

            self.saa.acquire() #-1  s - me
            self.sda.acquire()

            if self.ga[0] < 4:
                self.ga[0] += 1
                print("*2 ++ %d" % self.ga[0])
            elif self.ga[0] >= 4:
                self.sad.release()
                self.sad.release()
                self.sad.release()
                self.sad.release()
                self.sad.release()
                #sad.release()
                print("*2 sleep")
                #time.sleep(50)
            else:
                print("error")

            self.saa.release()     #+1  s - me -next

    def dec1(self):
        for i in range(20):
            self.sdd.acquire()

            self.sad.acquire() #-1  s - me

            if self.ga[0] >0:
                self.ga[0] -= 1
                print("*1 -- %d == %d" % (self.ga[0], self.put_time()))
                self.put_time()
            elif self.ga[0] == 0:
                self.sd5.release()
                self.sda.release()
                self.sda.release()
                self.sda.release()
                self.sda.release()
                self.sda.release()
            else:
                print("error")


            self.sdd.release()

    def dec2(self):
        for i in range(20):
            self.sdd.acquire()

            self.sad.acquire() #-1  s - me

            if self.ga[0] > 0:
                self.ga[0] -= 1
                print("*2 -- %d == %d" % (self.ga[0], self.put_time()))
            elif self.ga[0] == 0:
                self.sd5.release()
                self.sda.release()
                self.sda.release()
                self.sda.release()
                self.sda.release()
                self.sda.release()
            else:
                print("error")

            self.sdd.release()

    def func5(self):
        while True:
            self.sd5.acquire()
            print("********************")

    def find_7(self):
        for node in self.event[:2]:
            print("now is : %d, start is %d" % (self.current_time, node.start_time))
            if self.current_time - node.start_time >= 7:
                print("success!!!!")
        return self.find_7

    def main(self):
        self.fun.append(self.find_7)
        self.timer_thread_start()
        ta1 = threading.Thread(target=self.add1)
        ta2 = threading.Thread(target=self.add2)
        td1 = threading.Thread(target=self.dec1)
        td2 = threading.Thread(target=self.dec2)
        t5 = threading.Thread(target=self.func5)

        ea1 = node()
        ea1.thd = ta1
        ea1.start_time = self.current_time
        self.event.append(ea1)
        ea2 = node()
        ea2.thd = ta2
        ea2.start_time = self.current_time
        self.event.append(ea2)
        ed1 = node()
        ed1.thd = td1
        ed1.start_time = self.current_time
        self.event.append(ed1)
        ed2 = node()
        ed2.thd = td2
        ed2.start_time = self.current_time
        self.event.append(ed2)
        e5 = node()
        e5.thd = t5
        e5.start_time = self.current_time
        self.event.append(e5)

        for i in self.event:
            i.thd.start()

test = test_semaphore()
test.main()
