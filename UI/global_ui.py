# from tkinter import *

import tkinter
import tkinter.messagebox
from utils.window_utils import open_select_box
from tkinter.constants import *
from logic_parse import compatible_logic_parse

WIDTH = 1000
HEIGHT = 600


class ContainerUI:
    def __init__(self):
        global WIDTH
        global HEIGHT
        self.tk = tkinter.Tk()
        self.tk.geometry('%sx%s' % (WIDTH, HEIGHT))
        self.tk.title('逻辑分析仪数据解析  logic data format parser')
        self.tk.resizable(0, 0)
        self.filename = tkinter.StringVar()
        self.label_str = tkinter.StringVar()
        self.label_str.set("欢迎使用逻辑分析仪数据解析器！！！")
        self.select_logic = tkinter.StringVar()

        self.radio_list = ['acute', 'seleae_logic1', 'seleae_logic2', 'lcd_mipi']
        self.warning_msg = tkinter.StringVar()
        self.frame = tkinter.Frame(self.tk, relief=RIDGE, borderwidth=2, width=WIDTH, height=HEIGHT, bg='#f6f6f6')
        self.frame.pack(fill=BOTH, expand=1)
        self.canvas = tkinter.Canvas(master=self.frame, width=800, height=250)
        self.format_img = None
        self.text = None
        self.parse_btn = None
        self.current_page = 1
        self.warning_box = tkinter.Message(self.frame)
        self.show_first_ui()
        self.tk.mainloop()

    def clear_frame(self):
        self.frame.destroy()
        self.frame = tkinter.Frame(self.tk, relief=RIDGE, borderwidth=2, width=WIDTH, height=HEIGHT, bg='#f6f6f6')
        self.frame.pack(fill=BOTH, expand=1)

    def go_next_ui(self, select):
        print(select)

    def show_first_ui(self):
        y_btn = 80
        tp_btn = tkinter.Button(
            self.frame,
            text='开始 解析',
            width=10,
            height=2,
            font=('', 18),
            padx=5,
            pady=2,
            command=self.show_parser_ui,
        )
        tp_btn.place(x=WIDTH/2 - 80, y=y_btn)
        # mp_btn = tkinter.Button(
        #     self.frame,
        #     text='MIPI 解析',
        #     width=10, height=2,
        #     font=('', 18),
        #     padx=5,
        #     pady=2,
        #     command=self.show_mipi_ui,
        # )
        # mp_btn.place(x=WIDTH/2 - 80, y=y_btn+80)
        # btn = tkinter.Button(self.bottom_frm, text='下一步', command=self.go_next_ui)
        # btn.pack(side=BOTTOM)

    def show_parser_ui(self):
        self.label_str.set("欢迎使用逻辑分析仪数据解析工具！！！")
        self.clear_frame()
        radio_place = dict(
            x=12,
            y=82,
            width=100,
            height=32,
        )
        radio_config = dict(
            master=self.frame,
            value=0,
            variable=self.select_logic,
            text='acute',
            command=self.check_logic,
        )
        for i, radio in enumerate(self.radio_list):
            radio_config['value'] = i
            setattr(self, radio, tkinter.Radiobutton(**radio_config))
            r = getattr(self, radio)
            r.configure(text=radio)
            radio_place['x'] = i*radio_place['width'] + 40
            if i == 0:
                r.select()
            else:
                r.deselect()
            r.place(**radio_place)

        self.show_format(self.radio_list[0])
        file_btn = tkinter.Button(
            self.frame,
            text='选择文件',
            height=1,
            command=self.get_file,
        )
        file_btn.place(x=400, y=120)
        file_entry = tkinter.Entry(
            self.frame,
            width=45,
            selectborderwidth=1,
            textvariable=self.filename,
        )
        file_entry.place(x=52, y=125)

        self.parse_btn = tkinter.Button(
            self.frame,
            text='解 析',
            width=5,
            height=1,
            font=('', 16),
            command=self.parser,
        )
        self.parse_btn.place(x=520, y=40)

        file_btn = tkinter.Button(
            self.frame,
            text='清 空',
            width=5,
            height=1,
            font=('', 16),
            command=self.res_clear,
        )
        file_btn.place(x=620, y=40)
        scroll = tkinter.Scrollbar(master=self.frame, background='white')
        scroll.place(x=WIDTH-32, y=120, width=24, height=400)
        self.text = tkinter.Text(self.frame, font=('', 14), yscrollcommand=scroll.set)
        self.text.place(x=520, y=120, width=450, height=400)
        scroll.config(command=self.text.yview)

    def get_file(self):
        filename = open_select_box()
        self.filename.set(filename)

    def check_logic(self):
        select = self.select_logic.get()
        x = self.radio_list[int(select)]
        self.show_format(x)

    def close_tk(self):
        self.tk.destroy()

    def show_format(self, select):
        self.canvas = tkinter.Canvas(master=self.frame, width=400, height=300)
        self.format_img = tkinter.PhotoImage(master=self.frame, file='%s.gif' % select)
        self.canvas.create_image(0, 0, anchor='nw', image=self.format_img)
        self.canvas.place(x=50, y=200)

    def parser(self):
        if self.filename.get():
            print('start parse !!!')
            logic_sel = self.select_logic.get()
            logic_sel = int(logic_sel)
            logic_obj = ''
            self.parse_btn.configure(state='disabled')
            if logic_sel == 0:
                logic_obj = 'IICLaLogicParse'
            elif logic_sel == 1:
                logic_obj = 'IICLogicParse'
            elif logic_sel == 2:
                logic_obj = 'IICLaLogicParse'
            elif logic_sel == 3:
                logic_obj = 'MIPILogicParse'
            else:
                print('i do not konw operate!')
            try:
                logic_parse = getattr(compatible_logic_parse, logic_obj)(self.filename.get())
                res = logic_parse.to_init_string()
                if not len(res):
                    tkinter.messagebox.showwarning(title='解析错误', message='请确认csv表内容,复合左图格式。')
                del logic_parse
                self.text.insert(tkinter.INSERT, res)
            except AssertionError:
                tkinter.messagebox.showwarning(title='解析错误', message='请确认csv表内容,复合左图格式。')
            self.parse_btn.configure(state='normal')

        else:
            msg_box = tkinter.Message(self.frame)
            msg_box.place(x=WIDTH/2, y=HEIGHT/2)

    def res_clear(self):
        self.text.delete(1.0, tkinter.END)


if __name__ == '__main__':
    ui = ContainerUI()
