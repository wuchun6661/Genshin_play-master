import win32gui, win32ui, win32con, win32api
import time
import cv2
import numpy as np
from threading import Thread


def key_loop(num, short_list, long_list, flag):
    time_delay = 0.25
    keys_num = {"1": 65,
                "2": 83,
                "3": 68,
                "4": 74,
                "5": 75,
                "6": 76}  # A S D J K L
    while True:
        time.sleep(0.01)
        # 触发短按
        if short_list[0]:
            # print('*********')
            short_list[0] = 0  # 复原标志位
            time.sleep(time_delay)

            win32api.keybd_event(keys_num[num], 0, 0, 0)
            win32api.keybd_event(keys_num[num], 0, win32con.KEYEVENTF_KEYUP, 0)

        # 触发长按
        if long_list[0]:
            long_list[0] = 0  # 复原标志位
            time.sleep(time_delay)

            if flag[0] < 0:
                win32api.keybd_event(keys_num[num], 0, 0, 0)
            else:
                win32api.keybd_event(keys_num[num], 0, win32con.KEYEVENTF_KEYUP, 0)

            flag[0] = -flag[0]  # 翻转标志位


def window_capture(hwnd=0, num="2", pos_char=None):
    if pos_char is None:
        pos_char = [852, 720]

    short_list = [0]
    long_list = [0]
    flag = [-1]
    yellow_interval = 0.12
    purple_interval = 0.15
    last_time = time.time()
    thread = Thread(target=key_loop, daemon=True, args=(num, short_list, long_list, flag))  # 创建一个子线程，用于接收数据
    thread.start()  # 启动子线程
    ###########尺寸###########
    d = 150  # 监测区域边长
    pos_circle = [pos_char[0], pos_char[1]]  # 圆心位置
    start_wh = (pos_circle[0] - d // 2, pos_circle[1] - d // 2)  # 检测框左上角坐标
    end_wh = (start_wh[0] + d, start_wh[1] + d)  # 检测框右下角坐标
    size_wh = (d, d)  # 检测区域的宽高
    w = d
    h = d

    # hwnd = 0  # 窗口的编号，0号表示当前活跃窗口
    hwndDC = win32gui.GetWindowDC(hwnd)  # 根据窗口句柄获取窗口的设备上下文DC(Divice Context)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)  # 根据窗口的DC获取mfcDC
    saveDC = mfcDC.CreateCompatibleDC()  # mfcDC创建可兼容的DC
    saveBitMap = win32ui.CreateBitmap()  # 创建bigmap准备保存图片
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)  # 为bitmap开辟空间

    print("线程" + num + "已启动")
    ###################################################
    while True:
        saveDC.SelectObject(saveBitMap)  # 高度saveDC，将截图保存到saveBitmap中
        saveDC.BitBlt((0, 0), size_wh, mfcDC, start_wh, win32con.SRCCOPY)  # 截取从(100，100)长宽为(w，h)的图片

        signedIntsArray = saveBitMap.GetBitmapBits(True)
        im_opencv = np.frombuffer(signedIntsArray, dtype='uint8')
        im_opencv.shape = (h, w, 4)
        im_opencv = cv2.cvtColor(im_opencv, cv2.COLOR_BGRA2BGR)
        ###############################检测################################

        Filename_yellow = "../imgs/yellow.png"
        yellow = cv2.imread(Filename_yellow)

        Filename_purple = "../imgs/purple.png"
        purple = cv2.imread(Filename_purple)

        res1 = cv2.matchTemplate(im_opencv, yellow, cv2.TM_CCOEFF_NORMED)  # 模板匹配
        threshold1 = 0.5
        loc1 = np.where(res1 >= threshold1)

        res2 = cv2.matchTemplate(im_opencv, purple, cv2.TM_CCOEFF_NORMED)  # 模板匹配
        threshold2 = 0.5
        loc2 = np.where(res2 >= threshold2)

        # print(loc)
        for pt in zip(*loc1[::-1]):
            flag[0] = -1
            now = time.time()

            # 筛除短时间内的重复检测
            if now - last_time < yellow_interval:
                break
            # print(flag[0])
            short_list[0] = 1
            last_time = now
            break

        for pt in zip(*loc2[::-1]):
            now = time.time()
            if now - last_time < purple_interval:
                break
            long_list[0] = 1
            last_time = now
            break

        #################################################################
        # cv2.imshow(num, im_opencv)  # 显示
        # #
        # if (cv2.waitKey(1) & 0xFF) == ord('q'):  # 其实有无0xFF都可，加上防止返回值超过255，和‘1’的ascii码比较
        #     break
    #######################################################
    # 释放内存
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)
    # 关闭all窗口
    cv2.destroyAllWindows()
    print("线程" + num + "已结束")
