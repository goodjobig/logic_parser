import os
import csv

# if not os.path.isfile(csv_path):
#     print('地址错误!!!')
#     select = input("按q退出  其他继续:")
#     if select == 'q':
#         os.sys.exit(0)
#     filename = open_select_box()
#     return BaseLogicParse.parse_csv(filename)
# csv_file = open(csv_path, 'r')
# reader = csv.reader(csv_file)
path = r'C:\Users\123\Desktop\X21.csv'
if os.path.isfile(path):
    f = open(path, 'r')
    reader = csv.reader(f)
    # print(reader)
    for row in reader:
        print(row)
# if __name__ == '__main__':
#     pass

