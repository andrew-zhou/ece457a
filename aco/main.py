from acocolony import ACOColony
from aconode import ACONode
from acoconstants import NUM_NODES, MIN_DIST, MAX_DIST, MAX_NEIGHBOURS

import random

def build_graph():
	nodes = {id_: ACONode(id_, False) for id_ in range(NUM_NODES)}
	for node in nodes.values():
		num_neighbours = random.randint(1, MAX_NEIGHBOURS)
		for _ in range(num_neighbours):
			id_ = random.randint(0, NUM_NODES - 1)
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
	goal = random.randint(0, NUM_NODES - 1)
	print('GOAL: {}'.format(goal))
	nodes[goal]._goal = True
	return nodes

graph = {
	0: ACONode(0, False),
	1: ACONode(1, False),
	2: ACONode(2, False),
	3: ACONode(3, True),
}

graph[0].neighbours = {
	1: graph[1],
	3: graph[3],
}
graph[0].distances = {
	1: 2,
	3: 5,
}
graph[0].pheromones = {
	1: 0.0,
	3: 0.0
}
graph[1].neighbours = {
	1: graph[1],
	2: graph[2],
}
graph[1].distances = {
	1: 2,
	2: 2,
}
graph[1].pheromones = {
	1: 0.0,
	2: 0.0
}
graph[2].neighbours = {
	1: graph[1],
	3: graph[3],
}
graph[2].distances = {
	1: 2,
	3: 2,
}
graph[2].pheromones = {
	1: 0.0,
	3: 0.0
}
graph[3].neighbours = {
	0: graph[0],
	2: graph[2],
}
graph[3].distances = {
	0: 5,
	2: 2,
}
graph[3].pheromones = {
	0: 0.0,
	2: 0.0
}

if __name__ == '__main__':
	# graph = build_graph()
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