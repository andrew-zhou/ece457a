from aco.acocolony import ACOColony
import random

class ACOChromosome(object):
	def __init__(self, graph, goals):
		self.graph = graph
		self.goals = goals
		self.complete = False
		self.solutions = None

	def solve(self):
		self.solutions = []
		for goal in self.goals:
			self.graph[goal]._goal = True
			colony = ACOColony(self.graph, 1)
			colony.search()
			route = colony.best_path
			if route:
				self.solutions.append(([n.id for n in route], colony.best_cost))
				self._strip_path_from_graph(route)
			self._reset_graph()
		self.complete = True
		return self.solutions

	def mutate(self):
		"""Performs a swap mutation on the goals list to randomly swap positions
		between two drones.
		"""
		a, b = random.randint(0, len(self.goals) - 1), random.randint(0, len(self.goals) - 1)
		self.goals[a], self.goals[b] = self.goals[b], self.goals[a]

	@classmethod
	def crossover(cls, dad, mom):
		"""We do cycle crossover between the dad and mom to get
		two new children chromosomes.

		Returns: two lists of crossover'd goals
		"""
		cycles = []
		keys_dad = {g: idx for idx, g in enumerate(dad.goals)}
		keys_mom = {g: idx for idx, g in enumerate(mom.goals)}
		child_a = [0 for _ in range(len(dad.goals))]
		child_b = [0 for _ in range(len(dad.goals))]
		used = set()

		for i in range(len(dad.goals)):
			if i in used:
				# Index already in a cycle
				continue
			new_cycle = set()
			p = i
			while p not in new_cycle:
				new_cycle.add(p)
				p = keys_dad[mom.goals[p]]
			used |= new_cycle
			cycles.append(new_cycle)

		flip = True
		for cycle in cycles:
			for i in cycle:
				if flip:
					child_a[i] = dad.goals[i]
					child_b[i] = mom.goals[i]
				else:
					child_a[i] = mom.goals[i]
					child_b[i] = dad.goals[i]
		return (child_a, child_b)

	def get_solutions(self):
		return self.solutions if self.complete else None

	def _strip_path_from_graph(self, path):
		for i in range(len(path) - 1):
			n = path[i].id
			next_ = path[i + 1].id
			del self.graph[n].neighbours[next_]
			del self.graph[n].distances[next_]
			del self.graph[n].pheromones[next_]
			del self.graph[next_].neighbours[n]
			del self.graph[next_].distances[n]
			del self.graph[next_].pheromones[n]

	def _reset_graph(self):
		for node in self.graph.values():
			for id_ in node.pheromones:
				node.pheromones[id_] = 0.0
			node._goal = False
