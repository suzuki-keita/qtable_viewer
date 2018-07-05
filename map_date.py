#!/usr/local/bin python
# -*- coding:utf-8 -+-
import main
import const
import random
import math

class map_date:
    def __init__(self):
        """
        mapping_table[x][y][action][direction]

        [direction] (x,y)が4の位置にあるときの周りのマップデータを示す。
        ０│１│２　
        ー＋ー＋ー
        ３│４│５
        ー＋ー＋ー
        ６│７│８
        """
        self.mapping_table = [[[[-1 for map in range(main.MAP)] for action in range(main.ACTION)]for y1 in range(const.S_NUM_COL + 1)] for x1 in range(const.S_NUM_ROW + 1)]
        self.qtable = [[[0 for action in range(main.ACTION)]for y1 in range(const.S_NUM_COL + 1)] for x1 in range(const.S_NUM_ROW + 1)]  #qtable
        self.start_grid = [-1,-1]
        self.goal_grid = [-1,-1]
        self.route_x = []
        self.route_y = []

    def follow_route(self):
        #Q値情報を元にゴールまでのルートを作成する
        self.route_x = []
        self.route_y = []
        self.q = 0
        self.grid_x = self.start_grid[0]
        self.grid_y = self.start_grid[1]
        self.max = 0
        self.next_grid_x = 0
        self.next_grid_y = 0
        self.tmp = 0
        self.goals_x = [self.goal_grid[0],self.goal_grid[0]-1,self.goal_grid[0]+1,self.goal_grid[0]]
        self.goals_y = [self.goal_grid[1]-1,self.goal_grid[1],self.goal_grid[1],self.goal_grid[1]+1]

        while(1):
            self.break_flag = False
            for j in range(4):
                if self.grid_x == self.goals_x[j] and self.grid_y == self.goals_y[j]:
                    self.break_flag = True
            for self.num in [1,3,5,7]:
                self.tmp = self.get_direction_return_q(self.num,self.qtable,self.grid_x,self.grid_y)
                if self.tmp[0] > self.max:
                    self.max = self.tmp[0]
                    self.next_grid_x = self.tmp[1]
                    self.next_grid_y = self.tmp[2]
            #ルートに追加
            self.route_x.append(self.grid_x)
            self.route_y.append(self.grid_y)
            self.grid_x = self.next_grid_x
            self.grid_y = self.next_grid_y

            if self.break_flag == True:
                break

        return 1

    def get_direction_return_q(self,number,_qtable,_x,_y):
        #number_to_direction
        _x = int(_x)
        _y = int(_y)
        #エージェントの上下左右のみ検出
        if number == 1:
            _x = _x
            _y = _y - 1
        elif number == 3:
            _x = _x - 1
            _y = _y
        elif number == 5:
            _x = _x + 1
            _y = _y
        elif number == 7:
            _x = _x
            _y = _y + 1

        #データ整形
        if _x > const.S_NUM_ROW:
            _x = const.S_NUM_ROW
        if _x < 0:
            _x = 0
        if _y > const.S_NUM_COL:
            _y = const.S_NUM_COL
        if _y < 0:
            _y = 0

        return self.get_max_q_action_return_q(_qtable,_x,_y),_x,_y

    def get_infomation(self):
        #各種情報を取得

        #経路長
        self.route_length = len(self.route_x)
        self.route_rotation = 0
        self.route_possibility = 0
        for i in range(self.route_length-1):
            #回転数
            #篠田のアドバイスで解決ゾロリ
            if self.get_max_q_action(self.qtable,self.route_x[i],self.route_y[i]) != self.get_max_q_action(self.qtable,self.route_x[i+1],self.route_y[i+1]):
                self.route_rotation = self.route_rotation + 1
            #エージェントが取り得る他の路
            for j in [1,3,5,7]:
                if self.mapping_table[self.route_x[i]][self.route_y[i]][0][j] == 2:
                    self.route_possibility = self.route_possibility + 1

        return self.route_length,self.route_rotation,self.route_possibility

    def get_max_q_action(self,_qtable,_x,_y):
        m = 0.0
        action = 0
        for i in range(const.Action_no):
            if float(_qtable[_x][_y][i]) >= float(m):
                m = _qtable[_x][_y][i]
                action = i
        if _qtable[_x][_y][0] == 0.00 and _qtable[_x][_y][1] == 0.00 and _qtable[_x][_y][2] == 0.00 and _qtable[_x][_y][3] == 0.00 and _qtable[_x][_y][4] == 0.00:   #�e�s����Q�l��0�̏ꍇ
            i = random.randint(0,4)
        return action

    def get_max_q_action_return_q(self,_qtable,_x,_y):
        m = 0.0
        for i in range(const.Action_no):
            if float(_qtable[_x][_y][i]) >= float(m):
                m = _qtable[_x][_y][i]
        if _qtable[_x][_y][0] == 0.00 and _qtable[_x][_y][1] == 0.00 and _qtable[_x][_y][2] == 0.00 and _qtable[_x][_y][3] == 0.00 and _qtable[_x][_y][4] == 0.00:
            return 0
        return m

    def get_max_q_prob(self,_qtable,_x,_y):
        choosen = 0                  #ボルツマンによって選択された行動
        denom = 0                    #ボルツマンの分母
        prob = [0 for i in range(const.Action_no)] #それぞれの行動に対する確率
        posible_action = []
        max_prob = 0

        for act in range(const.Action_no):
            posible_action.append([act,_qtable[_x][_y][act]])

        for act in range(len(posible_action)):
            no = posible_action[act]
            tmp = no[1] / const.T
            denom = math.exp(tmp) + denom

        for act in range(len(posible_action)):
            no = posible_action[act]
            tmp = no[1] / const.T
            prob[act] =  math.exp(tmp) / denom
            if max_prob < prob[act]:
                max_prob = prob[act]

        return max_prob
