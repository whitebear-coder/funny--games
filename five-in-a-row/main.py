'''
this function is the main of gobang
anthor: white_mai
email: 18341491429@163.com
'''

import ui
import ai
import database
from graphics import *


def main():
    # change为1电脑先手，change1为玩家先手
    change = 1
    #
    win = ui.gobangwin()
    for i in range(database.high+1):
        for j in range(database.row+1):
            database.whole.append((i, j))
    # 各个点
    print(database.whole)

    g = 0
    m = 0
    n = 0
    # 搜索的深度
    database.DEPTH -= 1

    while g == 0:
        # 电脑先手
        if change % 2 == 1:
            # 初始情况
            if change == 1:
                pos = (7, 7)
                # ai点下过的棋子
                database.AItotal.append(pos)
                # 所有下过的点11
                database.Alltotal.append(pos)
            # 非初始情况
            if change != 1:
                pos = ai.AIthink()
                if pos in database.Alltotal:
                    print("error")

                database.AItotal.append(pos)
                database.Alltotal.append(pos)

            print(pos[0]+1, pos[1]+1, "\n")
            # 画白点
            piece = Circle(Point(database.width * pos[0]+20, database.width * pos[1]+20), 16)
            piece.setFill('white')
            piece.draw(win)

            if ui.game_win(database.AItotal):
                # 文本
                message = Text(Point(50, 50), "白棋胜利！")
                message.draw(win)
                # 推出循环
                g = 1
            # 转换成黑棋下棋
            change = change + 1

        # 玩家先手
        else:
            #
            p2 = win.getMouse()
            if not ((round((p2.getX()-20) / database.width), round((p2.getY()-20) / database.width)) in database.Alltotal):
                # 玩家输入的点
                a2 = round((p2.getX()-20) / database.width)
                b2 = round((p2.getY()-20) / database.width)
                # 玩家下过的点
                database.Playertotal.append((a2, b2))
                # 总的点
                database.Alltotal.append((a2, b2))
                # 画黑点
                piece = Circle(Point(database.width * a2+20, database.width * b2+20), 16)
                piece.setFill('black')
                piece.draw(win)
                if ui.game_win(database.Playertotal):
                    message = Text(Point(100, 100), "黑棋胜利！")
                    message.draw(win)
                    g = 1

                change = change + 1
    '''
    message = Text(Point(100, 120), "单击退出")
    message.draw(win)
    '''
    win.getMouse()
    win.close()


# 主函数用于程序的轮转运行
if "_name_=='_main_'":
    main()
