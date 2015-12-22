import random

from logic.utils import count_line, line_y, merge_lists
from params import SIZE_X, MUTATION_SIZE, SIZE_Y, INITIAL_SHAPES_SIZE


class Shape(object):
    def __init__(self, color):
        self.color = color

    def mutate_color(self):
        elem = random.randint(0, 2)
        self.color[elem] = min(max(int(round(self.color[elem] + random.gauss(0, 128 * MUTATION_SIZE))), 0), 255)


class Triangle(Shape):
    @staticmethod
    def get_random_vector(p):
        return [int(round(random.gauss(p[0], SIZE_X * INITIAL_SHAPES_SIZE))),
                int(round(random.gauss(p[1], SIZE_Y * INITIAL_SHAPES_SIZE)))]

    @staticmethod
    def generate():
        p = [random.randint(0, SIZE_X - 1), random.randint(0, SIZE_Y - 1)]
        p1, p2, p3 = Triangle.get_random_vector(p), Triangle.get_random_vector(p), Triangle.get_random_vector(p)
        color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
        return Triangle(p1, p2, p3, color)

    def __init__(self, p1, p2, p3, color):
        super(Triangle, self).__init__(color)
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.left_x, self.middle_x, self.right_x = -1, -1, -1
        self.trailing_edge, self.left_edge, self.right_edge = None, None, None
        self.traverse_dir = None
        self.update_traverse_params()

    def update_traverse_params(self):
        self.normalize()
        points = sorted([self.p1, self.p2, self.p3], key=lambda p: p[0])
        self.left_x = points[0][0]
        self.middle_x = points[1][0]
        self.right_x = points[2][0]

        self.trailing_edge = count_line(points[0], points[2])
        self.left_edge = count_line(points[0], points[1])
        self.right_edge = count_line(points[1], points[2])

        self.traverse_dir = 1 if self.left_edge[0] > self.trailing_edge[0] else -1

    def normalize(self):
        xs = []
        for p in [self.p1, self.p2, self.p3]:
            p[0] = max(min(p[0], SIZE_X - 1), 0)
            p[1] = max(min(p[1], SIZE_Y - 1), 0)

            while p[0] in xs:
                p[0] += 1 if p[0] < SIZE_X - 3 else -1

            xs.append(p[0])

    def count_traverse_direction(self):
        return 1 if self.left_edge[0] > self.trailing_edge[0] else -1

    def draw(self, image_array):
        for x in range(self.left_x, self.right_x + 1):
            bound_edge = self.left_edge if x <= self.middle_x else self.right_edge
            for y in range(line_y(self.trailing_edge, x), line_y(bound_edge, x), self.traverse_dir):
                image_array[y][x] = self.color_pixel(image_array[y][x])

    def color_pixel(self, old_color):
        if old_color is None:
            return self.color
        else:
            return merge_lists(old_color, self.color, lambda c1, c2: int(round((c1 + c2) / 2.0)))

    def mutate_shape(self):
        p = random.choice([self.p1, self.p2, self.p3])
        dx = random.gauss(0, SIZE_X * MUTATION_SIZE)
        dy = random.gauss(0, SIZE_Y * MUTATION_SIZE)

        p[0] = int(round(p[0] + dx))
        p[1] = int(round(p[1] + dy))

        self.update_traverse_params()

    def clone(self):
        return Triangle(list(self.p1), list(self.p2), list(self.p3), list(self.color))

