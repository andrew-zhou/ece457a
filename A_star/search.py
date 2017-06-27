from graph import Node

HEIGHT_MAP = [
	[0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0]
]

def heuristic(node, goal):
	curX, curY, curZ = node.pos
	endX, endY, endZ = goal.pos

	return ((endX - curX)**2 + (endY - curY)**2 + (endZ - curZ)**2)**0.5

def reconstruct_path(came_from, current):
	pos = current.pos
	total_path = [pos]
	while pos in came_from:
		pos = came_from[pos]
		total_path.append(pos)
	return reversed(total_path)

def A_star_search(start, goal):
	path_cost = {}
	path_cost[start.pos] = 0.0

	est_total_cost = {}
	est_total_cost[start.pos] = path_cost[start.pos] + heuristic(start, goal)

	closed_set = set()
	open_set = {start.pos: start}

	came_from = {}

	while len(open_set) > 0:
		current = min(open_set.values(), key=lambda n: est_total_cost[n.pos])
		if current.pos == goal.pos:
			return reconstruct_path(came_from, current), est_total_cost[goal.pos]

		del open_set[current.pos]
		closed_set.add(current.pos)

		for neighbour in current.neighbours_iter():
			# Ignore the neighbor which is already evaluated.
			if neighbour.pos in closed_set:
				continue

			# Discover a new node
			if neighbour.pos not in open_set:
				open_set[neighbour.pos] = neighbour

			# The distance from start to a neighbor
			neighbour_path_cost = path_cost[current.pos] + 1
			if neighbour.pos in path_cost and neighbour_path_cost >= path_cost[neighbour.pos]:
				continue # This is not a better path.

			# This path is the best until now. Record it!
			came_from[neighbour.pos] = current.pos
			path_cost[neighbour.pos] = neighbour_path_cost
			est_total_cost[neighbour.pos] = path_cost[neighbour.pos] + heuristic(neighbour, goal)

	return []

if __name__ == '__main__':
	start = Node((0, 0, 0))
	goal = Node((5, 5, 5))
	path, cost = A_star_search(start, goal)

	print('--- OPTIMAL PATH ---')
	for idx, node_pos in enumerate(path):
		print('{}: {}'.format(idx, node_pos))
	print('--- COST: {} ---'.format(cost))
