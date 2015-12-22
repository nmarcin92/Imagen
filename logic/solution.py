from params import SIZE_X, SIZE_Y


class Solution(object):
    def __init__(self, shapes):
        self.shapes = shapes
        self.fitness = 0.0

    def generate_image(self):
        img = [[None for x in range(SIZE_X)] for y in range(SIZE_Y)]
        for s in self.shapes:
            s.draw(img)

        return [[[0, 0, 0] if p is None else p for p in line] for line in img]

    def count_fitness(self, base):
        ind_img = self.generate_image()
        d = 0L
        for x in range(0, SIZE_X, 10):
            for y in range(0, SIZE_Y, 10):
                c_i = ind_img[y][x]
                c_b = base[y][x]
                d += (c_i[0] - c_b[0]) ** 2 + (c_i[1] - c_b[1]) ** 2 + (c_i[2] - c_b[2]) ** 2
        self.fitness = SIZE_X * SIZE_Y * (3 * (255 ** 2)) - d
