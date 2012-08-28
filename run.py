#!/usr/bin/env python
from PySide.QtCore import *
from PySide.QtGui import *
import sys

from maze import Maze

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Bomb Seekerz")
        self.init_maze()

    def init_maze(self):
    #  custom map is a list containing each row
    #  and the width is the length of the first row
        custom_map = []
        f = open('map.txt', 'r')
        for line in f.readlines():
            custom_map.append(line)
        f.close()
        width = len(custom_map[0]) 
        height  = len(custom_map)

        self.maze = Maze(width, height, custom_map)
 
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 10, 0)
        hbox.addWidget(self.maze)
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 10, 0, 0)
        hbox.addLayout(vbox)
 
        self.agents = QLineEdit("s")
        vbox.addWidget(QLabel("agent to watch:"))
        vbox.addWidget(self.agents)

        self.btn_watch = QPushButton("Watch Agent")
        self.btn_watch.clicked.connect(self.watchAgent)
        vbox.addWidget(self.btn_watch)

        self.btn_remove = QPushButton("Remove path")
        self.btn_remove.clicked.connect(self.remove)
        vbox.addWidget(self.btn_remove)        
 
        self.btn_solve = QPushButton("Start")
        self.btn_solve.clicked.connect(self.startSolving)
        vbox.addWidget(self.btn_solve)
 
        self.btn_step = QPushButton("Next Step")  
        self.btn_step.clicked.connect(self.doStep)
        vbox.addWidget(self.btn_step)
        
        self.btn_stop = QPushButton("Stop")
        self.btn_stop.setEnabled(False)
        self.btn_stop.clicked.connect(self.stopSolving)
        vbox.addWidget(self.btn_stop)
        
        self.btn_restart = QPushButton("Restart")
        self.btn_restart.setEnabled(True)
        self.btn_restart.clicked.connect(self.restart)
        vbox.addWidget(self.btn_restart)

        vbox.addStretch()
 
        proxy_widget = QWidget()
        proxy_widget.setLayout(hbox)
        self.setCentralWidget(proxy_widget)
 
        self.maze.init()

    def watchAgent(self):
        if self.agents.displayText() == 's':
            for a in self.maze.agents:
                if a.is_scout:
                    agent = a
                    break
        else:
            try:
                agent = self.maze.agents[int(self.agents.displayText())-1]
            except:
                return True       
            for a in self.maze.agents:
                if a.draw_path:
                    a.draw_path = False        
        agent.draw_path = True

    def remove(self):
        for a in self.maze.agents:
            if a.draw_path:
                a.draw_path = False


    def restart(self):
        self.Maze = None
        self.init_maze()

    def doStep(self):
        if self.maze.stop_parent:
            self.stopSolving()
        self.maze.step_num += 1
        for a in self.maze.agents:
            a.move()
        self.maze.repaint()
 
    def startSolving(self):
        self.btn_solve.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.btn_step.setEnabled(True)
        self.maze.init()
 
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.doStep)
        self.timer.setInterval(500)
        self.timer.start()
 
    def stopSolving(self):
        self.btn_stop.setEnabled(False)
        self.btn_solve.setEnabled(True)
        self.btn_step.setEnabled(True)
        self.timer.stop()
  
 
app = QApplication(sys.argv)
 
mw = MainWindow()
mw.show()
 
sys.exit(app.exec_())