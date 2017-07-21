#!/bin/python3

import math
import threading
import random

import aco.acoconstants as acoconstants

class Ant(threading.Thread):
    def __init__(self, start):
        """Initializes an ant to traverse from start to a goal node.

        start: Starting node in graph
        """
        super(Ant, self).__init__()
        self.location = start
        self.route = [start]
        self.cost = 0.0
        self.complete = False

    def run(self):
        while True:
            # Finish if we have reached a goal
            if self.location.is_goal():
                break
            next_ = self._pick_next()
            # Finish if no more possible steps
            if not next_:
                break
            self._traverse(next_)
            
        self.complete = True

    def _pick_next(self):
        attractiveness = {}
        attr_total = 0.0
        considered = []
        for neighbour in self.location.neighbours.values():
            # Ignore if already visited
            if neighbour in self.route:
                continue
            pheromones = self.location.pheromones_to(neighbour.id)
            desirability = 1.0 / self.location.cost_to(neighbour.id)
            attractiveness[neighbour.id] = (pheromones ** acoconstants.ALPHA) * (desirability ** acoconstants.BETA)
            attr_total += attractiveness[neighbour.id]
            considered.append(neighbour)

        # If no neighbours considered, return None
        if not attractiveness:
            return None

        # If sum attractiveness is 0, pick next neighbour randomly
        if attr_total == 0.0:
            return random.choice(considered)

        # Spin a weighted roulette wheel to pick next node
        spin = random.random()
        for neighbour in considered:
            weight = attractiveness[neighbour.id] / attr_total
            spin -= weight
            if spin <= 0:
                return neighbour

        # Should never reach this point
        raise Exception('Something in the code broke if we reached this point')

    def _traverse(self, next_):
        self.cost += self.location.cost_to(next_.id)
        self.route.append(next_)
        self.location = next_

    def get_route(self):
        """Public accessor for route. Returns None if not complete."""
        return self.route if self.complete else None

    def get_cost(self):
        """Public accessor for cost. Returns None if not complete."""
        if not self.complete:
            return None
        if not self.route[-1].is_goal():
            return math.inf
        return self.cost
