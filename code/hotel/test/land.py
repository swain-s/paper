from socket import *
from tkinter import *
#from PIL import Image, ImageTk
import json
#import gui
#import file_aes
#import aes

class Land(object):
    def __init__(self):
        self.land_addr = ('10.8.216.91', 6997)
        self.land_socket = socket(AF_INET, SOCK_STREAM)
        self.key = 'abcdefg'

        self.first_window = Tk()
        self.frame = Frame(self.first_window, width=400, height=300, bg='lightblue')
        #self.first_image_file = Image.open("first.png")
        #self.first_im = ImageTk.PhotoImage(self.first_image_file)
        #self.first_image_label = Label(self.frame, image=self.first_im).pack(side=LEFT, padx=0)

        self.con_button = Button(self.frame, width=10, height=1, bg='red', text='未连接服务器', command=self.con)
        self.ok_con = Button(self.frame, width=10, height=1, bg='green', text='已连接服务器')

        self.name_frame = Frame(self.frame, width=200, height=30, bd=0, bg='black')
        self.name_label = Label(self.name_frame, bd=1, width=8, bg='lightblue', text='用户名：')
        self.user_name = Entry(self.name_frame, width=20, font=12, bd=0, bg='white')

        self.pass_frame = Frame(self.frame, width=200, height=30, bd=0, bg='black')
        self.pass_label = Label(self.pass_frame, width=8, bd=1, bg='lightblue', text='密码：')
        self.pass_word = Entry(self.pass_frame, width=20, font=12, bd=0, bg='white')

        self.ok_button = Button(self.frame, text='登录', width=5, height=1, bd=3, bg='#7fb80e', command=self.next_window)
        self.exit_button = Button(self.frame, text='退出', width=5, height=1, bd=3, bg='#7fb80e', command=self.click_exit)
        self.register_button = Button(self.frame, text='注册', width=10, height=1, bd=3, bg='#fdb933', command=self.click_register)

    def frame_place(self):
        self.first_window.geometry('400x300')
        self.first_window.title('注册-登录')
        self.frame.place(x=0, y=0)
        self.con_button.place(x=0, y=0)

        self.name_frame.place(x=75, y=60)
        self.name_label.grid(row=0, column=0)
        self.user_name.grid(row=0, column=1)

        self.pass_frame.place(x=75, y=100)
        self.pass_label.grid(row=0, column=0)
        self.pass_word.grid(row=0, column=1)

        self.ok_button.place(x=120, y=150)
        self.exit_button.place(x=240, y=150)
        self.register_button.place(x=160, y=270)

    def con(self):
        self.land_socket.connect(self.land_addr)
        self.ok_con.place(x=0, y=0)
        print('连接成功！')

    def reg_submit(self):
        list = []
        name = self.reg_user_name.get()
        password = self.reg_pass_word.get()
        list.append(name)
        list.append(password)

        json_file_list = json.dumps(list)
        #encoded_file_list = aes.aes_encrypt(json_file_list, self.key)
        #self.land_socket.send(encoded_file_list)

        self.reg_success.place(x=50, y=250)

    def reg_go_back(self):
        self.register_frame.destroy()

    def next_window(self):
        order = 'land'
        order = aes.aes_encrypt(order, self.key)
        print(order)
        self.land_socket.send(order)

        land_list = []
        name = self.user_name.get()
        print(name)
        password = self.pass_word.get()
        print(password)
        land_list.append(name)
        land_list.append(password)

        json_file_list = json.dumps(land_list)
        encoded_file_list = aes.aes_encrypt(json_file_list, self.key)
        self.land_socket.send(encoded_file_list)

        self.first_window.destroy()

        Output = gui.Gui()
        Output.main()

    def click_exit(self):
        self.first_window.destroy()

    def click_register(self):
        order = 'register'

        self.register_frame = Frame(self.frame, width=400, height=300, bg='red')
        self.second_image_file = Image.open("second.png")
        self.second_im = ImageTk.PhotoImage(self.second_image_file)
        self.second_image_label = Label(self.register_frame, image=self.second_im).pack(side=LEFT, padx=0)

        self.reg_name_frame = Frame(self.register_frame, width=200, height=30, bd=0, bg='yellow')
        self.reg_name_label = Label(self.reg_name_frame, bd=2, width=8, bg='#99ccff', text='设定名字：')
        self.reg_user_name = Entry(self.reg_name_frame, width=20, font=12, bd=0, bg='white')

        self.reg_pass_frame = Frame(self.register_frame, width=200, height=30, bd=0, bg='yellow')
        self.reg_pass_label = Label(self.reg_pass_frame, width=8, bd=2, bg='#99ccff', text='设定密码：')
        self.reg_pass_word = Entry(self.reg_pass_frame, width=20, font=12, bd=0, bg='white')

        self.reg_ok_button = Button(self.register_frame, text='提交注册', width=8, height=1, bd=3, bg='#cd9a5b',
                                    command=self.reg_submit)
        self.reg_exit_button = Button(self.register_frame, text='返回登录', width=8, height=1, bd=3, bg='#cd9a5b',
                                      command=self.reg_go_back)

        self.reg_success = Label(self.register_frame, text='注册成功， 请返回登录', bg='green')

        self.register_frame.place(x=0, y=0)


        self.reg_name_frame.place(x=75, y=140)
        self.reg_name_label.grid(row=0, column=0)
        self.reg_user_name.grid(row=0, column=1)

        self.reg_pass_frame.place(x=75, y=180)
        self.reg_pass_label.grid(row=0, column=0)
        self.reg_pass_word.grid(row=0, column=1)

        self.reg_ok_button.place(x=120, y=240)
        self.reg_exit_button.place(x=240, y=240)


        print(order)
        order = aes.aes_encrypt(order, self.key)
        print(order)

        self.land_socket.send(order)
        print('order 发送成功')


    def main(self):
            self.frame_place()
            self.first_window.mainloop()



My_land = Land()
My_land.main()