import sys
import time
import argparse
import copy
sys.path.insert(0, '../graph')

from iomanager import IOManager
from iomanager import GraphNode

from population import Population
from chromosome import Chromosome

from graph import Graph

from gaconstants import START_NODE

def remove_cycle(path):
  new_path = copy.deepcopy(path)
  for i in range(len(new_path)):
    if i >= len(new_path): break
    n1 = new_path[i]
    for j in range(i+1, len(new_path)):
      if j >= len(new_path): break
      n2 = new_path[j]
      if n1 == n2:
        new_path = new_path[:i] + new_path[j:]
        i-=1
        break
  return new_path

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--graph', help='File name for graph', required=True)
  parser.add_argument('--goals', nargs='+', help='Goal node ids for drones', required=True)
  args = parser.parse_args()
  goals = [int(g) for g in args.goals]
  graph = IOManager.import_graph(args.graph)

  # IOManager.export_graph(graph, '../aco/waterloo.ecegraph')
  # graph = IOManager.import_graph('../aco/waterloo.ecegraph')

  paths = []
  costs = []
  removed = {}
  start_time = time.time()
  for goal in goals:
    end = goal
    population = Population(graph[START_NODE], end, removed)
    path = population.evolve()
    path = remove_cycle(path)
    new_cost = Chromosome.calc_costs(path, graph, goal, removed)
    costs.append(new_cost)
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
  print 'path: ' + str(paths)
  print 'costs: ' + str(costs)
  print('Overall time: {}'.format(end_time - start_time))

  # if graph != None:
    # graph.plotMovementsMultiPaths(paths, routes)

if __name__ == '__main__':
  main()