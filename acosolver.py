#!/bin/python3

import argparse
import copy
import random
import threading
import time

from graph.iomanager import IOManager
from aco.aconode import ACONode
from aco.acoconstants import NUM_CHROMOSOMES, NUM_GENERATIONS, MUTATE_RATE, CROSSOVER_RATE
from aco.acochromosome import ACOChromosome

class ACOSolver(object):
	def __init__(self, fname, goals):
		self.goals = goals
		self._setup_graph(fname)
		self._setup_chromosomes()

	def _setup_graph(self, fname):
		self.graph = IOManager.import_graph(fname, ACONode)

	def _setup_chromosomes(self):
		self.chromosomes = []
		for _ in range(NUM_CHROMOSOMES):
			order = copy.copy(self.goals)
			random.shuffle(order)
			self.chromosomes.append(ACOChromosome(self.graph, order))

	def solve(self):
		best_score, best_soln, best_order = None, None, None
		for _ in range(NUM_GENERATIONS):
			threads = [threading.Thread(target=c.solve) for c in self.chromosomes]
			for t in threads:
				t.start()
			for t in threads:
				t.join()			
			new_gen = []
			for i in range(0, NUM_CHROMOSOMES, 2):
				# Parse through pairs of chromosomes
				c1 = self.chromosomes[i]
				c2 = self.chromosomes[i+1]
				# Look for best score
				score1 = sum([sol[1] for sol in c1.get_solutions()])
				score2 = sum([sol[1] for sol in c2.get_solutions()])
				if not best_score or score1 < best_score:
					best_score = score1
					best_soln = c1.get_solutions()
					best_order = c1.goals
				if score2 < best_score:
					best_score = score2
					best_soln = c2.get_solutions()
					best_order = c2.goals
				# Mutate c1
				if random.random() < MUTATE_RATE:
					c1.mutate()
				goals1 = c1.goals
				# Mutate c2
				if random.random() < MUTATE_RATE:
					c2.mutate()
				goals2 = c2.goals
				# Crossover
				if random.random() < CROSSOVER_RATE:
					goals1, goals2 = ACOChromosome.crossover(c1, c2)
				# Add to new generation
				child1 = ACOChromosome(self.graph, goals1)
				child2 = ACOChromosome(self.graph, goals2)
				new_gen.append(child1)
				new_gen.append(child2)
			# Elitism model - keep best solution so far in population
			if best_order:
				best = ACOChromosome(self.graph, best_order)
				new_gen[-1] = best
			self.chromosomes = new_gen
		return (best_score, best_soln, best_order)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--graph', help='File name for graph', required=True)
	parser.add_argument('--goals', nargs='+', help='Goal node ids for drones', required=True)
	args = parser.parse_args()
	goals = [int(g) for g in args.goals]

	solver = ACOSolver(args.graph, goals)
	start_time = time.time()
	score, solutions, order = solver.solve()
	end_time = time.time()
	solutions = [soln[0] for soln in solutions]
	print('Best overall score: {}'.format(score))
	print('Best order of goal nodes: {}'.format(order))
	print('Best path solutions: {}'.format(solutions))
	print('Overall time: {}'.format(end_time - start_time))