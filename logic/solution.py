from PIL import Image
from PIL import ImageDraw

from logic.shapes import Triangle, Circle
from params import SIZE_X, SIZE_Y

class Solution(object):

    def __init__(self, shapes):
        self.shapes = shapes
        self.fitness = 0.0

    def generate_image(self):
        # img = [[None for x in range(SIZE_X)] for y in range(SIZE_Y)]
        # for s in self.shapes:
        #     s.draw(img)
        #
        # return [[[0, 0, 0] if p is None else p for p in line] for line in img]

        im = Image.new('RGB', (SIZE_X, SIZE_Y), 'white')
        draw = ImageDraw.Draw(im)
        for s in self.shapes:
            if type(s) is Triangle:
                draw.polygon(s.p1+s.p2+s.p3, fill=tuple(s.color))
            elif type(s) is Circle:
                draw.ellipse((s.s[0]-s.r,s.s[1]-s.r,s.s[0]+s.r,s.s[1]+s.r),fill=tuple(s.color))

        return im

    def count_fitness(self, base):
        ind_img = self.generate_image()
        d = 0L
        for x in range(0, SIZE_X, 10):
            for y in range(0, SIZE_Y, 10):
                c_i = ind_img.getpixel((x,y))
                c_b = base.getpixel((x,y))
                d += (c_i[0] - c_b[0]) ** 2 + (c_i[1] - c_b[1]) ** 2 + (c_i[2] - c_b[2]) ** 2
        self.fitness = SIZE_X * SIZE_Y * (3 * (255 ** 2)) - d
