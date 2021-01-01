import threading
import time
import random

#****************** part1 add event **************
class node(object):
    def __init__(self, n):
        self.id = n
        self.next = None
#****************************************************
# 0 1 2 3 4
# + + + + +
# 0 0 0 0 0
# 0 0 0 0 0 0
class head(object):
    def __init__(self, n):
        self.num = n
        self.first = None

def init_hash():
    cnt = 0
    hs_list = []
    for i in range(0, 5):
        hs_list.append(head(i))

    cnt_node = head(0)
    hs_list.append(cnt_node)
    return cnt, hs_list

#************   add   ***********
def add(ids, n, hs_list):  #ids的第n个元素， cnt:node树
    anode = node(ids[n])

    hn = ids[n] % 5
    lastnode = hs_list[hn].first
    if lastnode == None:
        hs_list[hn].first = anode
        hs_list[5].num += 1
        return 0
    else:
        while(True):
            if lastnode.next == None:
                break
            lastnode = lastnode.next
        lastnode.next = anode
        hs_list[5].num += 1

def traverse(hs_list, n):   #hs_list的第n个队列
    print("tra-" + str(n), end=":")
    current = hs_list[n].first
    while(True):
        if current == None:
            break
        elif current != None:
            print(current.id, end="->")
            current = current.next
        else:
            print("error!")
    print("")

def traverse_all(hs_list):
    cnt = hs_list[5].num
    print("cnt:" + str(cnt))
    for i in range(0, len(hs_list)-1):
        traverse(hs_list, i)


#************   eat   ***********
def eat(hs_list):
    for hn in range(0 ,5):
        if hn == 4 and hs_list[hn].first == None:
            print("eat error!")
            return -1
        if hs_list[hn].first == None:
            continue
        else:
            print("-eat:" + str(hs_list[hn].id) + " = " + str(hn))
            new_first = hs_list[hn].next
            hs_list[hn].first = new_first
            hs_list[5].num -= 1

#************************************************************
def producer(ids, hs_list):
    for i in range(0, len(ids)):
        add(ids, i, hs_list)
        time.sleep(1)

def custemer(hs_list):
    return 0


def main():
    ids = [1, 3, 5, 6, 8, 10, 11, 13, 15, 20, 23, 2, 12]
    (cnt, hlist) = init_hash()
    th1 = threading.Thread(target=producer, args=(ids, cnt, hlist))
    producer(ids, hlist)
    traverse_all(hlist)

    #time.sleep(3)
    #eat(hlist)

#main()



condition1 = threading.Condition()
condition2 = threading.Condition()


class mynode():
    def __init__(self, num):
        self.num = num
        self.cnt = 0

def add1(list):
    while True:
        condition1.acquire()
        condition2.acquire()
        if list[0].num == 5:
            print("add sleep")
            condition1.notify()
            condition1.wait()
            time.sleep(1)
            print("add wake up")
        elif list[0].num < 5:
            list[0].num += 1
            list[0].cnt += 1
            print("+++", end="")
            tra1(list)
        #condition.release()
        time.sleep(2)

def dec1(list):
    time.sleep(1)
    while True:
        condition1.acquire()
        condition2.notify()
        if list[0].num <= 0:
            print("dec error!")
            condition1.notify()
            condition1.wait()
            time.sleep(1)
            print("dec wake up")
        elif list[0].num >0:
            list[0].num -=1
            list[0].cnt += 1
            print("---", end="")
            tra1(list)
        #condition.release()
        time.sleep(2)

def dec2(list):
    time.sleep(1)
    while True:
        condition2.acquire()
        if list[0].num <= 0:
            print("2222 dec error!")
            condition2.notify()
            condition2.wait()
            time.sleep(1)
            print("2222 dec wake up")
        elif list[0].num >0:
            list[0].num -=1
            list[0].cnt += 1
            print("222 ---", end="")
            tra1(list)
        #condition.release()
        time.sleep(2)

def tra1(list):
    print("num is: %d, cnt is: %d\n" % ((list[0].num), list[0].cnt))

def test_thread():
    list = []
    node = mynode(0)
    list.append(node)
    # list ok!

    p = threading.Thread(target=add1, args=(list, ))
    p.start()
    c1 = threading.Thread(target=dec1, args=(list, ))
    c1.start()
    c2 = threading.Thread(target=dec2, args=(list, ))
    c2.start()
    #c2 = threading.Thread(target=dec1, args=list)

    #p.join()
    #tra1(list)

time_cnt = 0
def timer_start():
    global time_cnt
    for i in range(100):
        time.sleep(1)
        time_cnt += 1

def readtime():
    global time_cnt
    for i in range(100):
        time.sleep(3)
        print(time_cnt)


def timer():
    timer = threading.Thread(target=timer_start)
    timer.start()

    rtime = threading.Thread(target=readtime)
    rtime.start()

timer()




def thread_info():
    athread = threading.Thread(target=add1, args=(list, ))
    print(threading.active_count())
    print(threading.enumerate())       #当前运行线程队列
    print(threading.current_thread())  #当前线程空间
#test_thread()
#thread_info()

def test_args():
    def addnum(b):
        b.num = b.num + 1

    class testnode():
        def __init__(self):
            self.num = 1

    a = testnode()
    addnum(a)
    print(a.num)

def aadd(b):
    b[0] = 10
