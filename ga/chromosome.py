#!/bin/python3
import random
import copy

from gaconstants import CHROMOSOME_LEN
from gaconstants import MAX_GENE
from gaconstants import SINGLE_VALUE_CROSSOVER_ALPHA, CONFLICT_COST

class Chromosome(object):
    def __init__(self, goal):
      self.goal = goal
      self.fitness = 0
      # mutate and crossover algorithms
      self.mutate = self._uniform_mutate
      self.crossover = self._one_point_crossover

      # randomize chromosome data
      self.data = []
      self._generate_random_data()

    @classmethod
    def calc_costs(cls, path, graph, goal, removed_graph):
      cost = 0
      reached = False
      node = graph[path[0]]
      for p in path[1:]:
        if p in removed_graph:
          # node removed, bad path
          cost += CONFLICT_COST
        if (p == goal):
          #reached goal node
          reached = True
          break
        cost += node.cost_to(p)
        node = graph[p]
      if not reached:
        cost += 1000
      return cost


    @classmethod
    def from_chromosome(cls, chromo):
      c = cls(chromo.goal)
      for i in range(CHROMOSOME_LEN):
        c.data[i] = chromo.data[i]
      return c

    def _generate_random_data(self):
      self.data = []
      for _ in range(CHROMOSOME_LEN):
        self.data.append(self._generate_random_gene())

    def _generate_random_gene(self):
      return random.randint(0, MAX_GENE);

    def _uniform_mutate(self):
      mutate_chromo = Chromosome(self.goal)
      return mutate_chromo

    def _single_value_crossover(self, other):
      c1 = Chromosome.from_chromosome(self)
      c2 = Chromosome.from_chromosome(other)

      k = random.randint(0, CHROMOSOME_LEN-1)
      c1.data[k] = (SINGLE_VALUE_CROSSOVER_ALPHA * other.data[k]) + \
        ((1-SINGLE_VALUE_CROSSOVER_ALPHA) * self.data[k])
      c2.data[k] = (SINGLE_VALUE_CROSSOVER_ALPHA * self.data[k]) + \
        ((1-SINGLE_VALUE_CROSSOVER_ALPHA) * other.data[k])

      return c1, c2

    def _one_point_crossover(self, other):
      c1 = Chromosome.from_chromosome(self)
      c2 = Chromosome.from_chromosome(other)
      k = random.randint(0, CHROMOSOME_LEN-1)
      c1.data = c1.data[:k] + c2.data[k:]
      c2.data = c2.data[:k] + c1.data[k:]
      return c1, c2

    def calculate_fitness(self, graph, removed_graph):
      self.fitness = 0
      node = graph
      reached = False
      for gene in self.data:
        neighbour_size = len(node.neighbours)
        if neighbour_size == 0:
          # end of graph
          break
        idx = int(gene % (neighbour_size + 1))
        if idx == neighbour_size:
          # do not move
          continue
        node_id = list(node.neighbours)[idx]
        if node_id in removed_graph:
          # node removed, bad path
          self.fitness += CONFLICT_COST
        if (node_id == self.goal):
          #reached goal node
          reached = True
          break
        self.fitness += node.cost_to(node_id)
        node = node.neighbours[node_id]
      if not reached:
        self.fitness += 1000

    def print_path(self, graph, removed_graph):
      node = graph
      path = str(node.id)
      path_arr = [node.id]
      for gene in self.data:
        neighbour_size = len(node.neighbours)
        if neighbour_size == 0:
          # end of graph
          break
        idx = int(gene % (neighbour_size + 1))
        if idx == neighbour_size:
          # do not move
          continue
        node_id = list(node.neighbours)[idx]
        if node_id in removed_graph:
          # node removed, bad path
          pass
        node = node.neighbours[node_id]
        if (node_id == self.goal):
          #reached goal node
          path += ' -> ' + str(node.id)
          path_arr.append(node.id)
          break
        path += ' -> ' + str(node.id)
        path_arr.append(node.id)
      print path
      return path_arr
