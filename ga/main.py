import sys
sys.path.insert(0, '../graph')

from iomanager import IOManager
from iomanager import GraphNode

from population import Population

from graph import Graph

def main():
  routes = [(1, 226), (9, 228), (17, 230)]
  raw_graph = Graph()
  graph = raw_graph.toGraphNode()
  # IOManager.export_graph(graph, '../aco/waterloo.ecegraph')
  # graph = IOManager.import_graph('../aco/waterloo.ecegraph')
  paths = []
  removed = {}
  for route in routes:
    start = route[0]
    end = route[1]
    population = Population(graph[start], end, removed)
    path = population.evolve()
    paths.append(path)
    # remove path from graph
    for p in path:
      removed[p] = p
    # s = path[0]
    # for i in range(1, len(path)):
    #   e = path[i]
    #   if e in graph[s].neighbours:
    #     del graph[s].neighbours[e]
    #   s = e
  if raw_graph != None:
    raw_graph.plotMovementsMultiPaths(paths, routes)

if __name__ == '__main__':
  main()