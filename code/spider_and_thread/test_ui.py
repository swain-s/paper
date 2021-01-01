from tkinter import *
import time
import threading
from test_time import *

class GUI(Timer):
    def __init__(self):
        super(Timer).__init__()
        self.current_time = 0
        self.main_window = Tk()
        self.main_frame = Frame(self.main_window, width=800, height=600)
        self.canvas = Canvas(self.main_frame, background="lightblue", width=800, height=600)

    def window_init(self):
        self.main_window.geometry("800x600")
        self.main_frame.place(x=0, y=0)
        self.canvas.place(x=0, y=0)
        self.canvas.update()

    def ui_thread_func(self):
        time.sleep(3)
        print("now i am:%d" % self.current_time)
        self.time_lable = Label(self.canvas, text=self.current_time, width=10, height=1, background="green")
        self.time_lable.place(x=0, y=0)
        self.canvas.update()

        time.sleep(2)
        print("now i am:%d" % self.current_time)
        self.paint_line(100)
        self.canvas.update()

        time.sleep(2)
        print("current time is", end=":")
        self.paint_line(300)
        self.canvas.update()

    def ui_thread_start(self):
        #self.window_init()
        self.ui_thread = threading.Thread(target=self.ui_thread_func)
        self.ui_thread.start()

    def paint_line(self, y):
        line = self.canvas.create_line(self.current_time*10, y, self.current_time*10+50, y)
        self.canvas.update()



