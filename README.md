# Comparison between Genetic Algorithms and Ant Colony Optimization for Multi-Agent Path Planning in 3D

## Introduction
This project attempts to solve 3D path planning for amazon drones using Genetic Algorithms and Ant Colony Optimization

## Directories
### /aco
Contains the logic for Ant Colony Optimization
### /ga
Contains the logic for Genetic Algorithms Optimization
### /graph
Contains the logic for generating graphs used to test the algorithms

## Setup
### running only the ACO algorithm
`python acosolver.py --graph <map file> --goals <node id 1> <node id 2> ...`

graph: the graph file used for the algorithm. E.g: waterloo.ecegraph

goals: the finishing node for each drone. All the drones start at node 1
### running only the GA algorithm
`cd ga`

`python main.py --graph <map file> --goals <node id 1> <node id 2> ...`

graph: the graph file used for the algorithm. E.g: ../waterloo.ecegraph

goals: the finishing node for each drone. All the drones start at node 1

### running both ACO and GA
`python aco_ga_waterloo.py`

this will run both the ACO and GA algorithm using the waterloo.ecegraph map with goals set to 226, 228, and 230

## Changing Parameters
### GA
The parameters for the GA can be changed in `ga/gaconstants.py`
### ACO
The parameters for the ACO can be changed in `aco/acoconstants.py`

**NOTE**: The list of figures, list of tables, and references do **not** count towards out report length of 6 pages.
