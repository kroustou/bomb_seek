from PySide.QtGui import *
import random

from astar import AStar
from utils import neighbours


class Agent():
    def __init__(self, position, qp, parent, is_scout=False):
        (self.x, self.y) = position
        self.step_num = 1
        self.path = [position]
        self.is_scout = is_scout
        self.parent = parent
        self.color = QColor(0, 96, 109, 255) if self.is_scout  else QColor(0, 168, 109, 255)
        self.draw_path = False
        self.bomb_location = False
        self.path_to_bomb = []  
        self.exchanges = 0

    def move(self):
        self.step_num += 1
        # if bomb in the neigbourhood
        if self.parent.target in neighbours((self.x, self.y), True):
            # The agent found the bomb
            self.bomb_location = self.parent.target
            if self.is_scout:
                # bomb deactivated
                self.parent.bomb_found = True
                return True
            else:
                self.color = QColor(200, 96, 109, 255)
                # the path is being reinitialized in
                # order to be show to the scout
                self.bomb_location = self.parent.target

        # if agent is scout and scout knows the bomb
        if self.bomb_location and self.is_scout:
            if self.path_to_bomb:
                (self.x, self.y) = self.path_to_bomb.pop()
                return True
            # create a shortcut
            target = self.bomb_location
            known_region = self.path
            start = (self.x, self.y)
            print 'calling astar'
            shortest_path = AStar()
            print 'will find the shortest path'
            self.path_to_bomb = shortest_path.find_path(start, target, known_region)
            return True

        # select to move randomly avoiding
        # to go to the last position
        order_list = ['u', 'r', 'd', 'l']
        random.shuffle(order_list)

        # get the available moves
        moves = []
        for order in order_list:
            if order == 'u':
                moves = self.up(moves)
            elif order == 'r':
                moves = self.right(moves)
            elif order == 'd':
                moves = self.down(moves)
            elif order == 'l':
                moves = self.left(moves)

        # if moves available
        if len(moves) != 0:
            # check if agents meet each other
            for agent in self.parent.agents:
                if (agent.x, agent.y) in neighbours((self.x, self.y)):
                    self.exchanges += 1
                    agent.path += self.path
                    self.path += agent.path
                    self.path = list(set(self.path))
                    agent.path = list(set(agent.path))
                    if (agent.is_scout) and (self.bomb_location) and (not agent.bomb_location):
                        agent.bomb_location = self.bomb_location
                        return True
                    else:
                        if self.bomb_location and not agent.bomb_location:
                            
                            agent.bomb_location = self.bomb_location
                            agent.color = QColor(200, 96, 109, 255)

            for m in moves:
                # The agent prefers to go to a
                # square he has not visited
                if m in self.path:
                    #we put this move at the end
                    moves.remove(m)
                    moves.append(m)
            (self.x, self.y) = moves[0]
            if moves[0] in self.path:
                self.path.remove((self.x, self.y))
            self.path.append((self.x, self.y))
        else:
            print 'cannot move'
            return False
        return True

    def up(self, moves):
        # try step up
        if self.y > 0 and not self.parent.is_wall(self.x, self.y - 1):
            moves.append((self.x, self.y - 1))
        return moves

    def right(self, moves):
        # try step right
        if self.x < self.parent.maze_width - 1 and not self.parent.is_wall(self.x + 1, self.y):
            moves.append((self.x + 1, self.y))
        return moves

    def down(self, moves):
        # try step down
        if self.y < self.parent.maze_height - 1 and not self.parent.is_wall(self.x, self.y + 1):
            moves.append((self.x, self.y + 1))
        return moves

    def left(self, moves):
        # try step left
        if self.x > 0 and not self.parent.is_wall(self.x - 1, self.y):
            moves.append((self.x - 1, self.y))
        return moves
