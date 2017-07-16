import graph

test_matrix = [
	[0, 0, 5],
	[3, 1, 2],
	[0, 4, 0],
]

if __name__ == '__main__':
	print 'OG:'
	print test_matrix
	g = graph.build_graph(test_matrix, 5)
	for level in range(6):
		print "Level: {}".format(level)
		for y in range(3):
			print '{} {} {}'.format(g[0][y][level], g[1][y][level], g[2][y][level])