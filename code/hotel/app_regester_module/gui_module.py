from tkinter import *

class Main_windows(object):
    def __init__(self):
        self.name = ""

        self.window = Tk()
        self.main_frame = Frame(self.window, width=1300, height=700, bd=0)
        self.button = Button(self.main_frame, width=7, text='self.name', bg='blue', fg='blue', command=self.click)
        self.enty = Entry(self.main_frame, width=20, font=12, bd=0, bg='blue')

    def click(self):
        self.name = self.enty.get()
        print(self.name)

    def main(self):
        self.window.geometry("400x400")
        self.main_frame.place(x=0, y=0)
        self.button.place(x=200, y=100)
        self.enty.place(x=100, y=50)

        self.window.mainloop()

M = Main_windows()
M.main()