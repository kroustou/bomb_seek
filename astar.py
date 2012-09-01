from utils import neighbours

class Node:
    def __init__(self, position, end, parent=None):
        self.position = position
        self.parent = parent
        self.x = position[0]
        self.y = position[1]
        self.end = end
        if not parent:
            self.g = 0
        else:
            self.g = parent.g + 1
        self.h = abs(self.x - self.end[0]) + (self.y - self.end[1])
        self.f = self.g + self.h


class AStar():
    def __init__(self):
        print 'astar init'
        self.open_list = []
        self.closed_list = []

    def find_path(self, start, end, known_region):
        print 'finding path'
        current = Node(start, end)
        self.open_list.append(current)
        self.map = known_region
        
        while self.open_list:
            #find the neighbours of the last item in list 
            self.open_list += self.neighbours(current, end)
            self.open_list.remove(current)
            self.closed_list.append(current)

            shortest_f = self.open_list[0]
            for node in self.open_list:
                if node.f < shortest_f.f:
                    shortest_f = node
            current = shortest_f
            if current.position in neighbours(end):
                print 'target found:', end
                break

        path_nodes = [current]
        while path_nodes[-1].position != start:
            path_nodes.append(path_nodes[-1].parent)
        path = []
        for node in path_nodes:
            path.append(node.position)
        print 'path found:', path
        return path

    def neighbours(self, node, end):
        candidates = []
        (x,y) = node.position
        neighbours = [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
        for n in neighbours:
            if n in self.map:
                candidate = Node(n, end, node)
                put = True
                for i in self.closed_list:
                    if i.position == candidate.position:
                        put = False 
                        break
                for i in self.open_list:
                    if i.position == candidate.position:
                        put = False 
                        break
                if put:
                    candidates.append(candidate)
        return candidates



