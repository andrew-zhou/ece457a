import sys

sys.path.insert(0, '../graph')

from iomanager import IOManager
from iomanager import GraphNode

import math
import itertools
import matplotlib.pyplot as plt
import numpy as np

INFINITY = 99999999

graph_cache = {}

class Graph(object):
  def __init__(self, mapfile__name='../graph/waterloo.map', start_pos=(0,0,0)):
    self.map = []
    with open(mapfile__name, 'rb') as mapfile:
      while True:
        row = mapfile.readline()
        if row == '':
          break;
        row = map(float, row.split(' '))
        self.map.append(row)

    self.height = len(self.map) / 10
    self.width = len(self.map[0]) / 10

    # data to convert between different map representations
    self.id_xy = {}
    self.id_map = []
    grid_id = 1
    for y in range(self.height):
      new_row = []
      for x in range(self.width):
        self.id_xy[grid_id] = (x, y)
        new_row.append((self.map[y][x], grid_id))
        grid_id += 1
      self.id_map.append(new_row)

    self.start_pos = (start_pos[0], start_pos[1], self.map[0][0]+1)
    self.finish_pos = (self.width - 1, self.height - 1, self.get(self.width-1, self.height-1)+1)
    self.pos = (start_pos[0], start_pos[1], self.map[0][0]+1)
    self.movement = [self.pos]

  def toGraphNode(self):
    graph_cache.clear()
    g = self.getWithId(self.start_pos[0], self.start_pos[1])
    h = g[0]
    i = g[1]
    node = GraphNode(i)
    graph_cache[i] = node
    self._toGraphNode(node, self.start_pos[0], self.start_pos[1], h)
    print graph_cache
    return graph_cache


  def _toGraphNode(self, node, x, y, h):
    self._linkGraph(node, h, x+1, y)
    self._linkGraph(node, h, x-1, y)
    self._linkGraph(node, h, x, y+1)
    self._linkGraph(node, h, x, y-1)
    self._linkGraph(node, h, x+1, y+1)
    self._linkGraph(node, h, x+1, y-1)
    self._linkGraph(node, h, x-1, y+1)
    self._linkGraph(node, h, x-1, y-1)

  def _linkGraph(self, node, h, nx, ny):
    g = self.getWithId(nx, ny)
    if g != None:
      oh = g[0]
      oi = g[1]
      recurse = False
      if oi in graph_cache:
        new_node = graph_cache[oi]
      else:
        new_node = GraphNode(oi)
        graph_cache[oi] = new_node
        recurse = True
      node.neighbours[oi] = new_node
      node.distances[oi] = abs(h - oh) + 1
      if recurse:
        self._toGraphNode(new_node, nx, ny, oh)

  def get(self, x, y):
    if y < 0 or y >= self.height or x < 0 or x >= self.width:
      return None
    return self.map[y][x]

  def getWithId(self, x, y):
    if y < 0 or y >= self.height or x < 0 or x >= self.width:
      return None
    return self.id_map[y][x]

  def setStart(self, pos):
    self.start_pos = (pos[0], pos[1], self.map[0][0]+1)
    self.pos = (start_pos[0], start_pos[1], self.map[0][0]+1)

  def calcMovementPenalty(self, movements):
    lastPos = self.start_pos;
    curPos = (0, 0, 0)
    penalty = 0
    for movement in movements:
      # add 1 penalty for each movement
      penalty += 1
      curPos = (lastPos[0] + movement[0], lastPos[1] + movement[1], lastPos[2] + movement[2])
      curPenalty = self.calcPenalty(lastPos, curPos)
      # if (curPenalty == INFINITY):
      #   # return immidiately if it's an invalid move
      #   return INFINITY
      penalty += curPenalty
      lastPos = curPos
    return penalty

  # x, y, z E [-1, 1]
  def move(self, x, y, z):
    newPos = (self.pos[0] + x, self.pos[1] + y, self.pos[2] + z)
    penalty = self.calcPenalty(self.pos, newPos)
    if (penalty == INFINITY):
      raise Exception("invalid tile")
    self.pos = (self.pos[0] + x, self.pos[1] + y, self.pos[2] + z)

  def calcPenalty(self, lastPos, pos):
    if pos[0] < 0 or pos[0] >= self.width:
      return 100
    if pos[1] < 0 or pos[1] >= self.height:
      return 100
    if pos[2] <= self.get(pos[0], pos[1]):
      return 100
    if pos == self.finish_pos:
      return -1000
    return 0

  def plot(self):
    coord = np.array(self.map, dtype=float)
    plt.imshow(coord, cmap='hot', interpolation='nearest')
    plt.show()

  def plotMovementsMultiPaths(self, paths, routes):
    colors = itertools.cycle(['g', 'b', 'c', 'm', 'y', 'k', 'w'])
    new_map = []
    for i in range(self.height):
      new_map.append(self.map[i][:self.width])

    scatters = []
    for p in paths:
      scatX = []
      scatY = []
      for i in p:
        xy = self.id_xy[i]
        scatX.append(xy[0])
        scatY.append(xy[1])
      scatters.append((scatX, scatY))

    coord = np.array(new_map, dtype=float)
    plt.imshow(coord, cmap='hot', interpolation='nearest')
    for scat, route in zip(scatters, routes):
      c = next(colors)
      plt.plot(scat[0], scat[1], color=c)
      start = self.id_xy[route[0]]
      end = self.id_xy[route[1]]
      rX = [start[0], end[0]]
      rY = [start[1], end[1]]
      plt.scatter(rX, rY, s=40, color=c)
    plt.show()

  def plotMovementsIds(self, ids):
    new_map = []
    for i in range(self.height):
      new_map.append(self.map[i][:self.width])
    scatX = []
    scatY = []
    for i in ids:
      xy = self.id_xy[i]
      scatX.append(xy[0])
      scatY.append(xy[1])

    coord = np.array(new_map, dtype=float)
    plt.imshow(coord, cmap='hot', interpolation='nearest')
    plt.scatter(scatX, scatY, s=10)
    plt.show()

  def plotMap(self):
    new_map = []
    for i in range(self.height):
      new_map.append(self.map[i][:self.width])

    coord = np.array(new_map, dtype=float)
    plt.imshow(coord, cmap='hot', interpolation='nearest')
    plt.show()

  def plotMovement(self, movements):
    scatX = [self.pos[0]]
    scatY = [self.pos[1]]
    for m in movements:
      scatX.append(scatX[len(scatX)-1]+m[0])
      scatY.append(scatY[len(scatY)-1]+m[1])

    new_map = []
    for i in range(self.height):
      new_map.append(self.map[i][:self.width])

    coord = np.array(new_map, dtype=float)
    plt.imshow(coord, cmap='hot', interpolation='nearest')
    plt.scatter(scatX, scatY, s=10)
    plt.show()