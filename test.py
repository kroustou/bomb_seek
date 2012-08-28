from agent import PathToBomb

map = [(0, 5), (0, 6), (0, 7), (1, 7), (1, 6), (1, 5), (1, 4), (1, 3), (0, 4), (0, 3), (6, 2), (6, 1), (5, 2), (5, 1), (4, 1), (3, 0), (3, 1), (3, 2), (2, 2), (1, 2), (1, 3)]
target = (5, 0)
location = (0, 3)
a = PathToBomb()
b = a.run(map, location, target)
print b