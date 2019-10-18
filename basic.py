#!/usr/bin/env python3

import reader


def distance(xy, i, j):
    dx = xy[i][0] - xy[j][0]
    dy = xy[i][1] - xy[j][1]
    return int((dx ** 2 + dy ** 2) ** 0.5 + 0.5)
def edge_cost(xy, edge):
    return distance(xy, edge[0], edge[1])
def edge_cost_sum(xy, edges):
    total = 0
    for e in edges:
        total += edge_cost(xy, e)
    return total

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

def write_edges(edges, output_file_path):
    with open(output_file_path, "w") as f:
        for e in edges:
            e = [str(x) for x in e]
            f.write(" ".join(e) + "\n")
def write_walk_edges(points, output_file_path):
    with open(output_file_path, "w") as f:
        for i in range(len(points) - 1):
            f.write(" ".join([str(points[i]), str(points[i + 1])]) + "\n")

if __name__ == "__main__":
    xy, ii = reader.read_xy("input/berlin52.tsp")
    print(tour_length(xy, ii))
    opt = reader.read_tour("input/berlin52.opt.tour")
    print(tour_length(xy, opt))


