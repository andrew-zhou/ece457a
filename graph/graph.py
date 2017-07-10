import matplotlib.pyplot as plt
import numpy as np

INFINITY = 99999999

class Graph(object):
  def __init__(self, mapfile__name='graph/waterloo.map', start_pos=(0,0,0)):
    self.map = []
    with open(mapfile__name, 'rb') as mapfile:
      while True:
        row = mapfile.readline()
        if row == '':
          break;
        row = map(float, row.split(' '))
        self.map.append(row)
    self.height = len(self.map) / 5
    self.width = len(self.map[0]) / 5
    self.start_pos = (start_pos[0], start_pos[1], self.map[0][0]+1)
    self.finish_pos = (self.width - 1, self.height - 1, self.get(self.width-1, self.height-1)+1)
    self.pos = (start_pos[0], start_pos[1], self.map[0][0]+1)
    self.movement = [self.pos]

  def get(self, x, y):
    return self.map[y][x]

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
    plt.scatter(scatX, scatY, s=3)
    plt.show()