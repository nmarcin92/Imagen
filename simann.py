import random

from PIL import Image
import math

from logic.shapes import Triangle, Circle
from logic.solution import Solution
from params import TRIANGLES_NR, CIRCLES_NR, SIZE_X, SIZE_Y

T_MAX = 100.0


def mutate_triangle(s, t):
    p = random.choice([s.p1, s.p2, s.p3])
    dx = random.gauss(-SIZE_X*t/2.0, SIZE_X * t/2.0)
    dy = random.gauss(-SIZE_Y*t/2.0, SIZE_Y * t/2.0)

    p[0] = int(round(p[0] + dx))
    p[1] = int(round(p[1] + dy))

    elem = random.randint(0, 2)
    s.color[elem] = min(max(int(round(s.color[elem] + random.gauss(0, 128 * t))), 0), 255)

    s.normalize()
    return s

def mutate_circle(s, t):
    dsx = random.gauss(-SIZE_X*t/2.0, SIZE_X * t/2.0)
    dsy = random.gauss(-SIZE_Y*t/2.0, SIZE_Y * t/2.0)
    s.s[0] += int(round(dsx))
    s.s[1] += int(round(dsy))
    size = (SIZE_X+SIZE_Y)/2.0
    s.r += int(round(random.gauss(-size*t/2.0, size*t/2.0)))
    elem = random.randint(0, 2)
    s.color[elem] = min(max(int(round(s.color[elem] + random.gauss(0, 128 * t))), 0), 255)

    s.normalize()
    return s

if __name__ == "__main__":
    base = Image.open('base.bmp').resize((SIZE_X, SIZE_Y), Image.ANTIALIAS)

    w = Solution([Triangle.generate() for i in range(TRIANGLES_NR)] + [Circle.generate() for i in range(CIRCLES_NR)])
    t = T_MAX
    alpha = 0.0001

    res = open('resim.txt', 'w')
    i = 0
    while t > 1.0e-3:
        i += 1
        w.count_fitness(base)
        w_new = Solution([])
        for s in w.shapes:
            if type(s) is Triangle:
                w_new.shapes.append(mutate_triangle(s.clone(), t))
            elif type(s) is Circle:
                w_new.shapes.append(mutate_circle(s.clone(), t))
        w_new.count_fitness(base)
        delta = w.fitness - w_new.fitness
        if delta < 0:
            w = w_new
        else:
            x = random.random()
            if x < math.exp(-delta/t):
                w = w_new
        t *= (1.0 - alpha)
        res.write(str(w.fitness) + "\n")
        res.flush()

    w.generate_image().save('sim.jpg', 'JPEG')




