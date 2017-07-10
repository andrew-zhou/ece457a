import random
import sys
import math

from graph import graph

'''
5 bits per gene:
    b0b1b2: directional movement
    b3: move up in z if 1
    b4: move down in zif 1
    if b3 == 0 and b4 == 0: stay on same level
    if b3 == 1 and b4 == 1: invalid gene, remove

generate N * M genes per chromosome (size of map)
'''

geneSet = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!.,"
target = "Hi, my name is Jake Si! I like apples."

test_map = graph.Graph()

class Chromosome:

    def __init__(self, gene, length, generation=0):
        self.gene = gene
        self.fitness = Chromosome.update_fitness(gene, length)
        self.generation = generation
        self.length = length;

    def getGeneAtIndex(self, index):
        return int(self.gene[2*index] + self.gene[2*index+1])

    def replaceGeneAtIndex(self, index, n):
        strN = str(n)
        if n < 10:
            strN = '0' + strN
        newGene = self.gene[:2*index] + strN + self.gene[2*index+2:]
        self.gene = newGene
        assert(len(self.gene)%2 == 0)

    def exchange(self, index1, index2, mate):
        # index1 <= index2
        left = self.gene[:index1]
        right = self.gene[index2:]
        middle = mate.gene[index1:index2]
        self.gene = left + middle + right
        assert(len(self.gene)%2 == 0)

    def crossover(self, mate):
        '''
        Two point crossover
        '''
        generation = max(self.generation, mate.generation)
        index1 = random.randint(1, self.length - 2)
        index2 = random.randint(1, self.length - 2)
        if index1 > index2:
            index1, index2 = index2, index1

        self.exchange(index1, index2, mate)
        mate.exchange(index1, index2, self)
        return Chromosome(self.gene, self.length, self.generation+1), \
            Chromosome(mate.gene, mate.length, mate.generation+1)

    def mutate(self):
        '''
        Random index mutation
        '''
        index = random.randrange(0, self.length)
        oldGene = self.getGeneAtIndex(index)
        newGene = oldGene
        while newGene == oldGene:
            newGene = random.getrandbits(5)
        self.replaceGeneAtIndex(index, newGene)
        return Chromosome(self.gene, self.length, self.generation+1)

    @staticmethod
    def getMovements(chromo, length):
        movements = []
        tempChromo = chromo
        for i in range(length):
            gene = int(chromo[2*i] + chromo[2*i+1])
            movement = gene & 7
            gene = gene >> 3
            moveUp = gene & 1
            gene = gene >> 1
            moveDown = gene & 1

            if moveUp == 1 and moveDown == 1:
                # do not move
                continue

            moveX = 0
            moveY = 0
            moveZ = 0

            if moveUp == 1:
                moveZ = 1
            if moveDown == 1:
                moveZ = -1
            if movement == 0:
                moveX = -1
            elif movement == 1:
                moveX = 1
            elif movement == 2:
                moveY = -1
            elif movement == 3:
                moveY = 1
            elif movement == 4:
                moveX = -1
                moveY = -1
            elif movement == 5:
                moveX = -1
                moveY = 1
            elif movement == 6:
                moveX = 1
                moveY = -1
            elif movement == 7:
                moveX = 1
                moveY = 1
            else:
                assert(False)
            movements.append((moveX, moveY, moveZ))
        return movements

    @staticmethod
    def update_fitness(gene, length):
        movements = Chromosome.getMovements(gene, length)
        return test_map.calcMovementPenalty(movements)

    @staticmethod
    def gen_random(length):
        '''
        Generate random 5 bit genes
        '''
        chromo = ''
        for i in range(length):
            gene = random.getrandbits(5)
            if gene < 10:
                chromo = chromo + '0'
            chromo = chromo + str(gene)
        assert(len(chromo)%2 == 0)
        return Chromosome(chromo, length)

class Population:

    def __init__(self, tournamentSize=3, mutationRate=0.1, crossoverRate=0.9, elitismRate=0.1, populationSize=500):
        self.population = []
        self.tournamentSize = tournamentSize
        self.mutationRate = mutationRate
        self.crossoverRate = crossoverRate
        self.elitismRate = elitismRate
        self.populationSize = populationSize
        self.bestParent = None

    # def display(self, guess):
    #     print("{0}\t\t{1}\t{2}".format(guess.gene, guess.fitness, guess.generation))

    def generate_population(self):
        for i in range(0, self.populationSize):
            chromo = Chromosome.gen_random(test_map.width * test_map.height)
            self.population.append(chromo)


    def tournament_selection(self):
        best = random.choice(self.population)
        for i in range(self.tournamentSize):
            cont = random.choice(self.population)
            if (cont.fitness < best.fitness):
                best = cont

        return best

    def setup(self):
        self.generate_population()
        self.population = sorted(self.population, key=lambda x: x.fitness)
        for p in self.population:
            print p.fitness
        self.bestParent = self.population[0]
        print self.bestParent.fitness

    def evolve(self):
        count = 0
        while count < 100:
            count += 1
            print count
            size = self.populationSize
            idx = int(round(size * self.elitismRate))
            buf = self.population[:idx]

            while (idx < size):
                if random.random() < self.mutationRate:
                    buf.append(self.tournament_selection().mutate())
                    idx += 1

                if random.random() < self.crossoverRate:
                    a, b = self.tournament_selection().crossover(self.tournament_selection())
                    buf.append(a)
                    buf.append(b)
                    idx += 2

            self.population = list(sorted(buf[:size], key=lambda x: x.fitness))

            bestChild = self.population[0]
            if self.bestParent.fitness <= bestChild.fitness:
                continue
            self.bestParent = bestChild
            print self.bestParent.fitness
        test_map.plotMovement(Chromosome.getMovements(self.bestParent.gene, self.bestParent.length))

def main():
    random.seed()
    pop = Population()
    pop.setup()
    pop.evolve()

if __name__ == "__main__":
    main()

