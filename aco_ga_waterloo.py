import sys

from graph.iomanager import IOManager
from graph.iomanager import GraphNode

from ga.population import Population
from ga.gaconstants import START_NODE

from graph.graph import Graph

from acosolver import ACOSolver

def main():
  goals = [226, 228, 230];
  routes = [(1, goals[0]), (1, goals[1]), (1, goals[2])]
  raw_graph = Graph(mapfile__name='./graph/waterloo.map')
  graph = raw_graph.toGraphNode()
  # generate ecegraph
  # IOManager.export_graph(graph, '../aco/waterloo.ecegraph')
  # graph = IOManager.import_graph('../aco/waterloo.ecegraph')

  solver = ACOSolver.from_graph(graph, goals)

  score, solutions, order = solver.solve()
  solutions = [soln[0] for soln in solutions]
  print('Best overall score: {}'.format(score))
  print('Best order of goal nodes: {}'.format(order))
  print('Best path solutions: {}'.format(solutions))

  paths = []
  removed = {}
  for goal in goals:
    end = goal
    population = Population(graph[START_NODE], end, removed)
    path = population.evolve()
    paths.append(path)
    # remove path from graph
    for p in path:
      removed[p] = p

  if raw_graph != None:
    # raw_graph.plotMovementsMultiPaths(solutions, routes, './result/aco.png')
    raw_graph.plotMovementsMultiPaths(paths, routes, './result/ga.png')


if __name__ == '__main__':
  main()