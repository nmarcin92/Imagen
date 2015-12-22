import random

from logic.solution import Solution
from params import SHAPES_NR, MUTATION_PROBABILTY, POPULATION_SIZE, PARENTS_SURVIVAL, SIZE_Y, SIZE_X


def cross_over(p1, p2):
    child = Solution([])
    for i in range(SHAPES_NR):
        if bool(random.getrandbits(1)):
            child.shapes.append(p1.shapes[i].clone())
        else:
            child.shapes.append(p2.shapes[i].clone())
    return child


def mutate(ind):
    for s in ind.shapes:
        if random.random() < MUTATION_PROBABILTY:
            if random.randint(0, 3) == 0:
                s.mutate_color()
            else:
                s.mutate_shape()
    return ind


def select(population, base):
    for p in population:
        p.count_fitness(base)

    population = sorted(population, key=lambda p: p.fitness, reverse=True)

    min_fitness = min([ind.fitness for ind in population]) - 1
    fitness_sum = sum([ind.fitness - min_fitness for ind in population])
    roulette = [[ind, 0] for ind in population]
    acc = 0.0
    for r in roulette:
        norm_fitness = float(r[0].fitness - min_fitness) / fitness_sum
        acc += norm_fitness
        r[1] = acc

    abc = 1
    print "$ current best fitness: " + str(
        (int(round(100.0 * population[0].fitness) / float(
            SIZE_X * SIZE_Y * (3 * (255 ** 2)))))) + " value:" + str(population[0].fitness)

    parents_survived = int(round(float(POPULATION_SIZE) * PARENTS_SURVIVAL))
    new_population = population[:parents_survived]

    for i in range((POPULATION_SIZE - parents_survived) / 2):
        drawn = random.random()
        father = next(r for r in roulette if r[1] >= drawn)[0]

        drawn = random.random()
        mother = next(r for r in roulette if r[1] >= drawn)[0]

        new_population.append(mutate(cross_over(father, mother)))
        new_population.append(mutate(cross_over(father, mother)))
        if len(new_population) == POPULATION_SIZE - 1:
            new_population.append(mutate(cross_over(father, mother)))

    return new_population
