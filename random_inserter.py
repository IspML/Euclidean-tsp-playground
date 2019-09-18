#!/usr/bin/env python3

import basic
import reader
from two_opt import TwoOpt
import random_util
import sys
from box import Box

xy = reader.read_xy("input/berlin52.tsp")
t = TwoOpt(xy)
t.optimize()
t.tour.plot()

def generate_random_midpoint(tour):
    si, sj = random_util.random_pair(tour.n, pad = 1)
    midpoint = basic.midpoint(tour.xy, tour.node_id(si), tour.node_id(sj))
    tour.insert_new_node(midpoint)

best = t.tour.node_ids[:]
best_length = t.tour.tour_length()
print("local optimum: " + str(best_length))
b = Box(t.tour.xy)

points = 1

for i in range(50):
    for p in range(points):
        t.tour.insert_new_node(b.random_xy())
    t.optimize()
    for p in range(points):
        t.tour.remove_last_xy()
    new_length = t.tour.tour_length()
    if new_length < best_length:
        t.optimize()
        best_length = t.tour.tour_length()
        best = t.tour.node_ids[:]
        print("best length: " + str(best_length))
    else:
        t.tour.reset(best)

