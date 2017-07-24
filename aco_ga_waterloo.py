import sys
import copy

from graph.iomanager import IOManager
from graph.iomanager import GraphNode

from ga.population import Population
from ga.chromosome import Chromosome
from ga.gaconstants import START_NODE

from graph.graph import Graph

from acosolver import ACOSolver

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
  goals = [226, 228, 230];
  routes = [(1, goals[0]), (1, goals[1]), (1, goals[2])]
  raw_graph = Graph(mapfile__name='./graph/waterloo.map')
  # path = [1, 23, 45, 66, 88, 89, 67, 87, 66, 45, 24, 23, 45, 67, 68, 67, 89, 111, 131, 111, 133, 154, 155, 156, 135, 136, 156, 177, 156, 135, 157, 178, 179, 178, 179, 180, 159, 160, 182, 181, 161, 183, 184, 206, 228, 207, 228, 207, 206, 228, 208, 230]
  # raw_graph.plotMovementsMultiPaths([path], [(1, 230)], './result/before_ga.png')
  # path = remove_cycle(path)
  # print path
  # raw_graph.plotMovementsMultiPaths([path], [(1, 230)], './result/after_ga.png')
  # return
  graph = raw_graph.toGraphNode()
  # generate ecegraph
  # IOManager.export_graph(graph, '../aco/waterloo.ecegraph')
  # graph = IOManager.import_graph('../aco/waterloo.ecegraph')

  solver = ACOSolver.from_graph(graph, goals)

  score, solutions, order = solver.solve()
  solutions = [soln[0] for soln in solutions]

  paths = []
  ga_scores = []
  removed = {}
  for goal in goals:
    end = goal
    population = Population(graph[START_NODE], end, removed)
    path = population.evolve()
    path = remove_cycle(path)
    new_cost = Chromosome.calc_costs(path, graph, goal, removed)
    print 'new path: ' + str(path)
    print 'new cost: ' + str(new_cost)
    ga_scores.append(new_cost)
    paths.append(path)
    # remove path from graph
    for p in path:
      removed[p] = p

  if raw_graph != None:
    raw_graph.plotMovementsMultiPaths(solutions, routes, './result/aco.png')
    raw_graph.plotMovementsMultiPaths(paths, routes, './result/ga.png')

  print 'GA:'
  print 'scores: ' + str(ga_scores)
  print 'paths: ' + str(paths)

  print 'ACO:'
  print('Best overall score: {}'.format(score))
  print('Best order of goal nodes: {}'.format(order))
  print('Best path solutions: {}'.format(solutions))

if __name__ == '__main__':
  main()