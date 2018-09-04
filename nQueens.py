import random
import operator
import copy

fitnessNumber = 0
termination = 10000


def random_chrom(n: int) -> list:
    """
    Random chromosome generation
    :param n: The number of queens to be placed on the chess board
    :return: randomly generated chromosome.
    """
    chrom = []  # one chromosome
    j = 0
    while True:
        temp = random.randint(0, n-1)
        if temp not in chrom:
            chrom.append(temp)   # generating genes randomly for the chromosome
            j += 1
        if j == n:
            break
    chrom.append(-1)   # initialising fitness value
    return chrom


def calculatefitness(population: list, n: int) -> list:
    """
    :param population: A list of chromosomes
    :param n: The number of queens to be placed on the chessboard
    :return: The list of chromosomes with their fitness stored at the end of each chromosome
    """
    global fitnessNumber
    for i in range(0, len(population)):

        if population[i][n] == -1:  # i is one chromosome

            collision = 0
            for j in range(0, n-1):

                for k in range(j+1, n):

                    if abs(population[i][j] - population[i][k]) == abs(j-k):

                        collision = collision + 1

            population[i][n] = 1/(collision + 0.1)
            fitnessNumber += 1  # fitnessNumber is a global variable

    if fitnessNumber >= termination:  # termination is an integer initialized to 10000
        population.sort(key=operator.itemgetter(n), reverse=True)
        print(population[0])
        exit()

    return population


def population_gen(population: list, count: int, n: int) -> list:
    """
    Initial population generation
    :param population: initial population of chromosomes
    :param count: count of the generation created
    :param n: The number of queens to be placed on the chessboard
    :return: fittest two chromosomes out of random five to be sent for crossover.
    """
    if count == 1:
        for i in range(0, 100):
            chrom = random_chrom(n)
            population.append(chrom)    # generating 100 random chromosomes as initial population
            population = calculatefitness(population, n)    # calculating fitness function

    # else:
    #    new_population = population
    temp_population = []
    for i in range(0, 5):
        temp_population.append(population[random.randint(0, 99)])  # five randomly chosen chromosomes #condition on index of chromosomes selected
    temp_population.sort(key=operator.itemgetter(n), reverse=True)     # fittest two chromosomes picked out of five
    crossover_pop = []
    for i in range(0, 2):
        crossover_pop.append(temp_population[i])
    return crossover_pop


def crossover(parents: list, recomb_prob: float, n: int) -> list:
    """
    :param parents: list of chromosomes involved in crossover
    :param recomb_prob: Recombination probability
    :param n: The number of queens to be placed on the chessboard
    :return: children created by crossover
    """
    rnd = random.random()  # picking a random number between 0 and 1
    index = random.randint(0, n)
    children = []
    if rnd <= recomb_prob:
        for i in range(0, 2):
            temp_children = []
            if index == 0:
                temp_children = parents[(i+1) % 2]    # Children remain the same as parents in the opposite index
            elif index == n:
                temp_children = parents[i]  # Children remain the same as parents
            else:
                for j in range(0, index):
                    temp_children.append(parents[i][j])   # Copying genes from parent to child until position 'index'
                k = index
                j = index
                while j < n:                           # to fill the remaining genes of the child
                    val = parents[((i + 1) % 2)][k]    # genes of parents post the position 'index'
                    if val not in temp_children[0:j]:
                        temp_children.append(val)
                        j += 1
                    k = (k+1) % n
            temp_children.append(-1)
            children.append(temp_children)

        children = calculatefitness(children, n)
        return children
    return parents


def mutation(permutation: list, mutation_prob: float, n: int) -> list:
    """"
    :param permutation: chromosome post recombination
    :param mutation_prob: mutation probability
    :param n: The number of queens to be placed on the chessboard
    :return: mutated chromosome
    """
    rnd = random.random()   # picking a random number between 0 and 1
    if rnd < mutation_prob:     # checking if mutation is allowed
        loci1 = random.randint(0, n - 2)
        loci2 = random.randint(0, n - 2)    # picking two mutation points in each chromosome
        while loci2 == loci1:
            loci2 = random.randint(0, n - 2)
        result = copy.deepcopy(permutation)
        result[0][loci1], result[0][loci2] = result[0][loci2], result[0][loci1]
        result[1][loci1], result[1][loci2] = result[1][loci2], result[1][loci1]     # performing swap mutation
        return result
    return permutation  # returning unmutated population in case mutation does not occur


def selection(population: list, n: int) -> list:
    """
    :param population: chromosome population post crossover and mutation
    :param n: The number of queens to be placed on the chessboard
    :return: best hundred of the population
    """
    population.sort(key=operator.itemgetter(n), reverse=True)     # ERROR IS IN THIS LINE
    population = population[:len(population) - 2]
    return population


def main():
    n = int(input("Enter the value of n"))
    recomb_prob = float(input("Enter the value of recombination probability"))
    mutation_prob = float(input("Enter the value of mutation probability"))

    population = []
    count = 1
    while True:
        crossover_val = population_gen(population, count, n)
        crossover_pop = crossover(crossover_val, recomb_prob, n)
        children = mutation(crossover_pop, mutation_prob, n)
        i = 0
        while i != 2:
            population.append(children[i])
            i += 1
        population = selection(population, n)
        count += 1

        
main()
