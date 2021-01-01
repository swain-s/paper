import optparse
import socket
import threading

tgIP = 'www.limyeeman.com'
#tgIP = 'www.baidu.com'
tgPORTs = [4444]

def scan_a_port(tIP, tPort):
    conSocket = socket.socket()
    print('2')
    try:
        conSocket.connect((tIP, tPort))
        print('ok')
        try:
            conSocket.send('hello?')
            result = conSocket.recv(1024)
            print('[+]%d /TCP open   --%s' % (tPort, result))
        except:
            print('[+]%d /TCP **** -nothing' % tPort)
    except:
        print('[+]%d /TCP closed' % tPort)


def connScan(f_tip, f_tports):
    print('1')
    for port in f_tports:
        print(port)
        t = threading.Thread(target=connScan, args=(f_tip, str(f_tports)))
        t.start()

def main():
#    connScan(tgIP, tgPORTs)
    scan_a_port(tgIP, 4444)
main()
