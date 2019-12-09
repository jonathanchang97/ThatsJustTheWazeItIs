#
#   navigation.py
# 
#       Contains an implementation of Dijkstra’s algorithm using our
#       weight system that accounts for the length of the road and the
#       number of cars on the road, as well as a function to update a
#       member graph object whenever a car reaches an intersection and
#       return the updated shortest path.
#

from collections import defaultdict
import json
import threading
from map import Graph
import copy


class Lightswitch:
    def __init__(self):
        self.__counter = 0
        self.__mutex = threading.Lock()

    def lock(self, semaphore):
        self.__mutex.acquire()
        self.__counter += 1
        if self.__counter == 1:
            semaphore.acquire()
        self.__mutex.release()

    def unlock(self, semaphore):
        self.__mutex.acquire()
        self.__counter -= 1
        if self.__counter == 0:
            semaphore.release()
        self.__mutex.release()


class Navigation:
    """ module define car navigation requests related to the map.  This includes
        reads and writes to the map"""

    def __init__(self, filename):
        self.graph = Graph(filename)
        self.__roomEmpty = threading.Lock()
        self.__turnstile = threading.Lock()
        self.__readSwitch = Lightswitch()

    # processes a car's request whenever it reaches an intersection
    def requestMapUpdate(self, body):
        self.__turnstile.acquire()
        self.__turnstile.release()

        self.__readSwitch.lock(self.__roomEmpty)
        path, wait, total_wait = self.dijkstra(body["curr"], body["dest"])
        self.__readSwitch.unlock(self.__roomEmpty)

        if not path:
            return json.dumps({"status" : -1})

        self.__turnstile.acquire()
        self.__roomEmpty.acquire()
        if len(path) == 1:
            self.updateMap(body["prev"], path[0], "")
        else:
            self.updateMap(body["prev"], path[0], path[1])
        self.__turnstile.release()
        self.__roomEmpty.release()

        if len(path) == 1:
            return json.dumps({"status" : 1})
        else:
            road = self.graph.edges[path[0]][path[1]].road_name
            return json.dumps({"status" : 0, "next" : path[1], "road" : road,
                               "wait" : wait, "total_wait" : total_wait})

    # calculates the SSSP from. the current node to the destination
    def dijkstra(self, curr, dest):
        if curr == dest:
            return [curr], 0, 0

        visited = {curr: 0}
        path = {curr: [curr]}

        nodes = copy.deepcopy(self.graph.nodes)

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

            for to_node in self.graph.edges[min_node]:
                weight = current_weight + \
                         self.graph.getWeight(min_node, to_node)
                if to_node not in visited or weight < visited[to_node]:
                    visited[to_node] = weight
                    path[to_node] = path[min_node] + [to_node]

        if dest in path:
            return path[dest], visited[path[dest][1]], visited[dest]
        else:
            return [], 0, 0

    # update the map when a car moves onto a new road
    def updateMap(self, prev, curr, next):
        if prev:
            self.graph.edges[prev][curr].num_cars -= 1
        if next:
            self.graph.edges[curr][next].num_cars += 1
