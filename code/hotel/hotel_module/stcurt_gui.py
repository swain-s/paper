from tkinter import *

class Model(object):
    def __init__(self):
        # 主窗口、主框架、主菜单框架、入住框架、离开框架、入住按钮、
        MAIN_WINDOW, ROOT_FRAME, MENU_FRAME, VISIT_FRAME, LEAVE_FRAME, VISIT_BUTTON, LEAVE_BUTTON, FACE_BUTTON = 0, 1, 2, 3, 4, 5, 6, 7

        #样式控制数据
        self.hash_key = ["main_window", "root_frame", "menu_frane", "vist_frame", "leave_frame", "visit_button", "leave_button", "face_button"]
        self.width = [800, 800, ]
        self.height = []
        self.color = []

        #布局控制数据
        self.place_x = [None, 0, 0, 0]
        self.place_y = [None, 0, 0, 0]


        #可变数据
        self.text = []

    def edit_text(self, who):
        pass

    def edit_color(self, who):
        pass


class Control(object):
    def __init__(self):
        MAIN_WINDOW, ROOT_FRAME, MENU_FRAME, VISIT_FRAME, LEAVE_FRAME, VISIT_BUTTON, LEAVE_BUTTON, FACE_BUTTON = 0, 1, 2, 3, 4, 5, 6, 7

        self.pre_order = None
        self.current_order = None
        self.order_pool = []
        self.old_order_pool = []

        self.control_func = [self.click_func(0x111111), self.click_func(0x1110101)]

    def click_func(self, order):
        self.order_pool.append(order)

class View(object):
    def __init__(self, Model, Control):
        self.model = Model
        self.control = Control
        MAIN_WINDOW, ROOT_FRAME, MENU_FRAME, VISIT_FRAME, LEAVE_FRAME, VISIT_BUTTON, LEAVE_BUTTON, FACE_BUTTON = 0, 1, 2, 3, 4, 5, 6, 7

        #数据
        self.width = None
        self.height = None
        self.color = None
        self.place_x = None
        self.place_y = None
        self.text = None

        #控制
        self.control_func = None
        self.pre_order = None
        self.current_order = None
        self.order_pool = []
        self.old_order_pool = []

        self.pre_handle = []
        self.current_handle = []
        self.order_handle_pool = []


        self.widget_list = []
        self.main_window = Tk()
        self.root_frame = Frame(self.main_window, width=self.width[ROOT_FRAME], height=self.height[ROOT_FRAME])
        self.menu_frame = Frame(self.root_frame, width=self.width[MENU_FRAME], height=self.height[MENU_FRAME])
        self.visit_frame = Frame(self.root_frame)
        self.leave_frame =  Frame(self.root_frame)
        self.visit_button = Button(self.menu_frame, command=self.control_func[VISIT_BUTTON])
        self.leave_button = Button(self.menu_frame, command=self.control_func[LEAVE_BUTTON])
        self.face_button = Button()

    def view_init(self):
        # 数据
        self.width = self.model.width
        self.height = self.model.height
        self.color = self.model.color
        self.place_x = self.model.place_x
        self.place_y = self.model.place_y
        self.text = self.model.text

        # 控制
        self.control_func = self.control.control_func
        
        while True:
            if len(self.order_handle_pool) > 0:
                self.current_handle = self.order_handle_pool[0]
                self.view_refresh(self.current_handle)


    def view_mainloop(self):
        pass

    def order_init(self):
        while True:
            if len(self.order_pool) > 0:
                self.current_order = self.order_pool[0]
                self.order_2_handel(self.current_order)


    def view_refresh(self, handle_tree):
        pass

    #指令翻译函数的功能：a)对于唯一指令，翻译为唯一树：代替hash表
    def order_2_handel(self, order):
        handle_tree = HandelTree()
        return handle_tree




class Node(object):
    def __init__(self, date=0, lchild=None, rchild=None):
        self.date = date
        self.lchild = lchild
        self.rchild = rchild

class HandelTree(object):
    def __init__(self):
        self.root = Node(1)
        self.size = 1
        self.tree_list = [self.root]

    def add_node(self, node):
        last_node = self.tree_list[self.size-1]
        last_node.lchild = node
        self.tree_list.append(node)
        self.size = self.size + 1


#tree = BTree()
#node1 = Node(3, None, None)
#node2 = Node(5, None, None)
#tree.add_node(node1)
#tree.add_node(node2)

class N(object):
    def __init__(self, date=None, next=None):
        self.date = date
        self.next = next

class L(object):
    def __init__(self):
        root = N(1, None)
        self.list = [root]
        self.size = 1

    def add(self, d):
        n = N(d, None)
        self.list[self.size-1].next = n
        self.list.append(n)
        self.size = self.size + 1

l = L()
l.add(5)
l.add("aaa")
l.add(["a", "b", 1])

for i in range(0, l.size):
    print(l.list[i].date)