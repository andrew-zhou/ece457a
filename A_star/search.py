import math

from graph import Node

HEIGHT_MAP = [
	[0, 5, 0, 0, 0],
	[5, 0, 0, 0, 0],
	[0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0],
	[0, 0, 0, 0, 3]
]

def heuristic(node, goal):
	curX, curY, curZ = node.pos
	endX, endY, endZ = goal.pos

	return ((endX - curX)**2 + (endY - curY)**2 + (endZ - curZ)**2)**0.5

def step_cost(node, neighbour):
	# Components of cost:
	# - Length = Base = 1
	# - Collision = infinity
	# - Height = neighbour.pos.z
	newX, newY, newZ = neighbour.pos
	if newZ < 0 or newY < 0 or newY > len(HEIGHT_MAP) - 1 or newX < 0 or newX > len(HEIGHT_MAP[0]) - 1:
		return math.inf

	length_cost = 1
	if newZ > HEIGHT_MAP[newY][newX]:
		collision_cost = 0
	else:
		collision_cost = math.inf
	height_cost = newZ
	return length_cost + collision_cost + height_cost

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
			neighbour_path_cost = path_cost[current.pos] + step_cost(current, neighbour)
			if neighbour.pos in path_cost and neighbour_path_cost >= path_cost[neighbour.pos]:
				continue # This is not a better path.

			# This path is the best until now. Record it!
			came_from[neighbour.pos] = current.pos
			path_cost[neighbour.pos] = neighbour_path_cost
			est_total_cost[neighbour.pos] = path_cost[neighbour.pos] + heuristic(neighbour, goal)

	return []

if __name__ == '__main__':
	start = Node((0, 0, 0))
	goal = Node((4, 4, 4))
	path, cost = A_star_search(start, goal)

	print('--- OPTIMAL PATH ---')
	for idx, node_pos in enumerate(path):
		print('{}: {}'.format(idx, node_pos))
	print('--- COST: {} ---'.format(cost))
