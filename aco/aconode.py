#!/bin/python3

import math

class ACONode(object):
    def __init__(self, id_, goal):
        self.id = id_
        self.neighbours = {}
        self.distances = {}
        self.pheromones = {}
        self._goal = goal

    def pheromones_to(self, id):
        return self.pheromones.get(id, 0)

    def cost_to(self, id):
        return self.distances.get(id, math.inf)

    def is_goal(self):
        return self._goal