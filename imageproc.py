from PIL import Image

from params import SIZE_Y, SIZE_X


def get_image_array(path):
    image = Image.open(path)
    imgdata = list(image.resize((SIZE_X, SIZE_Y), Image.ANTIALIAS).getdata())
    return [imgdata[y * SIZE_X:(y + 1) * SIZE_X] for y in range(SIZE_Y)]
