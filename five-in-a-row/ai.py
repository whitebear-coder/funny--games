'''
该文件为ai的基础算法
author: white_mai
email: 18341491429@163.com
'''

import improvment
import database
import ui


# 该函数，对胜利，防御，攻击模型进行匹配
# 对方下棋为2
# 己方下棋为1
# 空格为0
def summodel(m, n, down, right, enemy_list, my_list, shapemodel):
    for tt in range(-4, 1):
        template = []
        # 周围的五个子
        for i in range(0, 5):
            if (m + (i + tt) * down, n + (i + tt) * right) in enemy_list:
                template.append(2)
            elif (m + (i + tt) * down, n + (i + tt) * right) in my_list:
                template.append(1)
            elif (m + (i + tt) * down, n + (i + tt) * right) in database.whole:
                template.append(0)
            else:
                template.append(-1)
        # 周围的五个子
        shap5 = (template[0], template[1], template[2], template[3], template[4])
        # 返回最优的状态
        for shape in shapemodel:
            if shap5 == shape:
                print(shap5)
                for i in range(0, 5):
                    if(template[i]==0):
                        database.best_point[0] = m + (i + tt) * down
                        database.best_point[1] = n + (i + tt) * right
                return True
    return False


# i整个的思考逻辑
def AIthink():
    # 先考虑自身是否能连成五胜利
    if improvment.victory_judge(True):
        return database.best_point[0], database.best_point[1]
    # 在进行防御判断，如果对手即将胜利， 直接返回
    elif improvment.defense_judge(True):
        return database.best_point[0], database.best_point[1]
    # 对面没有连5的情况下优先连活4
    elif improvment.attack_judge(True):
        return database.best_point[0], database.best_point[1]
    else:
        # ab剪枝
        negamax(True, database.DEPTH, -1000000000, 1000000000)
        # 返回当前下的棋
        return database.best_point[0], database.best_point[1]


# 得到局势估分
def getgrade(AIturn):
    # 双方表格
    tablequeue1 = []
    tablequeue2 = []
    # 双方得分
    bonus2 = 0
    bonus1 = 0
    # AI回合
    if AIturn:
        table1 = database.AItotal
        table2 = database.Playertotal
    # 玩家回合
    else:
        table1 = database.Playertotal
        table2 = database.AItotal
    for temp in table1:
        x = temp[0]
        y = temp[1]
        # 对我方棋盘的四个方向进行打分，打分后统计。
        # 列方向
        bonus1 = sumdirection(x, y, table2, table1, tablequeue1, 0, 1)+bonus1
        # 行方向
        bonus1 = sumdirection(x, y, table2, table1, tablequeue1, 1, 0)+bonus1
        # 斜向下方向
        bonus1 = sumdirection(x, y, table2, table1, tablequeue1, 1, 1)+bonus1
        # 斜向上方向
        bonus1 = sumdirection(x, y, table2, table1, tablequeue1, -1, 1)+bonus1
    for temp in table2:
        x = temp[0]
        y = temp[1]
        # 对对方棋盘的四个方向进行打分，打分后统计。
        # 列方向
        bonus2 = sumdirection(x, y, table1, table2, tablequeue2, 0, 1)+bonus2
        # 行方向
        bonus2 = sumdirection(x, y, table1, table2, tablequeue2, 1, 0)+bonus2
        # 斜向下方向
        bonus2 = sumdirection(x, y, table1, table2, tablequeue2, 1, 1)+bonus2
        # 斜向上方向
        bonus2 = sumdirection(x, y, table1, table2, tablequeue2, -1, 1)+bonus2

    # 通过改变参数改变棋风, 例如攻击性强的，攻击性弱的
    # bonus = bonus1 - bonus2*0.7
    bonus = bonus1 - bonus2 * 7.5
    return bonus


# 极大极小搜索加ab剪枝，nage是正负交替的极大极小搜索
def negamax(aiturn, depth, alpha, beta):
    # 游戏是否结束,探索的递归深度是否到边界
    if ui.game_win(database.AItotal) or ui.game_win(database.Playertotal) or depth == 0:
        return getgrade(aiturn)
    # 生成备选点
    temp_list = list(set(database.whole).difference(set(database.Alltotal)))
    # 搜索顺序排序  提高剪枝效率
    mysqort(temp_list)
    # 遍历每一个候选步
    for chess in temp_list:
        # 如果要评估的位置没有相邻的子， 则不去评估  减少计算
        if not nearby(chess):
            continue
        # 当前为ai回合，则尝试下一下，到下一层打分
        if aiturn:
            database.AItotal.append(chess)
        # 当前为player回合
        else:
            database.Playertotal.append(chess)
        database.Alltotal.append(chess)
        # 向下搜索，极大极小反向
        value = -negamax(not aiturn, depth - 1, -beta, -alpha)
        # 把尝试的子拿掉
        if aiturn:
            database.AItotal.remove(chess)
        # 把尝试的子拿掉
        else:
            database.Playertotal.remove(chess)
        # 把尝试的子拿掉
        database.Alltotal.remove(chess)
        # alpha beta剪枝
        if value > alpha:
            # 若到达搜索深度
            if depth == database.DEPTH:
                database.best_point[0] = chess[0]
                database.best_point[1] = chess[1]
            # 保存当前的alpha
            if value >= beta:
                return beta
            alpha = value
    return alpha


# 返回一个棋是否在已有棋的8连通域内
def nearby(search_loc):
    # 给定上下左右以及四个斜线的方法
    for i in range(-1, 2):
        for j in range(-1, 2):
            # 该点不予判断
            if i == 0 and j == 0:
                continue
            # 若有连通点，返回true
            if (search_loc[0] + i, search_loc[1]+j) in database.Alltotal:
                return True
    return False


# 分值计算某个方向
def sumdirection(x, y, table1, table2, tablequeue, down, right):
    for temp in tablequeue:
        for temp2 in temp[1]:
            if x == temp2[0] and y == temp2[1] and down == temp[2][0] and right == temp[2][1]:
                return 0
    #  加分项
    add_bonus = 0
    # 最大的得分项
    max_bonus = (0, None)
    # 在落子点 左右方向上循环查找得分形状
    for tt in range(-5, 1):
        # 该方向上的板子
        template = []
        # 某方向6斜格搜索，对方的子为2，我方为1，空为0，墙壁为-1，墙壁很重要
        for i in range(0, 6):
            if (x+(i+tt)*down, y+(i+tt)*right) in table1:
                template.append(2)
            elif (x+(i+tt)*down, y+(i+tt)*right) in table2:
                template.append(1)
            elif (x+(i+tt)*down, y+(i+tt)*right) in database.whole:
                template.append(0)
            else:
                template.append(-1)
        # 5长度模板
        templatefive = (template[0], template[1], template[2], template[3], template[4])
        # 6长度模板
        templatesix = (template[0], template[1], template[2], template[3], template[4], template[5])
        # 如果长度模板在数据库里，算分数
        for (grade, shape) in database.table:
            if templatefive == shape or templatesix == shape:
                # 保存当期那的最大分数
                if grade > max_bonus[0]:
                    max_bonus = (grade, ((x+(0+tt)*down, y+(0+tt)*right), (x+(1+tt)*down, y+(1+tt)*right), (x+(2+tt)*down, y+(2+tt)*right), (x+(3+tt)*down, y+(3+tt)*right), (x+(4+tt)*down, y+(4+tt)*right)), (down, right))
    if max_bonus[1] is not None:
        for temp5 in tablequeue:
            for temp3 in temp5[1]:
                for temp4 in max_bonus[1]:
                    if temp3 == temp4 and max_bonus[0] > 20 and temp5[0] > 20:
                        add_bonus += temp5[0] + max_bonus[0]
        tablequeue.append(max_bonus)
    return add_bonus + max_bonus[0]


# 对备选点进行排序，在剪枝的时候减小计算
def mysqort(temp_list):
    # 上一个棋的所在带你，-1为list最后一个数据。
    temp = database.Alltotal[-1]
    # 计算当前下的子后的8连通域
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                 continue
             # 把刚下的棋的周围位置移动到list最后方，在搜索上提前
            if (temp[0] + i, temp[1] + j) in temp_list:
                    # 把优先级较高的点从list中删除，再把优先级较高的点插入到第一个位置
                    temp_list.remove((temp[0] + i, temp[1] + j))
                    temp_list.insert(0, (temp[0] + i, temp[1] + j))