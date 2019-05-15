import os
import time


fps = 60
start_time = 0


def start_count_time():
    global start_time
    start_time = time.time()
    x = 1000
    while x:
        c_time = time.time()
        print(c_time - start_time)
        x -= 1


def update(content):
    interval_time = 1 / fps
    os.system('cls')
    print(content)


if __name__ == '__main__':
    start_count_time()
