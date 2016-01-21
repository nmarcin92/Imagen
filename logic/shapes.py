import random

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

    def normalize(self):
        xs = []
        for p in [self.p1, self.p2, self.p3]:
            p[0] = max(min(p[0], SIZE_X - 1), 0)
            p[1] = max(min(p[1], SIZE_Y - 1), 0)

            while p[0] in xs:
                p[0] += 1 if p[0] < SIZE_X - 3 else -1

            xs.append(p[0])

    def mutate_shape(self):
        p = random.choice([self.p1, self.p2, self.p3])
        dx = random.gauss(-SIZE_X*MUTATION_SIZE/2.0, SIZE_X * MUTATION_SIZE/2.0)
        dy = random.gauss(-SIZE_Y*MUTATION_SIZE/2.0, SIZE_Y * MUTATION_SIZE/2.0)

        p[0] = int(round(p[0] + dx))
        p[1] = int(round(p[1] + dy))

        self.normalize()

    def clone(self):
        return Triangle(list(self.p1), list(self.p2), list(self.p3), list(self.color))


class Circle(Shape):

    @staticmethod
    def generate():
        s = [random.randint(SIZE_X * INITIAL_SHAPES_SIZE, SIZE_X*(1-INITIAL_SHAPES_SIZE)-1),
             random.randint(SIZE_Y * INITIAL_SHAPES_SIZE, SIZE_Y*(1-INITIAL_SHAPES_SIZE)-1)]
        r = (SIZE_X + SIZE_Y) / 2.0 * INITIAL_SHAPES_SIZE
        color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

        c = Circle(s, r, color)
        c.normalize()
        return c

    def __init__(self, s, r, color):
        super(Circle, self).__init__(color)
        self.s = s
        self.r = r

    def mutate_shape(self):
        # center point mutation
        if bool(random.getrandbits(1)):
            dsx = random.gauss(-SIZE_X*MUTATION_SIZE/2.0, SIZE_X * MUTATION_SIZE/2.0)
            dsy = random.gauss(-SIZE_Y*MUTATION_SIZE/2.0, SIZE_Y * MUTATION_SIZE/2.0)
            self.s[0] += int(round(dsx))
            self.s[1] += int(round(dsy))

        #radius mutation
        else:
            size = (SIZE_X+SIZE_Y)/2.0
            self.r += int(round(random.gauss(-size*MUTATION_SIZE/2.0, size*MUTATION_SIZE/2.0)))

        self.normalize()

    def normalize(self):
        s = self.s
        r = self.r
        while s[0]-r < 0:
            s[0] += 1
        while s[0]+r > SIZE_X-1:
            s[0] -= 1
        while s[1]-r < 0:
            s[1] += 1
        while s[1]+r > SIZE_Y-1:
            s[1] -= 1

    def clone(self):
        return Circle(list(self.s), self.r, list(self.color))
