import os
import time
from utils.window_utils import open_select_box
from logic_parse import compatible_logic_parse


def delay_second(t_time):
    if isinstance(t_time, int):
        while t_time:
            time.sleep(1)
            t_time -= 1


def main():
    while 1:
        print("请选着逻辑分析仪类型 1: acute logic |  2:saleae logic 3 saleae logic mode 2 默认为 acute Logic(enter) | q: quit ")
        choice = input()
        if choice == '2':
            logic_obj = 'IICLogicParse'
        elif choice == 'q':
            break
        elif choice == '3':
            logic_obj = 'IICSaleLogicParse'
        elif choice == '4':
            logic_obj = 'MIPILogicParse'
        else:
            logic_obj = 'IICLaLogicParse'

        filename = open_select_box()
        logic_parse = getattr(compatible_logic_parse, logic_obj)(filename)
        try:
            logic_parse.to_c_file()
        except AttributeError:
            print(logic_parse.to_init_string())
        count = 3
        while count:
            print("解析 成功 %ss后退出 ... " % count)
            time.sleep(1)
            count -= 1
        os.sys.exit(0)


if __name__ == '__main__':
    main()
