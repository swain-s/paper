# 接收socket事件 -->
#               socket_in_event_pool-->写入新事件-->保存一个client连接
#               socket_in_finish_pool-->写入新事件-->待写入主事件池
#               socket_in_date_pool-->写入待处理数据

import socket

sockti_connected_evpool = []    #已连接事件池
sockti_shakehand_evpool = []    #已握手事件池

socketi_ready_evid = []
socketi_used_evid = []

socketi_order_evpool = []    #指令事件池

socketi_dapool = []    #处理完成数据池




class socket_moudel(object):
    def __init__(self):
        self.IP = "127.0.0.1"
        self.port = 5000
        self.max_connect = 5
        self.sever_socket = socket.socket()
        self.sever_socket.bind((self.IP, self.port))

    def recevie_message(self):
        self.sever_socket.listen(self.max_connect)
        while True:
            (client, source_ip) = self.sever_socket.accept()
            client_id = self.add_socket_client("passwd", client, source_ip)
            print(client_id)
            while True:
                message = client.recv(1024)
                print(message)
                self.add_socket_date(client_id, "passwd", message)
                if not message:
                    break

            for i in range(0, len(socket_in_date_pool)):
                for j in range(0, len(socket_in_date_pool[i])):
                    print("client_id:%d,  message_id:%s, date:%s" % (
                    socket_in_date_pool[i][j].client_id, socket_in_date_pool[i][j].message_id,
                    socket_in_date_pool[i][j].date))

    def add_socket_client(self, next_module, client, source_ip):
        s_in_client = socket_in_client()
        s_in_client.client_id = len(socket_in_client_pool)
        print(s_in_client.client_id)
        s_in_client.next_moudule = next_module
        s_in_client.client = client
        s_in_client.source_ip = source_ip
        s_in_client.d_ip = self.IP
        socket_in_client_pool.append(s_in_client)
        return s_in_client.client_id

    def add_socket_date(self, client_id, next_module, date):
        s_in_date = socket_in_date()
        s_in_date.client_id = client_id
        if len(socket_in_date_pool) <len(socket_in_client_pool):
            s_in_date.message_id = 0
        elif len(socket_in_date_pool) == len(socket_in_client_pool):
            s_in_date.message_id = len(socket_in_date_pool[client_id])
        s_in_date.next_module = next_module
        s_in_date.date = date
        if len(socket_in_date_pool) <len(socket_in_client_pool):
            socket_in_date_pool.append([s_in_date])
        elif len(socket_in_date_pool) == len(socket_in_client_pool):
            socket_in_date_pool[client_id].append(s_in_date)


#a = socket_moudel()
#a.recevie_message()



