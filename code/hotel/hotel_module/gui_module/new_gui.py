from tkinter import *
from PIL import Image, ImageTk

class Main_windows(object):
    def __init__(self):
        self.window_width = 800
        self.window_height = 600
        self.init_window = Tk()
        self.parent_frame = Frame(self.init_window, width=self.window_width, height=self.window_height, bd=0, bg="green")
        self.child_frame = []

        image_file = Image.open("image/1_1.png")
        self.f11 = ImageTk.PhotoImage(image_file)

        image_file = Image.open("image/1_2.png")
        self.f12 = ImageTk.PhotoImage(image_file)

        image_file = Image.open("image/f1.png")
        self.f1 = ImageTk.PhotoImage(image_file)

    #设置背景图片
    def set_bg_image(self):
        image_file = Image.open("image/f.png")
        self.bg_image = ImageTk.PhotoImage(image_file)
        image_label = Label(self.parent_frame, bd=0, image=self.bg_image)#两个变量均为全局变量
        image_label.place(x=0, y=0)

    #框架处理
    #初始框架
    def create_first_frame(self):
        first_frame = Frame(self.parent_frame, width=self.window_width/2, height=self.window_height/2, bd=0, bg="yellow")#400*300
        self.child_frame.append(first_frame)

        image_label = Label(first_frame, bd=0, image=self.f1)#两个变量均为全局变量
        image_label.pack(side=LEFT, padx=0, pady=0)
        #image_label.place(x=0, y=0)

        button = ["办理入住", "退房"]
        button_size_width = [225, 225]
        button_size_height = [50, 50]
        button_palce_x = [80, 80]
        button_place_y = [75, 200]
        come_button = Button(first_frame, width=button_size_width[0], height=button_size_height[0], text=button[0], image=self.f11,  command=self.click_first_in)
        out_button = Button(first_frame, width=button_size_width[1], height=button_size_height[1], image=self.f12, text=button[1], command=self.click_first_out)
        come_button.place(x=button_palce_x[0], y=button_place_y[0])
        out_button.place(x=button_palce_x[1], y=button_place_y[1])
        first_frame.place(x=self.window_width/8, y=self.window_height/4)


    #入住框架
    def create_in_freme(self):
        in_frame = Frame(self.parent_frame, width=self.window_width*2/3, height=self.window_height*3/4, bd=0, bg="red")#400*150
        self.child_frame.append(in_frame)
        back_button = Button(in_frame, width=6, height=2, bg="blue", text="返回", command=self.click_back).place(x=0, y=0)
        button = ["人脸识别", "二维码扫描", "认证成功"]
        button_size_width = [10, 10, 10]
        button_size_height = [6, 6, 6]
        button_palce_x = [50, 200, 350]
        button_place_y = [75, 75, 75]
        self.face_button = Button(in_frame, width=button_size_width[0], height=button_size_height[0], text=button[0], command=self.t1)
        qrcode_button = Button(in_frame, width=button_size_width[1], height=button_size_height[1], text=button[1])
        ok_button = Button(in_frame, width=button_size_width[2], height=button_size_height[2], text=button[2])
        self.face_button.place(x=button_palce_x[0], y=button_place_y[0])
        qrcode_button.place(x=button_palce_x[1], y=button_place_y[1])
        ok_button.place(x=button_palce_x[2], y=button_place_y[2])
        in_frame.place(x=0, y=self.window_height/8)

    def t1(self):
        self.face_button.destroy()

    #退房框架
    def create_out_freme(self):
        out_frame = Frame(self.parent_frame, width=self.window_width*2/3, height=self.window_height*3/4, bd=0, bg="blue")#400*150
        self.child_frame.append(out_frame)
        back_button = Button(out_frame, width=6, height=2, bg="blue", text="返回", command=self.click_back).place(x=0, y=0)
        button = ["人脸识别", "二维码扫描", "认证成功"]
        button_size_width = [10, 10, 10]
        button_size_height = [6, 6, 6]
        button_palce_x = [100, 250, 400]
        button_place_y = [75, 75, 75]
        face_button = Button(out_frame, width=button_size_width[0], height=button_size_height[0], text=button[0])
        qrcode_button = Button(out_frame, width=button_size_width[1], height=button_size_height[1], text=button[1])
        ok_button = Button(out_frame, width=button_size_width[2], height=button_size_height[2], text=button[2])
        face_button.place(x=button_palce_x[0], y=button_place_y[0])
        qrcode_button.place(x=button_palce_x[1], y=button_place_y[1])
        ok_button.place(x=button_palce_x[2], y=button_place_y[2])
        out_frame.place(x=0, y=self.window_height/8)

    def del_other_frame(self):
        for frame in self.child_frame:
            frame.destroy()

    #按钮处理
    #办理入住按钮
    def click_first_in(self):
        self.del_other_frame()
        self.create_in_freme()

    #办理退房
    def click_first_out(self):
        self.del_other_frame()
        self.create_out_freme()

    def click_back(self):
        self.del_other_frame()
        self.create_first_frame()

    #初始化
    #窗口初始化
    def frame_init(self):
        self.init_window.geometry("%dx%d" % (self.window_width, self.window_height))
        self.parent_frame.place(x=0, y=0)
        self.set_bg_image()
        self.create_first_frame()
        self.init_window.mainloop()


M = Main_windows()
M.frame_init()