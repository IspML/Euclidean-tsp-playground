#!/usr/bin/env python3

import basic
import reader
from two_opt import TwoOpt
import random_util
import sys
import plot

import mst

xy = reader.read_xy("input/berlin52.tsp")
t = TwoOpt(xy)
t.optimize()
t.tour.plot()
t.tour.plot_seq()

best = t.tour.node_ids[:]
best_length = t.tour.tour_length()
print("local optimum: " + str(best_length))

points = 0

mst_edges = mst.prim(t.tour.xy)

mst_connectivity = [[]] * len(t.tour.xy)
for e in mst_edges:
    mst_connectivity[e[0]].append(e[1])
    mst_connectivity[e[1]].append(e[0])

new_edges = mst.get_new_mst_edges(t.tour, mst_edges)

plot.plot_edges(t.tour, new_edges, "g:^")
t.tour.show()

def get_mst_points(n):
    pass

for i in range(50):
    for _ in range(points):
        new_xy = get_mst_point()
        t.tour.insert_new_node(new_xy)
    t.optimize()
    for _ in range(points):
        t.tour.remove_last_xy()
    new_length = t.tour.tour_length()
    if new_length < best_length:
        t.optimize()
        best_length = t.tour.tour_length()
        best = t.tour.node_ids[:]
        print("best length: " + str(best_length))
    else:
        t.tour.reset(best)

