from aco.ant import Ant
from aco.acoconstants import NUM_ANTS, NUM_ITERATIONS, UPDATE_CONST, EVAPORATION_CONST, START_NODE
import math

class ACOColony(object):
	def __init__(self, graph, forbidden_moves, goal):
		"""Colony manages the ants.

		Parameters:
			graph: (dict) key-value pairs are id-ACONode
			start_id: (int) id of start ACONode
		"""
		self.graph = graph
		self.best_path = None
		self.best_cost = math.inf
		self.pheromone_map = {}
		self.forbidden_moves = forbidden_moves
		self.goal = goal

	def search(self):
		start = self.graph[START_NODE]
		for _ in range(NUM_ITERATIONS):
			self.ants = [Ant(start, self.pheromone_map, self.forbidden_moves, self.goal) for _ in range(NUM_ANTS)]

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

			# Evaporate pheromones
			for k, v in self.pheromone_map.items():
				self.pheromone_map[k] = v * (1 - EVAPORATION_CONST)

			# Add pheromones
			for k, v in pheromone_updates.items():
				if k not in self.pheromone_map:
					self.pheromone_map[k] = 0.0
				self.pheromone_map[k] += v

	def _populate_pheromone_updates(self, ant, updates):
		route = ant.get_route()
		cost = ant.get_cost()
		if not route:
			return
		for i in range(len(route) - 1):
			m, n = route[i], route[i + 1]
			if (m.id, n.id) not in updates:
				updates[(m.id, n.id)] = 0.0
			updates[(m.id, n.id)] += UPDATE_CONST / cost
			if (n.id, m.id) not in updates:
				updates[(n.id, m.id)] = 0.0
			updates[(n.id, m.id)] += UPDATE_CONST / cost
