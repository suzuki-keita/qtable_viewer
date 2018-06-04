#!/usr/local/bin python
# -*- coding:utf-8 -+-
import csv
import const
import pygame
from pygame.locals import *

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
        self.qtable_s = [[[0 for action in range(ACTION)]for y1 in range(const.S_NUM_COL + 1)] for x1 in range(const.S_NUM_ROW + 1)]  #source task
        self.qtable_reader(self.qtable_s)


    def qtable_reader(self, qtable_ss):
        self.qtable = []
        o = open('q_table(source).csv', 'r')
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

    def draw(self, screen):
         sysfont = pygame.font.SysFont(None, 30)
         for y in range(NUM_COL):
            for x in range(NUM_ROW):
                if self.field[y][x].k == WALL:   #障害物
                    pygame.draw.rect(screen,(0,0,0),Rect(x*CS,y*CS,CS,CS))   #0,0,0=黒

                if self.field[y][x].k == START:   #スタート
                    pygame.draw.rect(screen,CS_COLOR,Rect(x*CS,y*CS,CS,CS))
                    direction = u"S"
                    screen.blit(self.font.render(direction, True, (0,0,0)), (x*CS+10,y*CS))


                if self.field[y][x].k == GOAL:   #ゴール
                    pygame.draw.rect(screen,CS_COLOR,Rect(x*CS,y*CS,CS,CS))
                    direction = u"G"
                    screen.blit(self.font.render(direction, True, (0,0,0)), (x*CS+5,y*CS))
                    #pygame.draw.rect(screen,(100,255,255),Rect(x*CS,y*CS,CS,CS))

                if self.field[y][x].k == ROAD:
                    pygame.draw.rect(screen,CS_COLOR,Rect(x*CS,y*CS,CS,CS))
                    if self.state_agent[y][x].get_max_q_action_return_q(self.qtable_c,x,y) != 0:   #色を濃くしていく部分（元のサンプルコード）
                        val = self.state_agent[y][x].get_max_q_action_return_q(self.qtable_c,x,y)
                        if val > 1:
                             val = 1
                        val *= 255.0   #複合演算子
                        color = (255,255-val,255-val)
                        pygame.draw.rect(screen,color,Rect(x*CS,y*CS,CS,CS))
                        num = self.state_agent[y][x].get_max_q_action(self.qtable_c,x,y).d
                        direction = u""
                        if num==UP:
                            direction = u"↑"
                        elif num==DOWN:
                            direction = u"↓"
                        elif num==LEFT:
                            direction = u"←"
                        else:
                            direction = u"→"
                            
                        if self.state_agent[y][x].get_max_q_action_return_q(self.qtable_c,x,y) > 0 and self.state_agent[y][x].get_max_q_prob(self.qtable_c,x,y,self.state_agent_now_prob) >= 0.9:
                            screen.blit(self.font.render(direction, True, (0,0,0)), (x*CS,y*CS))

                if y == self.agent.y and x == self.agent.x:   #常に表示
                    pygame.draw.rect(screen,(0,0,255),Rect(x*CS,y*CS,CS,CS))

                pygame.draw.rect(screen,(50,50,50),Rect(x*CS,y*CS,CS,CS),1)
                step = sysfont.render('step='+'%d' %const.Step_Agent1, False, (0,0,0))
                white_step = sysfont.render('         '+'%d' %const.Step_f_Agent1, False, (255,255,255))
                episode=sysfont.render('episode='+'%d' %const.EPISODE_Agent1, False, (0,0,0))
                white_episode = sysfont.render('               '+'%d' %const.EPISODE_Agent1, False, (255,255,255))
                self.screen.blit(white_step, (20,const.SCR_Y+35))
                self.screen.blit(step, (20,const.SCR_Y+35))
                self.screen.blit(white_episode, (20,const.SCR_Y+70))
                self.screen.blit(episode, (20,const.SCR_Y+70))

if __name__ == '__main__':
    main()
