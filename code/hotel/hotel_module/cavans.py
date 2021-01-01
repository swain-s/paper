from tkinter import *
# 创建窗口
root = Tk()
root.geometry("800x600")
# 创建并添加Canvas
first_frame = Frame(root, width=800, height=600)
first_frame.pack()

cv = Canvas(first_frame, background='blue', width=400, height=300)
cv.place(x=0, y=0)

cv.create_rectangle(30, 30, 20, 200,
    outline='red', # 边框颜色
    stipple = 'question', # 填充的位图
    fill="red", # 填充颜色
    width=5 # 边框宽度
    )
cv.create_oval(240, 30, 330, 200,
    outline='yellow', # 边框颜色
    fill='pink', # 填充颜色
    width=4 # 边框宽度
    )

def f1():
    cv.destroy()

button = Button(cv, width=10, height=1, command=f1)
button.place(x=50, y=200)



root.mainloop()