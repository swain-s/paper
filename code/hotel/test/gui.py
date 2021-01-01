from socket import *
from tkinter import *
from PIL import Image, ImageTk
import re
import json
import sys
import os
import aes
import file_aes


class Gui(object):
    def __init__(self):
        self.addr = ('10.8.216.91', 6992)
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.key = 'abcdefg'

        self.window = Tk()
        self.main_frame = Frame(self.window, width=1300, height=700, bd=0)
        self.image_file = Image.open("background.png")
        self.im = ImageTk.PhotoImage(self.image_file)
        self.image_label = Label(self.main_frame, image=self.im).pack(side=LEFT, padx=0)

        self.sever_frame = Frame(self.main_frame, width=560, height=550, bd=0)
        self.left_sever = Frame(self.sever_frame, width=275, height=550, bd=0, bg='Seashell')
        self.right_sever = Frame(self.sever_frame, width=280, height=550, bd=0, bg='Seashell')

        self.client_frame = Frame(self.main_frame, width=560, height=550, bd=0)
        self.left_client = Frame(self.client_frame, width=275, height=550, bd=0, bg='black')
        self.image_label = Label(self.left_client, image=self.im).pack(side=LEFT, padx=0, pady=0)
        self.right_client = Frame(self.client_frame, width=280, height=550, bd=0, bg='Seashell')
        self.button1 = Button(self.main_frame, bd=0, text='服务器', fg='white', font=20, bg='black')
        self.button2 = Button(self.main_frame, bd=0, text='客户端', fg='white', font=20, bg='black')

        self.tip1 = Frame(self.main_frame, bg='black', width=100, height=30)
        self.tip2 = Frame(self.main_frame, bg='black', width=100, height=30)
        self.tip3 = Frame(self.main_frame, bg='black', width=100, height=30)
        self.tip4 = Frame(self.main_frame, bg='black', width=100, height=30)
        self.tip1_label = Label(self.tip1, text='未连接',bg='black', fg='white', width=12)
        self.tip2_label = Label(self.tip2, text='未连接....', bg='black',fg='white', width=12)
        self.tip3_label = Label(self.tip3, text='未连接...', bg='black',fg='white', width=12)
        self.tip4_label = Label(self.tip4, text='未连接...', bg='black',fg='white', width=12)

        self.con_button = Button(self.main_frame, text='未连接', font= 30, width=7, height=1, bg='Brown', command=self.click_con)
        self.get_button = Button(self.main_frame, text='接收', font=30, width=7, height=1, bg='Brown', command=self.click_get)
        self.send_button = Button(self.main_frame, text='发送', font=30, width=7, height=1, bg='Brown', command=self.click_send)
        self.exit_button = Button(self.main_frame, text='退出', font=30, width=7, height=1, bg='Brown', command=self.click_exit)

    def frame_place(self):
        self.window.title('客户端')
        self.window.geometry('1300x700')
        self.main_frame.place(x=0, y=0)

        self.sever_frame.place(x=70, y=100)
        self.left_sever.place(x=0, y=0)
        self.right_sever.place(x=280, y=0)

        self.client_frame.place(x=700, y=100)
        self.left_client.place(x=0, y=0)
        self.right_client.place(x=280, y=0)

        self.tip1.place(x=620, y=200)
        self.tip2.place(x=620, y=300)
        self.tip3.place(x=620, y=400)
        self.tip4.place(x=620, y=500)

        self.con_button.place(x=900, y=30)
        self.get_button.place(x=1000, y=30)
        self.send_button.place(x=1100, y=30)
        self.exit_button.place(x=1200, y=30)

        self.button1.place(x=50, y=80)
        self.button2.place(x=680, y=80)

        self.tip1_label.pack()
        self.tip2_label.pack()
        self.tip3_label.pack()
        self.tip4_label.pack()

    def begin(self):
        path = sys.path[0]
        file_list = os.listdir(path)
        print(file_list)
        i = 0
        j = len(file_list)
        for i in range(0, j):
            print(file_list[i])
            button = Button(self.left_client, text=file_list[i], width=30, bg='yellow', command=lambda i=i: self.click_client(i))
            button.place(x=30, y=30 * i + 10)

    def my_submit(self, order):
        if order == 'get':
            self.tip2_label.config(text='接收文件指令')
            self.tip3_label.config(text='选择文件中...')
            file_name = self.seach.get()
            aes_file_name = aes.aes_encrypt(file_name, self.key)
            self.client_socket.send(aes_file_name)
            print(aes_file_name)
            file_size = self.client_socket.recv(1024)
            print(file_size)
            file_size = aes.aes_decrypt(file_size, self.key)
            print(file_size)
            file_size = file_size.strip()
            file_size = int(file_size)
            print(file_size)

            f = open(file_name, 'wb')
            while True:
                if file_size > 1024:
                    data = self.client_socket.recv(1024)
                else:
                    data = self.client_socket.recv(file_size)
                if not data:
                    break
                f.write(data)
                file_size = file_size - len(data)
                if file_size == 0:
                    break
            f.close()
            file_aes.file_decrypt(file_name, self.key)

            print(file_name, '接收完毕')
            self.menu.destroy()

            new_path = sys.path[0]
            new_file_list = os.listdir(new_path)
            self.new_button = Button(self.left_client, text=file_name, width=30, bg='yellow')
            self.new_button.place(x=30, y=len(new_file_list)*30-20)


        elif order == 'send':
            self.tip2_label.config(text='发送文件指令')
            self.tip3_label.config(text='选择文件中...')
            file_name = self.seach.get()
            my_file_name = file_name
            file_aes.file_encrypt(file_name, self.key)

            new_file_name = 'temp-' + file_name

            aes_file_name = aes.aes_encrypt(file_name, self.key)
            for i in range(0, 1024-len(aes_file_name)):
                aes_file_name = aes_file_name + b' '
            self.client_socket.send(aes_file_name)

            file_size = os.path.getsize(new_file_name)
            str_file_size = str(file_size)
            aes_file_size = aes.aes_encrypt(str_file_size, self.key)
            for i in range(0, 1024-len(aes_file_size)):
                aes_file_size = aes_file_size +b' '
            print(aes_file_size)
            self.client_socket.send(aes_file_size)

            f = open(new_file_name, 'rb')
            while True:
                data = f.read(1024)
                if not data:
                    break
                self.client_socket.send(data)
            f.close()
            os.remove(new_file_name)


            self.tip4_label.config(text='发送成功啦')
            print('结束-发送文件')
            self.menu.destroy()

            new_file_list = self.client_socket.recv(1024)
            new_file_list = aes.aes_decrypt(new_file_list, self.key)
            new_file_list = json.loads(new_file_list)
            print(new_file_list)
            print(len(new_file_list))
            self.new_button = Button(self.left_sever, text=file_name, width=30, bg='yellow')
            self.new_button.place(x=30, y=len(new_file_list)*30-20)

    def click_client(self, i):
        return 0

    def click_sever(self, i):
        print(re.search('file_list[i]', '.'))

    def click_con(self):
        self.client_socket.connect(self.addr)
        self.tip1_label.config(text='已连接到服务器')
        self.tip2_label.config(text='待命...')
        self.tip3_label.config(text='待命...')
        self.tip4_label.config(text='待命...')
        order = 'list'
        order = aes.aes_encrypt(order, self.key)
        print(order)
        self.client_socket.send(order)
        file_list = self.client_socket.recv(1024)
        file_list = aes.aes_decrypt(file_list, self.key)

        file_list = json.loads(file_list)
        print(file_list)

        i = 0
        j = len(file_list)
        for i in range(0, j):
            print (file_list[i])
            button = Button(self.left_sever, text=file_list[i], width=30, bg='yellow',
                            command=lambda i=i: self.click_sever(i))
            button.place(x=30, y=30*i+10)
        self.already = Button(self.main_frame, text='已连接', font= 30, width=7, height=1, bg='green')
        self.already.place(x=900, y=30)

    def click_get(self):
        order = 'get'
        self.menu = Frame(self.main_frame, width=700, height=70, bd=0, bg='black')
        self.label = Label(self.menu, bd=0, bg='Thistle', text='请输入文件名：')
        self.seach = Entry(self.menu, width=20, font=12, bd=0, bg='white')
        self.button = Button(self.menu, width=10, height=1, bd=3, text='确定', bg='green',
                        command=lambda order=order: self.my_submit(order))
        self.menu.place(x=500, y=25)
        self.label.grid(row=0, column=0)
        self.seach.grid(row=0, column=1)
        self.button.grid(row=0, column=2)

        order = aes.aes_encrypt(order, self.key)
        self.client_socket.send(order)
        print('接收文件--请求成功')
        self.tip2_label.config(text='请选择接收文件')
        self.my_submit(order)
#        self.menu.destroy()

    def click_send(self):
        order = 'send'
        self.menu = Frame(self.main_frame, width=700, height=70, bd=0, bg='black')
        self.label = Label(self.menu, bd=0, bg='Thistle', text='请输入文件名：')
        self.seach = Entry(self.menu, width=20, font=12, bd=0, bg='white')
        self.button = Button(self.menu, width=10, height=1, bd=3, text='确定', bg='green',
                             command=lambda order=order: self.my_submit(order))
        self.menu.place(x=500, y=25)
        self.label.grid(row=0, column=0)
        self.seach.grid(row=0, column=1)
        self.button.grid(row=0, column=2)

        order = aes.aes_encrypt(order, self.key)
        self.client_socket.send(order)
        print('发送文件--请求成功')
        self.tip2_label.config(text='请选择发送文件')
        self.my_submit(order)

    def click_exit(self):
        order = 'exit'
        order = aes.aes_encrypt(order, self.key)
        self.client_socket.send(order)

        self.window.destroy()

    def main(self):
        self.begin()
        self.frame_place()
        self.window.mainloop()


#Output = Gui()
#Output.main()
