#!/bin/python3

import threading
import random

import acoconstants

class Ant(threading.Thread):
    def __init__(self, start):
        """Initializes an ant to traverse from start to a goal node.

        start: Starting node in graph
        """
        self.location = start
        self.route = []
        self.cost = 0.0
        # TODO: Might want to track completion status to one of: goal, no more moves, max iterations
        self.complete = False

    def run(self):
        # TODO: We may want an optional max number of iterations
        while True:
            next_ = self._pick_next()
            # Finish if no more possible steps
            if not next_:
                break
            self._traverse(next_)
            # Finish if we have reached a goal
            if self.location.is_goal():
                break
        self.complete = True

    def _pick_next(self):
        attractiveness = {}
        attr_total = 0.0
        considered = []
        # TODO: Implement this in nodes
        for neighbour in self.location.neighbours:
            # Ignore if already visited
            if neighbour in self.route:
                continue
            # TODO: Implement this stuff
            pheromones = self.location.pheromones_to(neighbour)
            desirability = 1.0 / self.location.cost_to(neighbour)
            attractiveness[neighbour.id] = (pheromones ** acoconstants.ALPHA) * (cost ** acoconstants.BETA)
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
        # TODO: Implement this in node
        self.cost += self.location.cost_to(next_)
        self.route.append(next_)
        self.location = next_

    def get_route(self):
    """Public accessor for route. Returns None if not complete."""
    return self.route if self.complete else None

    def get_cost(self):
    """Public accessor for cost. Returns None if not complete."""
    return self.cost if self.complete else None
