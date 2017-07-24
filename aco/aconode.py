#!/bin/python3

import math

class ACONode(object):
    def __init__(self, id_):
        self.id = id_
        self.neighbours = {}
        self.distances = {}

    def cost_to(self, id):
        return self.distances.get(id, float('inf'))