from aco.acocolony import ACOColony
import random

class ACOChromosome(object):
	def __init__(self, graph, goals):
		self.graph = graph
		self.goals = goals
		self.complete = False
		self.solutions = None
		self.used_edges = set()

	def solve(self):
		self.solutions = []
		for goal in self.goals:
			colony = ACOColony(self.graph, self.used_edges, goal)
			colony.search()
			route = colony.best_path
			if route:
				self.solutions.append(([n.id for n in route], colony.best_cost))
				self._add_forbidden_moves(route)
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

	def _add_forbidden_moves(self, route):
		for idx in range(len(route) - 1):
			edge = (route[idx].id, route[idx + 1].id)
			self.used_edges.add(edge)
