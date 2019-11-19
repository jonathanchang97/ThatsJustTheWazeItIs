from transitFlow import *
from navigation import *

g = Graph("example.txt")
# for from_edge in g.edges:
#     print(from_edge + ": ")
#     for to_edge in g.edges[from_edge]:
#         print("\t" + to_edge + " " + g.edges[from_edge][to_edge].road_name + " " + str(g.edges[from_edge][to_edge].distance))

print(dijkstra(g, 'B', 'E'))
