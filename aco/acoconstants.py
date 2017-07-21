#!/bin/python3

# Tuning Parameters
ALPHA = 0.5
BETA = 1.2

# Colony Parameters
NUM_ANTS = 8
NUM_ITERATIONS = 80
UPDATE_CONST = 1000.0
EVAPORATION_CONST = 0.4

# Graph Parameters
NUM_NODES = 10
MIN_DIST = 1
MAX_DIST = 10
MAX_NEIGHBOURS = 2

# Meta Parameters
NUM_CHROMOSOMES = 10  # This should always be even
NUM_GENERATIONS = 5
MUTATE_RATE = 0.1
CROSSOVER_RATE = 0.7