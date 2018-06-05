#!/usr/local/bin python
# -*- coding:utf-8 -+-
import csv
import const
import pygame
import random
import math
import os
import glob
import sys
from pygame.locals import *

FOLDER_PASS = "/Users/takashi/Documents/knowledge/policy_files/"

SCR_RECT = Rect(0, 0, const.SCR_X, const.SCR_Y+const.Text_Y)   #Rect(left,top,width,height)
CS = const.CS
NUM_ROW = int(const.SCR_X / CS)   # フィールドの行数11
NUM_COL = int(const.SCR_Y / CS)  # フィールドの列数11

GLID = 49
EGENT = 1
ACTION = 5
START = 0
GOAL = 1
ROAD = 2
WALL = 3
ROBOT = 4
CS_COLOR = (255, 255, 255)
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3
STOP = 4
DIREC = [LEFT, RIGHT, UP, DOWN]


class main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCR_RECT.size)   #以下、self.名称はアトリビュートを追加
        self.screen.fill((255,255,255))
        self.font = pygame.font.SysFont("timesnewroman",42)
        self.folder_list = []
        self.folder_list = self.get_qtable_list()
        self.qtable_s = [[[0 for action in range(ACTION)]for y1 in range(const.S_NUM_COL + 1)] for x1 in range(const.S_NUM_ROW + 1)]  #source task
        self.qtable_reader(self.qtable_s,self.folder_list[0])
        self.draw(self.screen,self.qtable_s,os.path.basename(self.folder_list[0]))
        i = 0;
        while (1):
            pygame.time.Clock().tick(10000)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:  # 閉じるボタンが押されたら終了
                    pygame.quit()       # Pygameの終了(画面閉じられる)
                    sys.exit()
                elif event.type==KEYDOWN:   #キーを押したとき
                    if event.key==K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                    elif event.key==K_LEFT: #戻る
                        i = i - 1
                        if i < 0:
                            i = 0
                        self.qtable_reader(self.qtable_s,self.folder_list[i])
                        self.draw(self.screen,self.qtable_s,os.path.basename(self.folder_list[i]))

                    elif event.key==K_RIGHT: #進む
                        i = i + 1
                        if i > len(self.folder_list):
                            i = len(self.folder_list)
                        self.qtable_reader(self.qtable_s,self.folder_list[i])
                        self.draw(self.screen,self.qtable_s,os.path.basename(self.folder_list[i]))

    def qtable_reader(self, qtable_ss,name):
        self.qtable = []
        o = open(name, 'r')
        dataReader = csv.reader(o)
        for row in dataReader:
            # q値を配列qtableに書き込み
            self.qtable.append(float(row[3]))
        self.count_qtable = 0
        for x in range(1, const.S_NUM_ROW+1):
            for y in range(1, const.S_NUM_COL+1):
                for action in range(ACTION):
                    # self.qtable_c[x][y][action] = const.TRANCE_RATE*self.qtable[self.count_qtable]
                    # q値と状態、行動の対応を作成
                    qtable_ss[x][y][action] = self.qtable[self.count_qtable]
                    self.count_qtable = self.count_qtable + 1

    def draw(self, screen, qtable_ss,name):
         self.screen.fill((255,255,255))
         sysfont = pygame.font.SysFont(None, 30)
         for x in range(1, const.S_NUM_ROW+1):
            for y in range(1, const.S_NUM_COL+1):
                pygame.draw.rect(screen,CS_COLOR,Rect(x*CS,y*CS,CS,CS))
                if self.get_max_q_action_return_q(qtable_ss,x,y) != 0:   #色を濃くしていく部分（元のサンプルコード）
                    val = self.get_max_q_action_return_q(qtable_ss,x,y)
                    if val > 1:
                         val = 1
                    val *= 255.0   #複合演算子
                    color = (255,255-val,255-val)
                    pygame.draw.rect(screen,color,Rect(x*CS,y*CS,CS,CS))
                    num = self.get_max_q_action(qtable_ss,x,y)
                    direction = u""
                    if num==UP:
                        direction = u"↑"
                    elif num==DOWN:
                        direction = u"↓"
                    elif num==LEFT:
                        direction = u"←"
                    else:
                        direction = u"→"

                    if self.get_max_q_action_return_q(qtable_ss,x,y) > 0 and self.get_max_q_prob(qtable_ss,x,y) >= 0.9:
                        screen.blit(self.font.render(direction, True, (0,0,0)), (x*CS,y*CS))

                pygame.draw.rect(screen,(50,50,50),Rect(x*CS,y*CS,CS,CS),1)
                step = sysfont.render('step='+'%d' %const.Step_Agent1, False, (0,0,0))
                episode=sysfont.render('episode='+'%d' %const.EPISODE_Agent1, False, (0,0,0))
                filename = sysfont.render('file_name='+'%s' %name, False, (0,0,0))
                self.screen.blit(step, (20,const.SCR_Y+35))
                self.screen.blit(episode, (20,const.SCR_Y+70))
                self.screen.blit(filename, (20,const.SCR_Y+105))

    def get_max_q_action(self,qtable,x1,y1):
        m = 0.0
        action = 0
        for i in range(const.Action_no):
            if float(qtable[x1][y1][i]) >= float(m):
                m = qtable[x1][y1][i]
                action = i
        if qtable[x1][y1][0] == 0.00 and qtable[x1][y1][1] == 0.00 and qtable[x1][y1][2] == 0.00 and qtable[x1][y1][3] == 0.00 and qtable[x1][y1][4] == 0.00:   #�e�s����Q�l��0�̏ꍇ
            i = random.randint(0,4)
        return action

    def get_max_q_action_return_q(self,qtable,x1,y1):
        m = 0.0
        for i in range(const.Action_no):
            if float(qtable[x1][y1][i]) >= float(m):
                m = qtable[x1][y1][i]
        if qtable[x1][y1][0] == 0.00 and qtable[x1][y1][1] == 0.00 and qtable[x1][y1][2] == 0.00 and qtable[x1][y1][3] == 0.00 and qtable[x1][y1][4] == 0.00:
            return 0
        return m

    def get_max_q_prob(self,qtable,x1,y1):
        choosen = 0                  #ボルツマンによって選択された行動
        denom = 0                    #ボルツマンの分母
        prob = [0 for i in range(const.Action_no)] #それぞれの行動に対する確率
        posible_action = []
        max_prob = 0

        for act in range(const.Action_no):
            posible_action.append([act,qtable[x1][y1][act]])

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

    def get_qtable_list(self):
        self.fl = glob.glob(FOLDER_PASS+"*")
        return self.fl

if __name__ == '__main__':
    main()
