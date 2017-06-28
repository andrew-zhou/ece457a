import matplotlib.pyplot as plt
import numpy as np

INFINITY = 99999999

class Graph(object):
  def __init__(self, mapfile__name='waterloo.map', start_pos=(0,0,0)):
    self.map = []
    with open(mapfile__name, 'rb') as mapfile:
      while True:
        row = mapfile.readline()
        if row == '':
          break;
        row = map(float, row.split(' '))
        self.map.append(row)
    self.height = len(self.map)
    self.width = len(self.map[0])
    self.start_pos = (start_pos[0], start_pos[1], self.map[0][0]+1)
    self.pos = (start_pos[0], start_pos[1], self.map[0][0]+1)
    self.movement = [self.pos]

  def get(x, y):
    return self.map[y][x]

  def setStart(pos):
    self.start_pos = (pos[0], pos[1], self.map[0][0]+1)
    self.pos = (start_pos[0], start_pos[1], self.map[0][0]+1)

  # x, y, z E [-1, 1]
  def move(self, x, y, z):
    newPos = (self.pos[0] + x, self.pos[1] + y, self.pos[2] + z)
    penalty = self.calcPenalty(self.pos, newPos)
    if (penalty == INFINITY):
      raise Exception("invalid tile")
    self.pos = (self.pos[0] + x, self.pos[1] + y, self.pos[2] + z)

  def calcPenalty(self, lastPos, pos):
    if pos[0] < 0 or pos[0] >= self.width:
      return INFINITY
    if pos[1] < 0 or pos[1] >= self.height:
      return INFINITY
    if pos[2] <= self.get(pos[0], pos[1]):
      return INFINITY

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

    coord = np.array(self.map, dtype=float)
    plt.imshow(coord, cmap='hot', interpolation='nearest')
    plt.scatter(scatX, scatY, s=3)
    plt.show()