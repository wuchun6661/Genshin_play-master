# pynput参考资料 https://blog.csdn.net/forward_huan/article/details/107991355

import time
from threading import Thread

import win32api

import play
from gui32 import My_gui32
import playsound

def main():
    # 检测框的中心坐标
    detect_pos = [[420, 720],
                  [636, 720],
                  [852, 720],
                  [1068, 720],
                  [1284, 720],
                  [1500, 720]]

    my = My_gui32()

    # 如果没找到原神窗口，则直接退出
    if my.hwndMain == -1:
        exit(0)

    # 启动6个线程
    for i in range(6):
        thread = Thread(target=play.window_capture, daemon=True, args=(my.hwndMain, str(i+1), detect_pos[i]))
        thread.start()

    # 检测退出按键
    while True:
        if win32api.GetKeyState(ord('Q')) < 0:  # [-127 1 -128 0]循环，其中负数是按下，非负数是抬起，且有些类似于Ctrl的按键是全局的
            break
        time.sleep(0.1)

    playsound.playsound("../sounds/close_sound.m4a")
    print("程序结束")
    exit(0)


if __name__ == "__main__":
    main()


