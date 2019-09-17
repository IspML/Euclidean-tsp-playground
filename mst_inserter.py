#!/usr/bin/env python3

import basic
import reader
from two_opt import TwoOpt
import random_util
import sys
import plot
from tour import Tour
import random

import mst

xy = reader.read_xy("input/berlin52.tsp")
t = TwoOpt(xy)
t.optimize()

best = t.tour.node_ids[:]
best_length = t.tour.tour_length()
print("local optimum: " + str(best_length))

points = 0

mst_edges = mst.prim(t.tour.xy)

mst_connectivity = [[]] * len(t.tour.xy)
for e in mst_edges:
    mst_connectivity[e[0]].append(e[1])
    mst_connectivity[e[1]].append(e[0])

simultaneous_edges = 10

for i in range(50):
    print("iteration: " + str(i))
    new_edges = mst.get_new_mst_edges(t.tour, mst_edges)
    improved = False
    ee = random.sample(new_edges, simultaneous_edges)
    for e in ee:
        m = basic.midpoint(xy, e[0], e[1])
        t.tour.insert_new_node(m)
    t.optimize()
    for _ in ee:
        t.tour.remove_last_xy()
    t.optimize()
    new_length = t.tour.tour_length()
    if new_length < best_length:
        best_length = new_length
        best = t.tour.node_ids[:]
        print("best length: " + str(best_length))
        improved = True
    else:
        t.tour.reset(best)
    if not improved:
        opt_tour = Tour(xy)
        opt = reader.read_tour("input/berlin52.opt.tour")
        opt_tour.reset(opt)
        opt_tour.plot()
        #t.tour.plot()
        plot.plot_edges(t.tour, new_edges, "g:^")
        t.tour.show()

