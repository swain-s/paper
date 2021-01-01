import socket

def test1():
    s = socket.socket()
    s.bind(("127.0.0.1", 5656))
    s.listen(5)

    a, addr = s.accept()
    print(a.recv(1024))

def test2():
    event_id = [i for i in range(0, 1000)]
    print(event_id[0])
    print(event_id[999])

def test3():
    from event_type import main_pool_event
    e_p = []
    a = main_pool_event()
    a.event_id = 3
    e_p.append(a)
    print(e_p[0].event_id)

def test4():
    import threading
    import time

    lock = threading.Lock()

    def f_send():
        cnt = 0
        while True:
            if cnt % 5 == 0 and cnt != 0:
                lock.release()

            time.sleep(1)
            cnt = cnt + 1
            print("send")
    def f_receive():
        while True:
            lock.acquire()
            print("receive------")
    t1 = threading.Thread(target=f_send, args=())
    t2 = threading.Thread(target=f_receive, args=())
    t1.start()
    t2.start()


def test5():
    import struct
    # native byteorder
    buffer = struct.pack("ihb", 1, 17, 3)
    print(repr(buffer))
    print(struct.unpack("ihb", buffer))

    # data from a sequence, network byteorder
    date = [1, 2, 3]
    buffer = struct.pack("!ihb", *date)
    print(repr(buffer))
    print(struct.unpack("!ihb", buffer))
test5()


