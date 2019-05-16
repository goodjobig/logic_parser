# from tkinter import *

import tkinter
from tkinter.constants import *

WIDTH = 500
HEIGHT = 300


class ContainerUI:
    def __init__(self):
        global WIDTH
        global HEIGHT
        self.tk = tkinter.Tk()
        self.tk.geometry('%sx%s' % (WIDTH, HEIGHT))
        self.tk.title = '逻辑分析仪数据解析  logic data format parser'
        self.frame = tkinter.Frame(self.tk, relief=RIDGE, borderwidth=2)
        self.frame.pack(fill=BOTH, expand=1)
        # label = tkinter.Label(self.frame, text="Hello, World")
        # label.pack(fill=X, expand=1)
        # button = tkinter.Button(self.frame, text="Exit", command=self.tk.destroy)
        # button.pack(side=BOTTOM)
        # rd1 = tkinter.Radiobutton(self.frame, text='logic1', value=0, variable=0)
        # rd2 = tkinter.Radiobutton(self.frame, text='logic2', value=1, variable=1)
        # rd3 = tkinter.Radiobutton(self.frame, text='logic3', value=2, variable=0)
        # rd1.pack(fill=X, expand=1)
        # rd2.pack(fill=X, expand=1)
        # rd3.pack(fill=X, expand=1)
        self.show_first_ui()
        self.tk.mainloop()

    def show_first_ui(self):
        label = tkinter.Label(self.frame, text="欢迎使用逻辑分析仪数据解析！！", font=('', 16))
        label.pack()


    def close_tk(self):
        self.tk.destroy()


if __name__ == '__main__':
    ui = ContainerUI()
