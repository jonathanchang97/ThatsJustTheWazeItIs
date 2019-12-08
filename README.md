# ThatsJustTheWazeItIs
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

## File Descriptions
* car.py:
	Implements the car class, or the client, which asks the server for
	directions until it reaches its destination. A car waits a specified
	time until it reaches an intersection, then makes a request containing
	its current location and its destination to the server. The server
	responds with the correct turn and how long it will take for the car
	to reach the next intersection. The car prints out the direction and
	waits that amount of time before making another request.

* map.py:
	Implements the graph and edge classes, the first of which parses a
	supplied text file and represents it as a directed graph, with a
	method to compute the weight of an edge as a function of its capacity
	and length. The edge class holds each edge’s name, weight, and current
	capacity.

* server.py:
	Makes use of the BaseHTTPRequestHandler class from the http.server
	library to handle the post requests from the cars. A car process
	wakes from sleep and requests to update the map and get its next
	move. The server then communicates with the map module and responds
	with a new street, direction and wait time.

* navigation.py:
	Contains an implementation of Dijkstra’s algorithm using our
	weight system that accounts for the length of the road and the
	number of cars on the road, as well as a function to update a
	member graph object whenever a car reaches an intersection and
	return the updated shortest path.

* myQueue.py:
	Contains Mark Sheldon's implementation of SynchronizedQueue from Mark’s
	solutions to the word histogram assignment.


* install_dependencies.sh:
	Script to install dependencies
