from acocolony import ACOColony
from aconode import ACONode
from acoconstants import NUM_NODES, MIN_DIST, MAX_DIST, MAX_NEIGHBOURS, NUM_DRONES

import random

def build_graph():
	nodes = {id_: ACONode(id_, False) for id_ in range(1, NUM_NODES + 1)}
	for node in nodes.values():
		num_neighbours = random.randint(1, MAX_NEIGHBOURS)
		for _ in range(num_neighbours):
			id_ = random.randint(1, NUM_NODES)
			if id_ == node.id:
				continue
			neighbour = nodes[id_]
			node.neighbours[id_] = neighbour
			neighbour.neighbours[node.id] = node
			node.pheromones[id_] = 0.0
			neighbour.pheromones[node.id] = 0.0
			distance = random.random() + random.randint(MIN_DIST, MAX_DIST - 1)
			node.distances[id_] = distance
			neighbour.distances[node.id] = distance
	return nodes

def strip_path_from_graph(graph, path):
	for i in range(len(path) - 1):
		n = path[i].id
		next_ = path[i + 1].id
		del graph[n].neighbours[next_]
		del graph[n].distances[next_]
		del graph[n].pheromones[next_]
		del graph[next_].neighbours[n]
		del graph[next_].distances[n]
		del graph[next_].pheromones[n]

def reset_graph(graph):
	for node in graph.values():
		for id_ in node.pheromones:
			node.pheromones[id_] = 0.0
		node._goal = False

if __name__ == '__main__':
	graph = build_graph()
	for drone in range(NUM_DRONES):
		print('Finding path for drone {}'.format(drone))
		goal = random.randint(1, NUM_NODES)
		graph[goal]._goal = True
		print('Goal for drone {} is {}'.format(drone, goal))

		colony = ACOColony(graph, 0)
		colony.search()
		print('Best Path:')
		route = colony.best_path
		dist_so_far = 0.0
		for i in range(len(route) - 1):
			n = route[i]
			print('Node: {}'.format(n.id))
			print('Distance so far: {}'.format(dist_so_far))
			print('Distance to next node: {}'.format(n.cost_to(route[i+1].id)))
			dist_so_far += n.cost_to(route[i+1].id)
		print('Best Cost: {}'.format(colony.best_cost))

		strip_path_from_graph(graph, route)
		reset_graph(graph)