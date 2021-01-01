import socket
import struct
import time

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.1.101', 6949))

def ssl():
    type = 4
    lenth = 10
    message = b"a" * 1015 + b"c"
    data = struct.pack("!II1016s", type, lenth, message)
    client_socket.send(data)

def unblock():
    while True:
        time.sleep(5)
        cnt = 1
        date = struct.pack("!I", cnt)
        client_socket.send(date)
        cnt += 1
unblock()