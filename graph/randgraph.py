import random

from graph.iomanager import GraphNode

def rand_graph(num_nodes, max_neighbours, min_dist, max_dist):
	nodes = {id_: GraphNode(id_) for id_ in range(1, num_nodes + 1)}
	for node in nodes.values():
		num_neighbours = random.randint(1, max_neighbours)
		for _ in range(num_neighbours):
			id_ = random.randint(1, num_nodes)
			if id_ == node.id:
				continue
			neighbour = nodes[id_]
			node.neighbours[id_] = neighbour
			neighbour.neighbours[node.id] = node
			distance = random.random() + random.randint(min_dist, max_dist - 1)
			node.distances[id_] = distance
			neighbour.distances[node.id] = distance
	return nodes