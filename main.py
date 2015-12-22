import numpy
from PIL import Image

from imageproc import get_image_array
from logic.operators import select
from logic.shapes import Triangle
from logic.solution import Solution
from params import SHAPES_NR, POPULATION_SIZE

if __name__ == "__main__":
    base = get_image_array("sam.jpg")
    population = [Solution([Triangle.generate() for i in range(SHAPES_NR)]) for j in range(POPULATION_SIZE)]

    for i in range(100):
        population = select(population, base)
        Image.fromarray(numpy.asarray(population[0].generate_image()), 'RGB').show()
        raw_input()