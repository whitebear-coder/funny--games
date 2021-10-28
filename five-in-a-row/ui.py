'''
该文件为五子棋的ui，用于绘制棋盘，
棋盘输赢判断
author: white_mai
email:18341491429@163.com
'''

import database
from graphics import *


# gobang棋盘界面
def gobangwin():#界面
    # 设置界面的大小
    win = GraphWin("第六组---啦啦队的gobang盘", database.width * database.high+40, database.width * database.row+40)
    # 设置背景颜色
    win.setBackground("burlywood")
    i1 = 20
    # 行的线
    while i1 <= database.width * database.high+20:
        l = Line(Point(i1, 20), Point(i1, database.width * database.high+20))
        l.draw(win)
        i1 = i1 + database.width

    i2 = 20
    # 竖的线
    while i2 <= database.width * database.row+20:
        l = Line(Point(20, i2), Point(database.width * database.row+20, i2))
        l.draw(win)
        i2 = i2 + database.width
    return win


# 判断胜利的标准
def game_win(list):
    for m in range(database.high+1):
        for n in range(database.row+1):
            # 棋盘上的点都下过，在List中能找到
            if n < database.row+1 - 4 and (m, n) in list and (m, n + 1) in list and (m, n + 2) in list and (
                    m, n + 3) in list and (m, n + 4) in list:
                return True
            elif m < database.row+1 - 4 and (m, n) in list and (m + 1, n) in list and (m + 2, n) in list and (
                        m + 3, n) in list and (m + 4, n) in list:
                return True
            elif m < database.row+1 - 4 and n < database.row+1 - 4 and (m, n) in list and (m + 1, n + 1) in list and (
                        m + 2, n + 2) in list and (m + 3, n + 3) in list and (m + 4, n + 4) in list:
                return True
            elif m < database.row+1 - 4 and n > 3 and (m, n) in list and (m + 1, n - 1) in list and (
                        m + 2, n - 2) in list and (m + 3, n - 3) in list and (m + 4, n - 4) in list:
                return True
    return False

