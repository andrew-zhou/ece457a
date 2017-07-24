#!/bin/python3
import random
import Queue
import threading
import math

from chromosome import Chromosome

from gaconstants import POP_SIZE
from gaconstants import TOURNAMENT_SIZE
from gaconstants import ITERATION
from gaconstants import ELITISM_RATE
from gaconstants import MUTATION_RATE

class Population(object):
    def __init__(self, graph, goal, removed_graph):
      self.graph = graph
      self.goal = goal
      self.removed_graph = removed_graph
      # generate random population
      self.chromosomes = []
      self._generate_random_population()

      # selection algorithm
      self.selection = self._tournament_selection

    def _generate_random_population(self):
      self.chromosomes = []
      for _ in range(POP_SIZE):
        c = Chromosome(self.goal)
        c.calculate_fitness(self.graph, self.removed_graph)
        self.chromosomes.append(c)
      # sort population
      self.chromosomes = sorted(self.chromosomes, key=lambda x: x.fitness)

    def _tournament_selection(self):
      best = random.choice(self.chromosomes)
      for i in range(TOURNAMENT_SIZE):
        cont = random.choice(self.chromosomes)
        if (cont.fitness < best.fitness):
          best = cont

      return best

    def _crossover(self, q, c1, c2):
      new1, new2 = c1.crossover(c2)
      new1.calculate_fitness(self.graph, self.removed_graph)
      new2.calculate_fitness(self.graph, self.removed_graph)
      q.put(new1)
      q.put(new2)

    def _mutate(self, c):
      new1 = c.mutate()
      new1.calculate_fitness(self.graph, self.removed_graph)
      return new1

    def evolve(self):
      for i in range(ITERATION):
        print "Generation " + str(i)
        # elitism
        idx = int(round(POP_SIZE * ELITISM_RATE))
        self.chromosomes = self.chromosomes[:idx]
        buf = self.chromosomes

        iteration = int(math.ceil((POP_SIZE - idx) / 2.0))
        q = Queue.Queue()
        threads = []
        for i in range(iteration):
          c1 = self.selection()
          c2 = self.selection()
          t = threading.Thread(target=self._crossover, args = (q, c1, c2))
          threads.append(t)

        for t in threads:
          t.start()

        for i in range(2*iteration):
          buf.append(q.get())

        for i in range (idx, len(buf)):
          r = random.random()
          if r <= MUTATION_RATE:
            buf[i] = self._mutate(buf[i])

        # while idx < POP_SIZE:
        #   r = random.random()
        #   if r <= MUTATION_RATE:
        #     c1 = self.selection()
        #     new1 = c1.mutate()
        #     new1.calculate_fitness(self.graph, self.removed_graph)
        #     buf.append(new1)
        #     idx += 1
        #   else:
        #     c1 = self.selection()
        #     c2 = self.selection()
        #     new1, new2 = c1.crossover(c2)
        #     new1.calculate_fitness(self.graph, self.removed_graph)
        #     new2.calculate_fitness(self.graph, self.removed_graph)
        #     buf.append(new1)
        #     buf.append(new2)
        #     idx += 2
        self.chromosomes = buf[:POP_SIZE]
        self.chromosomes = sorted(self.chromosomes, key=lambda x: x.fitness)
        print "Best fitness in current generation: " + str(self.chromosomes[0].fitness)
      print "Best overall fitness: " + str(self.chromosomes[0].fitness)
      return self.chromosomes[0].print_path(self.graph, self.removed_graph)
