import re
import csv
import os.path
from abc import abstractmethod
from logic_parse.c_file_parse import TPCFileFactory
from logic_parse.base_format import IICDataGroup, IICDataGroupList, MIPIDataGroup , MIPIDataGroupList
from utils.window_utils import open_select_box


class TPCFileMixin:
    def to_c_file(self):
        assert isinstance(self, BaseLogicParse)
        cff = TPCFileFactory(self.py_list)
        cff.parse()


class InitStringMixin:
    def to_init_string(self):
        assert isinstance(self, BaseLogicParse)
        s = ''
        for i in self.py_list:
            sd_pack = 'SSD2828_WritePackageSize(%s);\n' % len(i)
            s += sd_pack
            for item in i:
                sd = 'SPI_WriteData(%s);\n' % item
                s += sd
            s += '\n'
        return s


class BaseLogicParse:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.csv_reader = self.parse_csv(self.csv_path)
        self.csv_list = self.select_col(self.csv_reader)
        self.py_list = self.res_2python_list(self.csv_list)
        assert isinstance(self.py_list, IICDataGroupList) or isinstance(self.py_list, MIPIDataGroupList), "py_List 必须是 DataGroupList 或 MIPIDataGroupList 类型"
        self.display()

    @staticmethod
    def parse_csv(csv_path):
        if not os.path.isfile(csv_path):
            print('地址错误!!!')
            select = input("按q退出  其他继续:")
            if select == 'q':
                os.sys.exit(0)
            filename = open_select_box()
            return BaseLogicParse.parse_csv(filename)
        csv_file = open(csv_path, 'r')
        reader = csv.reader(csv_file)
        return reader

    @abstractmethod
    def res_2python_list(self, csv_list):
        ''' format the csv_list as [addr,write_or_read[,data1,data2....]]
        :param csv_list: splited csv reader list
        :return:[[addr,write_or_read[,data1,data2....]],...]
        '''
        pass

    @abstractmethod
    def select_col(self, csv_reader):
        pass

    def display(self):
        def check(value):
            if value and value.isdigit():
                value = int(value)
            else:
                return False
            return value
        if len(self.py_list) >= 1:
            self.py_list.show()
            start = input("输入起始行:")
            end = input("输入结束行:")
            start = check(start)
            end = check(end)
            if start is False:
                start = 0
            if end is False:
                end = None
            self.py_list[start:end]
            self.py_list.show()
        else:
            # raise ValueError("未检测到有效数据")
            pass


class IICLogicParse(BaseLogicParse, TPCFileMixin):
    def select_col(self, csv_reader):
        result = []
        for col in csv_reader:
            result.append(col)
        return result

    def res_2python_list(self, csv_list):
        # groups = []
        # group = []
        dgl = IICDataGroupList()
        list_arg = csv_list[1:]
        p_for_block = re.compile(r'setup\s(?P<wr_mode>(write)|(read))\sto\s\[(?P<addr>0x\w{2})\]')
        for item in list_arg:
            effect_value = item[-1]
            start = re.search(p_for_block, effect_value.lower())
            if start:
                dg = IICDataGroup()
                dgl.append(dg)
                wr_mod = 0 if start.group('wr_mode') == 'write' else 1
                addr = start.group('addr')
                dg.addr = addr
                dg.wr_mode = wr_mod
            else:
                try:
                    if effect_value == '':
                        continue
                    dg.append(effect_value[:4])
                except NameError:
                    pass
        return dgl


class IICLaLogicParse(BaseLogicParse, TPCFileMixin):
    def select_col(self, csv_reader):
        result = []
        for col in csv_reader:
            result.append(col[2:11])
        # for index, val in enumerate(result):
        #     print(index, val)
        return result[1:]

    def res_2python_list(self, csv_list):
        dgl = IICDataGroupList()
        data_pattern = re.compile(r'[a-f0-9]{2}')
        wr_pattern = re.compile(r'(wr)|(rd)')
        insignificance = re.compile(r'\s+')
        for item in csv_list:
            if not item:
                continue
            is_insignificance = re.match(insignificance, item[0].lower())
            if item and not is_insignificance:
                # 解析地址
                temp_addr = re.search(data_pattern, item[0].lower())
                mod = re.search(wr_pattern, item[0].lower())
                if temp_addr and mod:
                    dg = IICDataGroup()
                    dgl.append(dg)
                    addr = temp_addr.group(0)
                    addr = int(addr, base=16)
                    addr_8bit = hex(addr << 1)
                    dg.addr = addr_8bit
                    # 解析模式
                    mod = mod.group(0)
                    mod = 0 if mod.lower() == 'wr' else 1
                    dg.wr_mode = mod
                # 将地址和读写模式加入大组
            for data in item[1:]:
                if not data or data == ' ':
                    break
                data = re.search(data_pattern, data.lower())
                if not data:
                    continue
                data = data.group(0)
                data = '0x' + data
                try:
                    dg.append(data)
                except NameError:
                    pass
        return dgl


class IICSaleLogicParse(BaseLogicParse, TPCFileMixin):
    def select_col(self, csv_reader):
        result = []
        for col in csv_reader:
            result.append(col[1:])
        return result[1:]

    def res_2python_list(self, csv_list):
        dgl = IICDataGroupList()
        # is_group_change = 0
        pre_group = None
        wr_pattern = re.compile(r'(write)')
        dg = IICDataGroup()
        for item in csv_list:
            if not item[0].isdigit():
                continue
            if pre_group != int(item[0]):
                if dg.addr:
                    dgl.append(dg)
                    dg = IICDataGroup()
                pre_group = int(item[0])
                dg.addr = item[1]
                w_search = re.search(wr_pattern, item[3].lower())
                print(w_search)
                dg.wr_mode = 0 if w_search else 1
            dg.append(item[2])
        return dgl


class MIPILogicParse(BaseLogicParse, InitStringMixin):

    def select_col(self, csv_reader):
        result = []
        for row in csv_reader:
            r_row = row[4:5] + row[7:15]
            result.append(r_row)
        return result[1:]

    def res_2python_list(self, csv_list):
        dgl = MIPIDataGroupList()
        for row in csv_list:
            if row[0] and len(row[0]) > 10:
                try:
                    dgl.append(data_group)
                except UnboundLocalError as e:
                    pass
                data_group = MIPIDataGroup()
            elif not row[1]:
                continue
            row = row[1:]
            try:
                data_group.append(*row)
            except UnboundLocalError:
                pass
        dgl.append(data_group)
        return dgl



if __name__ == '__main__':
    # logic_parse = IICLogicParse(r'C:\Users\123\Desktop\schedule\2019-04-11\12103207_X850_A32F_ST7701S_5.0_480x854_2LINE_OK\a32f_start.csv')
    # logic_parse.to_c_file()
    # logic_parse = IICLaLogicParse(r'C:\Users\123\Desktop\schedule\2019-04-08\12201680_X850_X5010_ILI9881C_AUO550_720X1280_3L_TP\12102164_X850_X522_ILI9881C_HSD52_720X1280_4L_TP_ok\start.csv')
    # logic_parse.to_c_file()
    pass
