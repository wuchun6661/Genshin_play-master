# -*- coding=utf-8 -*-
"""
作者：wcy
日期：2024年5月9日
时间：16：57：03
"""
import time
import win32gui


class My_gui32:
    def __init__(self):
        self._hwndMain = -1  # 主窗口
        self.imgx = -1
        self.imgy = -1
        self.timeBegin = time.time()
        self.timeEnd = time.time()

        self.get_YuanShen_Hwnd()

    # 得到原神窗口句柄 title = 原神
    def get_YuanShen_Hwnd(self):
        self._hwndMain = -1
        Thwnd = -1
        hwndList = self.get_child_windows(0)
        for hwnd in hwndList:
            try:
                className = win32gui.GetClassName(hwnd)
                title = win32gui.GetWindowText(hwnd)
                # print(className, title)
                if className == 'UnityWndClass':
                    if title == '原神':
                        # print(hwnd, className, title)
                        # left, top, right, bottom = win32gui.GetWindowRect(hwnd)

                        Thwnd = hwnd  # 回传参数，break
                        break
            except:
                pass

        if Thwnd != -1:
            left, top, right, bottom = win32gui.GetWindowRect(Thwnd)
            print('发现原神窗口，hwnd:', Thwnd, ' 窗口：', str(left) + " " +
                  str(top) + " " + str(right) + " " + str(bottom) + ' w= ' + str(right - left)
                  + " h= " + str(bottom - top))
            self._hwndMain = Thwnd
            # self.get_child_windows(self._hwndMain)
            # print(self.get_child_windows(self._hwndMain),666)
        else:
            print("未发现原神窗口")

    def get_child_windows(self, parent):
        '''
        获得parent的所有子窗口句柄
        返回子窗口句柄列表
        '''
        # if not parent:
        #    return
        hwndChildList = []
        win32gui.EnumChildWindows(parent, lambda hwnd, param: param.append(hwnd), hwndChildList)
        return hwndChildList
    @property
    # 将方法变成属性来调用
    def hwndMain(self):
        return self._hwndMain
