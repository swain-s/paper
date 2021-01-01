import socket
import time

sever_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sever_socket.setblocking(False)
sever_socket.bind(("127.0.0.1", 6949))
sever_socket.listen(5)

def accept():
    while True:
        try:
            c, ip = sever_socket.accept()
            print("--", ip)
            try:
                time.sleep(1)
                date = c.recv(4, 0x40)
            except:
                date = None
                time.sleep(5)
                print("no")
            if date:
                print("+++", date)
        except:
            time.sleep(5)
            print("ask")
def recv():
    queue = []
    while True:
        try:
            print(1, end=" ")
            c, ip = sever_socket.accept()
            print(2)
        except:
            time.sleep(2)
            print("ip")
        else:
            print("connect: ", ip)
            c.setblocking(False)
            queue.append(c)

            dqueue = []
            while True:
                try:
                    for sk in queue:
                        date = sk.recv(4, 0x40)
                        dqueue.append(date)
                except:
                    print("da")
                    date = None
                    time.sleep(2)
                else:
                    if len(dqueue) > 0:
                        print("+++", dqueue)
                        dqueue = []

def reactor():
    pass

recv()

