from ant import Ant
from acoconstants import NUM_ANTS, NUM_ITERATIONS, UPDATE_CONST, EVAPORATION_CONST
import math

class ACOColony(object):
	def __init__(self, graph, start_id):
		"""Colony manages the ants.

		Parameters:
			graph: (dict) key-value pairs are id-ACONode
			start_id: (int) id of start ACONode
		"""
		self.graph = graph
		self.start_id = start_id
		self.best_path = None
		self.best_cost = math.inf

	def search(self):
		start = self.graph[self.start_id]
		for _ in range(NUM_ITERATIONS):
			self.ants = [Ant(start) for _ in range(NUM_ANTS)]

			for ant in self.ants:
				ant.start()

			for ant in self.ants:
				ant.join()

			pheromone_updates = {}  # Key-value is (x, y) to get pheromones to add for x-id to y-id
			for ant in self.ants:
				self._populate_pheromone_updates(ant, pheromone_updates)
				if ant.get_cost() < self.best_cost:
					self.best_cost = ant.get_cost()
					self.best_path = ant.get_route()

			for node in self.graph.values():
				for id_, old_pheromones in node.pheromones.items():
					new_pheromones = old_pheromones * (1 - EVAPORATION_CONST) + pheromone_updates.get((node.id, id_), 0.0)
					node.pheromones[id_] = new_pheromones

	def _populate_pheromone_updates(self, ant, updates):
		route = ant.get_route()
		cost = ant.get_cost()
		for i in range(len(route) - 1):
			m, n = route[i], route[i + 1]
			if (m.id, n.id) not in updates:
				updates[(m.id, n.id)] = 0.0
			updates[(m.id, n.id)] += UPDATE_CONST / cost
			if (n.id, m.id) not in updates:
				updates[(n.id, m.id)] = 0.0
			updates[(n.id, m.id)] += UPDATE_CONST / cost
