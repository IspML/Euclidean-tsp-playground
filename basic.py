#!/usr/bin/env python3

import reader

def distance(xy, i, j):
    dx = xy[i][0] - xy[j][0]
    dy = xy[i][1] - xy[j][1]
    return int((dx ** 2 + dy ** 2) ** 0.5 + 0.5)

def tour_length(xy, ii):
    assert(len(xy) > 1)
    assert(len(ii) > 1)
    n = len(xy)
    L = 0
    j = ii[-1]
    for i in ii:
        L += distance(xy, i, j)
        j = i
    return L

if __name__ == "__main__":
    xy, ii = reader.read_xy("input/berlin52.tsp")
    print(tour_length(xy, ii))
    opt = reader.read_tour("input/berlin52.opt.tour")
    print(tour_length(xy, opt))
