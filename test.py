from map import *
from navigation import *

g = Navigation("example.txt")
print(g.dijkstra('D', 'E'))
