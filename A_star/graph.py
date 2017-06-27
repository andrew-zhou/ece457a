class Node:
	SIZE = 1

	def __init__(self, pos):
		self.pos = pos

	def neighbours_iter(self):
		x, y, z = self.pos
		new_positions = [
			(x + Node.SIZE, y, z), (x - Node.SIZE, y, z),
			(x, y + Node.SIZE, z), (x, y - Node.SIZE, z),
			(x, y, z + Node.SIZE), (x, y, z - Node.SIZE)
		]

		for new_position in new_positions:
			yield Node(new_position)
