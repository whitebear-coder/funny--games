'''
该文件为ai算法上的优化
author: white_mai
email: 18341491429@163.com
'''
import ai
import database


# 胜利判断
def victory_judge(AIturn):
    if AIturn:
        table1 = database.AItotal
        table2 = database.Playertotal
        for temp in table1:
            x = temp[0]
            y = temp[1]
            # 四个方向进行计算
            if ai.summodel(x, y, 0, 1, table2, table1, database.victory):
                return True
            elif ai.summodel(x, y, 1, 0, table2, table1, database.victory):
                return True
            elif ai.summodel(x, y, 1, 1, table2, table1, database.victory):
                return True
            elif ai.summodel(x, y, -1, 1, table2, table1, database.victory):
                return True
    return False


# 进攻判断
def attack_judge(AIturn):
    if AIturn:
        table1 = database.AItotal
        table2 = database.Playertotal
        for temp in table1:
            x = temp[0]
            y = temp[1]
            # 八个方向选四个方向进行计算
            if ai.summodel(x, y, 0, 1, table2, table1, database.attack):
                return True
            elif ai.summodel(x, y, 1, 0, table2, table1, database.attack):
                return True
            elif ai.summodel(x, y, 1, 1, table2, table1, database.attack):
                return True
            elif ai.summodel(x, y, -1, 1, table2, table1, database.attack):
                return True
    return False


# 防御判断
def defense_judge(AIturn):
    if AIturn:
        table1 = database.AItotal
        table2 = database.Playertotal
        for temp in table2:
            x = temp[0]
            y = temp[1]
            # 四个方向进行计算
            if ai.summodel(x, y, 0, 1, table2, table1, database.defense):
                return True
            elif ai.summodel(x, y, 1, 0, table2, table1, database.defense):
                return True
            elif ai.summodel(x, y, 1, 1, table2, table1, database.defense):
                return True
            elif ai.summodel(x, y, -1, 1, table2, table1, database.defense):
                return True
    return False



