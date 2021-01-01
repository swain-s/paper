import socket

c = socket.socket()
c.connect(("14.215.177.39/", 80))
c.send(b'hello')

date = c.recv(1024)
print(date)
