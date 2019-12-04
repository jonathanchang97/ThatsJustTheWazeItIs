# transit flow module for ThatsJustTheWazeItIs
from collections import defaultdict
import numpy as np
import pandas as pd


class Edge:
    """docstring for Edge."""

    def __init__(self, road_name, distance):
        self.road_name = road_name
        self.distance = distance
        self.num_cars = 0

class Graph:
    """Implements graph functionality."""

    def __init__(self, filename):
        self.nodes = set()
        self.edges = defaultdict(defaultdict)
        map_data = self.parseFile(filename)
        self.addMapData(map_data)

    def parseFile(self, filename):
        # Load data
        return np.loadtxt(filename, dtype='str', skiprows=1, delimiter=',')

    def addMapData(self, map_data):
        for road in map_data:
            self.nodes.add(road[0])
            self.nodes.add(road[1])
            self.edges[road[0]][road[1]] = Edge(road[2], float(road[3]))

    def getWeight(self, from_node, to_node):
        road = self.edges[from_node][to_node]
        return road.distance * (1 + road.num_cars / (road.num_cars + road.distance))
