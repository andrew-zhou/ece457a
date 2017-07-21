#!/bin/python3

import math

class GraphNode(object):
    def __init__(self, id_):
        self.id = id_
        self.neighbours = {}
        self.distances = {}

    def cost_to(self, id):
        return self.distances.get(id, math.inf)

class IOManager(object):
    """IOManager handles converting between dictionaries of GraphNode objects and
    .ecegraph files.
    """
    @classmethod
    def import_graph(cls, filename, node_cls=GraphNode):
        """Returns a dictionary of GraphNode objects.

        Parameters:
            filename: Name of .ecegraph file to import (ie. map.ecegraph)

        Returns:
            Dictionary where keys are ids and values are GraphNode objects.

        Example:
            graph = IOManager.import_graph('g.ecegraph')
        """
        with open(filename, 'r') as file:
            num_nodes = None
            graph = {}
            for line in file:
                if num_nodes is None:
                    num_nodes = int(line)
                    graph = {id_: node_cls(id_) for id_ in range(1, num_nodes + 1)}
                else:
                    m, n, dist = line.split(' ')
                    m = int(m)
                    n = int(n)
                    dist = float(dist)
                    graph[m].neighbours[n] = graph[n]
                    graph[n].neighbours[m] = graph[m]
                    graph[m].distances[n] = dist
                    graph[n].distances[m] = dist
            return graph

    @classmethod
    def export_graph(cls, graph, filename):
        """Saves the graph as an .ecegraph file.

        Parameters:
            graph: Dictionary of id keys to GraphNode object values
            filename: Name of .ecegraph file to save to
        """
        edges = {}
        for node in graph.values():
            for neighbour, dist in node.distances.items():
                if (node.id, neighbour) in edges or (neighbour, node.id) in edges:
                    continue
                edges[(node.id, neighbour)] = dist

        file_string = '{}\n'.format(len(graph))
        for edge, dist in edges.items():
            file_string = file_string + '{} {} {}\n'.format(edge[0], edge[1], dist)
        file_string = file_string[:-1]  # Strip the last \n

        with open(filename, 'w') as file:
            file.write(file_string)
