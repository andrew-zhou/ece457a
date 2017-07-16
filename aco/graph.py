def build_graph(matrix, max_height):
	"""Always assume that the matrix is square.

	Returns 3D list, where each graph[x][y][z] corresponds to an x, y, z point in space
	graph[x][y][z] = True if it is free space, false if it is an obstacle
	"""
	graph = []
	for x in range(len(matrix)):
		graph.append([])
		for y in range(len(matrix[0])):
			graph[x].append([])
			for z in range(max_height+1):
				graph[x][y].append(matrix[x][y] <= z)
	return graph