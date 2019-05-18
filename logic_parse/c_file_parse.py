import string
import os
from logic_parse.base_format import IICDataGroupList


BASE_TARGET_PATH = os.path.join(os.environ.get('USERPROFILE'), 'Desktop')
TARGET_PATH = os.path.join(BASE_TARGET_PATH, 'TP_DATA_OUT_PUT')

_C_FILE_DATA_CONTENT = ''''''

_C_FILE_TEMPLATE = \
'''
#include "tp_init.h"\n
extern u8 tp_delay;\n
#define Delay tp_delay\n
void Tp_Init_For_La(void){\n
  u8 dataBuff[64];\n
${content}\n
}\n
'''


_H_FILE_TEMPLATE = \
'''
#ifndef TP_INIT_H
#define TP_INIT_H\r\n
#include "TouchPoint.h"\r\n
void Tp_Init_For_La(void);\r\n
# endif //TP_INIT_H\r\n
'''

C_FILE_DATA_WRITE = '  I2C_Write({a},dataBuff,{length},Delay);\n'
C_FILE_DATA_READ = '  I2C_Read({a},dataBuff,{length},Delay);\n'
C_FILE_DATA_BUFF = '  dataBuff[${index}] = ${hex_value};\n'

Read_Func = 'I2C_Read'
Write_Func = 'I2C_Write'


def file_select_loop(base_path, full_path):
    while 1:
        file_name = input('文件名:')
        path = os.path.join(base_path, file_name)
        if os.path.isfile(path):
            print("文件已经存在 是否覆盖 y覆盖")
            select = input(":")
            if select.lower() == 'y':
                rename_replace = True
                break
            else:
                print("重新输入")
        else:
            rename_replace = False
            break
    if not rename_replace:
        os.rename(full_path, path)
    else:
        os.replace(full_path, path)


class TPCFileFactory:

    def __new__(cls, *args, **kwargs):
        print(type(args[0]))
        if len(args) == 1 and isinstance(args[0], IICDataGroupList):
            obj = super().__new__(cls)
        else:
            raise ValueError("有且只有一个类型位DataGroupList的参数!")
        return obj

    def __init__(self, py_list):
        global _C_FILE_DATA_CONTENT
        global C_FILE_DATA_WRITE
        global C_FILE_DATA_READ
        global C_FILE_DATA_BUFF
        self.data_source = py_list
        self.template = string.Template(_C_FILE_TEMPLATE)
        # for data in self.data_source:
        #     # addr = data[0]
        #     # wr_mode = data[1]
        #     if data.wr_mode == 0:
        #         for index, d in enumerate(data):
        #             data_buffer = string.Template(C_FILE_DATA_BUFF)
        #             temp = data_buffer.substitute({'index': index, 'hex_value': d})
        #             _C_FILE_DATA_CONTENT += temp
        #         _C_FILE_DATA_CONTENT += C_FILE_DATA_WRITE.format(a=data.addr, length=len(data))
        #     else:
        #         _C_FILE_DATA_CONTENT += C_FILE_DATA_READ.format(a=data.addr, length=len(data))
        self.res = None

    def clear_data(self):
        global _C_FILE_DATA_CONTENT
        global C_FILE_DATA_WRITE
        global C_FILE_DATA_READ
        global C_FILE_DATA_BUFF
        for data in self.data_source:
            if data.wr_mode == 0:
                for index, d in enumerate(data):
                    data_buffer = string.Template(C_FILE_DATA_BUFF)
                    temp = data_buffer.substitute({'index': index, 'hex_value': d})
                    _C_FILE_DATA_CONTENT += temp
                _C_FILE_DATA_CONTENT += C_FILE_DATA_WRITE.format(a=data.addr, length=len(data))
            else:
                _C_FILE_DATA_CONTENT += C_FILE_DATA_READ.format(a=data.addr, length=len(data))
        return _C_FILE_DATA_CONTENT

    def parse(self):
        s = self.clear_data()
        self.res = self.template.safe_substitute(content=s)
        print('parse to c file start...')
        if not os.path.isdir(TARGET_PATH):
            os.mkdir(TARGET_PATH)
        c_path = os.path.join(TARGET_PATH, 'tp_init.c')
        if os.path.isfile(c_path):
            select = input('tp_init.c 已经存在 按y覆盖, 按其他给前文件重命名')
            if select.lower() != 'y':
                file_select_loop(TARGET_PATH, c_path)
        with open(c_path, 'w') as f:
            f.write(self.res)
        print('parsed to c file end...')
        print('start generate h file...')
        h_path = os.path.join(TARGET_PATH, 'tp_init.h')
        with open(h_path, 'w') as f:
            f.write(_H_FILE_TEMPLATE)
        print('generated h file end...')



