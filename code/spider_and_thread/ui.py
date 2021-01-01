from tkinter import *
import threading
import time

#*************   Moudle   **************************
class m_event(object):
    def __init__(self, op, v_queue):
        self.op = op     # add, delete, update
        self.title = "news tittle"   #  class, tittle, message
        self.message = []            #  class, tittle, message

        self.queue = v_queue

class Moudle(object):
    def __init__(self):
        self.queue = []
        self.md_thread = threading.Thread(target=self.md_thread_func)


    def md_thread_func(self):
        while True:
            try:
                if len(self.queue) > 0:
                    e = self.queue.pop(0)
                    print("M: handing")
                    if e.op == "get":
                        time.sleep(2)

                        fir_b_event = event("add")
                        e.queue.append(fir_b_event)
                    elif e.op == "get1":
                        time.sleep(2)

                        fir_b_event = event("add2")
                        e.queue.append(fir_b_event)
            except:
                print("+")

    def main(self):
        self.md_thread.start()


#**************   View    ***************************
class widget_node(object):
    def __init__(self, id, type, widg):
        self.id = id
        self.type = type
        self.widg = widg

        self.left = None
        self.right = None

class event(object):
    def __init__(self, op):
        self.op = op
        self.type = "button"
        self.target = 1

class View(object):
    def __init__(self, m_queue):
        self.queue = []
        self.ui_thread= threading.Thread(target=self.ui_thread_func)

        self.root_w = widget_node(0, "window", Tk())
        self.root_w.widg.geometry("200x200")

        self.m_queue = m_queue

    def ui_thread_func(self):
        while True:
            try:
                if len(self.queue) > 0:
                    e = self.queue.pop(0)
                    print("V:handing")
                    if e.op == "add":
                        self.root_w.left.left.widg.destroy()
                        sec_b = widget_node(3, "button", Button(self.root_f.widg, width=10, height=2, bg="yellow",
                                                                     command=self.sec_b_func))
                        sec_b.widg.place(x=100, y=100)
                        self.root_w.left.left = sec_b
                    elif e.op == "add2":
                        self.root_w.left.left.widg.destroy()
                        fir_b = widget_node(2, "button", Button(self.root_f.widg, width=10, height=2, bg="yellow",
                                                                     command=self.fir_b_func))
                        fir_b.widg.place(x=0, y=0)
                        self.root_w.left.left = fir_b
            except:
                print("-")

    def fir_b_func(self):
        print("V: B : 1")
        fir_b_event = m_event("get", self.queue)
        self.m_queue.append(fir_b_event)

    def sec_b_func(self):
        print("V: B: 2")
        fir_b_event = m_event("get1", self.queue)
        self.m_queue.append(fir_b_event)


    def init(self):
        self.root_f = widget_node(1, "frame", Frame(self.root_w.widg, width=200, height=200, bg="red"))
        self.root_w.left = self.root_f
        self.root_f.widg.place(x=0, y=0)

        self.fir_b = widget_node(2, "button", Button(self.root_f.widg, width=10, height=2, bg="yellow", command=self.fir_b_func))
        self.root_f.left = self.fir_b
        self.fir_b.widg.place(x=0, y=0)

    def main(self):
        self.init()
        self.ui_thread.start()
        self.root_w.widg.mainloop()

M = Moudle()
M.main()
V = View(M.queue)
V.main()