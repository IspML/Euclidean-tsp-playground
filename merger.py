#!/usr/bin/env python3

# tour-merging strategies aimed at identifying and preserving improved sections of tours
# that would otherwise be thrown away if the overall tour length is worse.

import inserter
import deleter
import reader
from two_opt import TwoOpt
import popt
import math
from itertools import combinations
import basic
from matplotlib import pyplot as plt

def count_num_tries(n):
    combos = 0
    nf = math.factorial(n)
    for r in range(n - 3, n - 1):
        combos += nf / math.factorial(n - r) / math.factorial(r)
    print("combos: " + str(combos))

def edge_diff(tour, other):
    edges = tour.edges()
    other_edges = other.edges()
    diff = edges - other_edges
    other_diff = other_edges - edges
    assert(len(diff) == len(other_diff))
    return diff, other_diff

def match_sets(edges, other_edges):
    if len(other_edges) < len(edges):
        return None
    points = set()
    for e in edges:
        points.add(e[0])
        points.add(e[1])
    compatible_edges = []
    compatible_points = set()
    for e in other_edges:
        if e[0] in points and e[1] in points:
            compatible_edges.append(e)
            compatible_points.add(e[0])
            compatible_points.add(e[1])
    if len(compatible_edges) < len(edges):
        return None
    if compatible_points != points:
        return None
    if len(compatible_edges) != len(edges):
        cc = combinations(compatible_edges, len(compatible_edges) - 1)
        for c in cc:
            compatible_points = set()
            for e in c:
                compatible_points.add(c[0])
                compatible_points.add(c[1])
            if compatible_points == points:
                return c
        return None
    assert(len(compatible_edges) == len(edges))
    return compatible_edges

def edge_cost(xy, edge):
    return basic.distance(xy, edge[0], edge[1])

def calculate_gain(xy, export_edges, import_edges):
    gain = 0
    for e in export_edges:
        gain += edge_cost(xy, e)
    for e in import_edges:
        gain -= edge_cost(xy, e)
    return gain

def try_n_set(xy, edges, other_edges, n):
    assert(len(edges) == len(other_edges))
    cc = combinations(edges, n)
    best_export = None
    best_import = None
    best_gain = -math.inf
    for c in cc:
        matched_set = match_sets(c, other_edges)
        if matched_set:
            gain = calculate_gain(xy, c, matched_set)
            if gain > best_gain:
                best_export = c
                best_import = matched_set
                best_gain = gain
    if best_gain <= 0:
        return None
    return best_gain, best_export, best_import

def try_all_sets(xy, edges, other_edges):
    assert(len(edges) == len(other_edges))
    candidates = []
    for i in range(3, len(edges) + 1):
        candidate = try_n_set(xy, edges, other_edges, i)
        if candidate:
            candidates.append(candidate)
    candidates.sort(reverse = True)
    return candidates

def list_from_adjacents(adjacents):
    start = 0
    ordered = [start, adjacents[start][0]]
    while len(ordered) < len(adjacents):
        nxt = adjacents[ordered[-1]][:]
        nxt.remove(ordered[-2])
        ordered.append(nxt[0])
        if ordered[-1] == start:
            return None
    return ordered

def plot_connectivity(xy, cc):
    for i in range(len(cc)):
        c = cc[i]
        for j in c:
            x = [xy[i][0], xy[j][0]]
            y = [xy[i][1], xy[j][1]]
            plt.plot(x, y, "x-")

def feasible(tour, export_edges, import_edges):
    cc = tour.connectivity()
    for e in export_edges:
        cc[e[0]].remove(e[1])
        cc[e[1]].remove(e[0])
    for e in import_edges:
        cc[e[0]].append(e[1])
        if len(cc[e[0]]) > 2:
            return None
        cc[e[1]].append(e[0])
        if len(cc[e[1]]) > 2:
            return None
        cc[e[0]].sort()
        cc[e[1]].sort()
    for c in cc:
        if len(c) != 2:
            return None
    return list_from_adjacents(cc)

if __name__ == "__main__":
    xy = reader.read_xy("input/berlin52.tsp")
    t1 = TwoOpt(xy)
    t1.optimize()
    deleter.deleter(t1)
    print("tour1 length: " + str(t1.tour.tour_length()))

    t2 = TwoOpt(xy)
    t2.tour.reset(t1.tour.node_ids)
    for i in range(50):
        t2.tour.reset(t1.tour.node_ids)
        improvement = popt.sequence_popt(t2, 10)
        print("new_tour length: " + str(t2.tour.tour_length()))
        exportable, importable = edge_diff(t1.tour, t2.tour)
        candidates = try_all_sets(xy, exportable, importable)
        for c in candidates:
            node_ids = feasible(t1.tour, c[1], c[2])
            if node_ids:
                t1.tour.reset(node_ids)
                t1.tour.validate()
                print("improved merged length: " + str(t1.tour.tour_length()))
                t1.optimize()
                print("post-merge hill climb: " + str(t1.tour.tour_length()))
                break

        """
        t1.tour.plot(markers="x:r")
        t2.tour.plot(markers="x:b")
        t2.tour.show()
        """
    print("final tour length: " + str(t1.tour.tour_length()))

