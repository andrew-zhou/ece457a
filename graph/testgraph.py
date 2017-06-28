import sys
from graph import Graph

graph = Graph('waterloo.map')
movements = []
for i in range(0, 10):
  movements.append((1, 1))

for i in range(0, 10):
  movements.append((0, 1))

for i in range(0, 100):
  movements.append((1, 0))
graph.plotMovement(movements)
sys.exit()