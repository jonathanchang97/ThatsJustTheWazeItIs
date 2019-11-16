# transit flow module for ThatsJustTheWazeItIs

class Car:
    """Implements car functionality."""

    def __init__(self, arg):
        self.arg = args


class Graph:
    """Implements graph functionality."""

    def __init__(self, filename):
        parseFile(filename)
        self.nodes = set()
        self.edges = defaultdict(list)

    def parseFile(self, filename):
        pass

    def add_node(self, value):
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, distance):
        self.edges[from_node].append((to_node, distance, 0))
