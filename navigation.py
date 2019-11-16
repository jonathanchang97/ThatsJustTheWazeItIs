# Navigation module for ThatsJustTheWazeItIs

def dijkstra(graph, initial):
    visited = {initial: 0}
    path = {}

    nodes = set(graph.nodes)

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

        for edge in graph.edges[min_node]:
            # weight = current_weight + graph.distances[(min_node, edge)]
            weight = current_weight + getWeight(graph.edges[min_node][edge])
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge].append(min_node)

      return path
