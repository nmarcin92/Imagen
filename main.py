from PIL import Image

from logic.operators import select
from logic.shapes import Triangle, Circle
from logic.solution import Solution
from params import POPULATION_SIZE, SIZE_Y, SIZE_X, TRIANGLES_NR, CIRCLES_NR

if __name__ == "__main__":

    base = Image.open('base.bmp').resize((SIZE_X, SIZE_Y), Image.ANTIALIAS)

    population = [
        Solution([Triangle.generate() for i in range(TRIANGLES_NR)] + [Circle.generate() for i in range(CIRCLES_NR)])
        for j in range(POPULATION_SIZE)]


    res = open('res.txt', 'w')

    r_c = 0
    i = 0
    while True:
        population = select(population, base)
        i += 1
        if i == 500:
            r_c += 1
            print str(r_c) + ' result'
            population[0].generate_image().save('res' + str(r_c) + '.jpg', 'JPEG')
            for p in population:
                p.count_fitness(base)

            population = sorted(population, key=lambda p: p.fitness, reverse=True)
            res.write(str(r_c) + "\t" + str(population[0].fitness) + "\t" + str(population[POPULATION_SIZE/2].fitness) + "\t" + str(population[POPULATION_SIZE-1].fitness) + "\n")
            res.flush()
            i = 0
