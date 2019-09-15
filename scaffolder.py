#!/usr/bin/env python3

import basic
import reader
from two_opt import TwoOpt
import random_util
import sys

xy = reader.read_xy("input/berlin52.tsp")
t = TwoOpt(xy)
t.optimize()
t.tour.show(call_show = False)
print("local optimum: " + str(t.tour.tour_length()))

def generate_random_midpoint(tour):
    si, sj = random_util.random_pair(tour.n, pad = 1)
    midpoint = basic.midpoint(tour.xy, tour.node_id(si), tour.node_id(sj))
    tour.insert_new_node(midpoint)


for i in range(50):
    generate_random_midpoint(t.tour)
    t.tour.show(call_show = True, markers = "ro:")
    continue
    t.tour.randomize()
    t.optimize()
    print("local optimum: " + str(t.tour.tour_length()))



