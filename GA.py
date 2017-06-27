import random
import sys

geneSet = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!.,"
target = "Hi, my name is Jake Si! I like apples."


class Chromosome:

    def __init__(self, gene, generation=0):
        self.gene = gene
        self.fitness = Chromosome.update_fitness(gene)
        self.generation = generation

    def crossover(self, mate):
        '''
        Two point crossover
        '''
        generation = max(self.generation, mate.generation)
        index1 = random.randint(1, len(target) - 2)
        index2 = random.randint(1, len(target) - 2)
        if index1 > index2:
            index1, index2 = index2, index1
        child1 = self.gene[:index1] + \
            mate.gene[index1:index2] + self.gene[index2:]
        child2 = mate.gene[:index1] + \
            self.gene[index1:index2] + mate.gene[index2:]
        # print parent1, parent2 ,child1, index
        return Chromosome(child1, generation + 1), Chromosome(child2, generation + 1)

    def mutate(self):
        '''
        Random index mutation
        '''
        index = random.randrange(0, len(self.gene))
        childGenes = list(self.gene)
        newGene, alternate = random.sample(geneSet, 2)
        childGenes[index] = alternate if newGene == childGenes[
            index] else newGene
        return Chromosome(''.join(childGenes), self.generation + 1)

    @staticmethod
    def update_fitness(gene):
        '''
        The difference between each letter's ASCII value from the target
        '''
        sum = 0
        for expected, actual in zip(target, gene):
            sum += abs(ord(actual) - ord(expected))
        return sum

    @staticmethod
    def gen_random():
        genes = []
        while len(genes) < len(target):
            sampleSize = min(len(target) - len(genes), len(geneSet))
            genes.extend(random.sample(geneSet, sampleSize))
        return Chromosome(''.join(genes))

class Population:

    def __init__(self, tournamentSize=3, mutationRate=0.1, crossoverRate=0.9, elitismRate=0.1, populationSize=2000):
        self.population = []
        self.tournamentSize = tournamentSize
        self.mutationRate = mutationRate
        self.crossoverRate = crossoverRate
        self.elitismRate = elitismRate
        self.populationSize = populationSize
        self.bestParent = None

    def display(self, guess):
        print("{0}\t\t{1}\t{2}".format(guess.gene, guess.fitness, guess.generation))

    def generate_population(self):
        for i in range(0, self.populationSize):
            self.population.append(Chromosome.gen_random())


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
        self.bestParent = self.population[0]
        self.display(self.bestParent)

    def evolve(self):
        while True:
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
            self.display(bestChild)
            if bestChild.fitness <= 0:
                return
            self.bestParent = bestChild

def main():
    random.seed()
    pop = Population()
    pop.setup()
    pop.evolve()

if __name__ == "__main__":
    main()

