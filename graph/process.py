import csv
import sys
import math
import matplotlib.pyplot as plt
import numpy as np

if len(sys.argv) != 2:
  print "Error: submit csv file"
  sys.exit()

with open(sys.argv[1], 'rb') as csvfile:
  reader = csv.reader(csvfile, delimiter=',')
  iterreader = iter(reader)
  # skip header
  next(iterreader)
  coordxy = []
  lastY = 0
  xArr = []
  coords = []
  for row in iterreader:
    x = float(row[0])
    y = float(row[1])
    h = float(row[2])
    if (y != lastY):
      coords.append(xArr)
      lastY = y
      xArr = [h]
    else:
      xArr.append(h)
  coords.append(xArr)
  del coords[0]

  filename = sys.argv[1].split('.')[0]
  print filename
  with open(filename+'.map', 'w') as mapfile:
    for c in coords:
      mapfile.write(' '.join(map(str, c)) + '\n')