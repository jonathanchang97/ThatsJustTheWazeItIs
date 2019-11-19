# Navigation module for ThatsJustTheWazeItIs
from collections import defaultdict

def dijkstra(graph, initial, final):
    visited = {initial: 0}
    path = {}

    nodes = graph.nodes

    while nodes:
        min_node = None
        for node in nodes:
          if node in visited:
            if min_node is None:
              min_node = node
            elif visited[node] < visited[min_node]:
              min_node = node

        if min_node is None:
          break

        nodes.remove(min_node)
        current_weight = visited[min_node]

        for to_node in graph.edges[min_node]:
            weight = current_weight + graph.getWeight(min_node, to_node)
            if to_node not in visited or weight < visited[to_node]:
                visited[to_node] = weight
                if to_node in path:
                    path[to_node].append(min_node)
                else:
                    path[to_node] = [min_node]

    return visited[to_node]
