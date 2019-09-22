#!/usr/bin/env python3

import reader

def distance(xy, i, j):
    dx = xy[i][0] - xy[j][0]
    dy = xy[i][1] - xy[j][1]
    return int((dx ** 2 + dy ** 2) ** 0.5 + 0.5)

def midpoint(xy, i, j):
    dx = xy[j][0] - xy[i][0]
    dy = xy[j][1] - xy[i][1]
    return (xy[i][0] + dx / 2.0, xy[i][1] + dy / 2.0)

def tour_length(xy, node_ids):
    assert(len(xy) > 1)
    assert(len(node_ids) > 1)
    n = len(xy)
    L = 0
    prev = node_ids[-1]
    for i in node_ids:
        L += distance(xy, i, prev)
        prev = i
    return L

def edges_from_order(node_ids):
    edges = set()
    prev = node_ids[-1]
    for i in node_ids:
        edge = (min(i, prev), max(i, prev))
        edges.add(edge)
        prev = i
    return edges

if __name__ == "__main__":
    xy, ii = reader.read_xy("input/berlin52.tsp")
    print(tour_length(xy, ii))
    opt = reader.read_tour("input/berlin52.opt.tour")
    print(tour_length(xy, opt))
