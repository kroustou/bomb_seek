#!/usr/bin/env python
from PySide.QtCore import *
from PySide.QtGui import *
import sys

from agent import Agent
    
class Maze(QWidget):
    def __init__(self, width, height, custom_map):
        QWidget.__init__(self)
        self.map = custom_map
        self.setMazeSize(width, height, boxsize = 20)
        self.generateMaze()
        self.bomb_found = False
        self.initial = True
        self.stop_parent = False
 
    def setMazeSize(self, width, height, boxsize):
        self.maze_width = width
        self.maze_height = height
        self.boxsize = boxsize
        self.setFixedSize(width * boxsize + 10, height * boxsize + 10)
 
    def generateMaze(self, width=None, height=None, sparseness=None):
        if width is None: width = self.maze_width
        if height is None: height = self.maze_height

    def is_wall(self, x, y):
        # print self.wall
        return (x,y) in self.wall

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.fillRect(0, 0, self.maze_width * self.boxsize + 10, self.maze_height * self.boxsize + 10, Qt.white)
 
        qp.translate(QPoint(5.5, 5.5))
        qp.setPen(Qt.black)
        b = self.boxsize
 
        if self.initial:
            # Position of walls, agents and scout
            self.agents = []
            self.wall = []
            for (y,row) in enumerate(self.map):
                for (x, coll) in enumerate(row):
                    if coll == '*':
                        qp.fillRect(x*b, y*b, b, b, Qt.black)
                        self.wall.append((x,y))
                    if coll == 'B':
                        self.target = (x,y)
                    try:
                        a_coll = int(coll)
                    except ValueError :
                        pass
                    else:
                        if a_coll in range(0,10):
                            self.agents.append(Agent((x,y),qp,self))
                    if coll == 'A':
                        self.scout = Agent((x,y),qp,self,True)
                        self.agents.append(self.scout)
            self.initial = False
        else:
            for w in self.wall:
                qp.fillRect(w[0]*self.boxsize, w[1] *self.boxsize, self.boxsize, self.boxsize, Qt.black)

        for a in self.agents:
            qp.fillRect(a.x*self.boxsize, a.y*self.boxsize, self.boxsize, self.boxsize, a.color)
            if a.draw_path:
                for p in a.path:
                    try:
                        qp.fillRect(p[0]*self.boxsize, p[1] *self.boxsize, self.boxsize, self.boxsize, QColor(0, 0, 255, 127))
                    except:
                        print 'couldn draw path'
        # target
        x, y = self.target
        qp.fillRect(x*b, y*b, b, b, Qt.red)
 
        # status
        if self.bomb_found:
            stats = ''
            counter = 0
            for a in self.agents:
                stats += '%s - moves: %s , exchanges: %s \n' %(counter if not a.is_scout else 'scout', a.step_num, a.exchanges)
                counter += 1
            stats += 'Overal time: %s sec\n' % ((a.step_num * 500) / 1000)
            stats += 'Step time 500ms \n'
            qp.setPen(Qt.blue)
            qp.setFont(QFont("sans", 22, QFont.Normal))
            qp.drawText(QRect(0, 0, self.maze_width * b, self.maze_height * b),
                Qt.AlignCenter | Qt.AlignVCenter,
                'bomb found!!!')
            f = open('stats.txt','w')
            f.write(stats)
            f.close()
            self.stop_parent = True
 
        qp.end()

    def init(self):
        self.maze = [[0 for x in range(0, self.maze_width)] for y in range(0, self.maze_height)]
        self.step_num = 1
        self.maze[y][x] = 1
        self.status = False