# That-sJustTheWazeItIs
The goal of our project is to create a concurrent network of cars driving on a map represented by a graph (vertices and edges).  The vertices on the graph represent each intersection/decision the car has to make and each edge is given a weight that is constantly changing.  The weight will be represented by a weight function that calculates the weight using the edge weight (distance / speed limit) and the number of cars currently on the road (traffic).  Each car represents their own concurrent thread and will be spawned with two arguments, their starting location and their destination (vertices).  Each thread will report the expected time of arrival at the destination calculated with an SSSP algorithm (probably Dijkstra’s algorithm).  This will be updated based on the current state of the map at each intersection, deciding the most optimal route to get to the destination as soon as possible (which will be affected by the movement of other cars).  Cars will only check for optimal path at each vertex as each car has to finish travelling on the road they are currently on before any change in decision can be made.  The main map will be represented by a “server” that communicates with the car threads.  A lock will have to be used to only allow one car to compute their optimal route and report the route they are currently taking to avoid race conditions.

## Dependencies
gtts

requests

numpy

python version must be >= 3.6



## Running example 
In one terminal window:

python server.py

In another terminal window(s):

python car.py A D http://localhost:8080
