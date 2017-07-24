import sys
import time
import argparse
sys.path.insert(0, '../graph')

from iomanager import IOManager
from iomanager import GraphNode

from population import Population

from graph import Graph

from gaconstants import START_NODE

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--graph', help='File name for graph', required=True)
  parser.add_argument('--goals', nargs='+', help='Goal node ids for drones', required=True)
  args = parser.parse_args()
  goals = [int(g) for g in args.goals]
  graph = IOManager.import_graph(args.graph)

  paths = []
  removed = {}
  start_time = time.time()
  for goal in goals:
    end = goal
    population = Population(graph[START_NODE], end, removed)
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
  end_time = time.time()
  print('Overall time: {}'.format(end_time - start_time))

  # if graph != None:
    # graph.plotMovementsMultiPaths(paths, routes)

if __name__ == '__main__':
  main()