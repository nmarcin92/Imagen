def count_line(p1, p2):
    a = float(p2[1] - p1[1]) / (p2[0] - p1[0])
    b = - a * p1[0] + p1[1]
    return a, b


def line_y(line, x):
    return int(round(line[0] * x + line[1]))


def merge_lists(t1, t2, function):
    return map(lambda e: function(e[0], e[1]), zip(t1, t2))


def sum_lists(t1, t2):
    return merge_lists(t1, t2, lambda x1, x2: x1 + x2)
