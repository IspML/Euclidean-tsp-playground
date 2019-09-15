#!/usr/bin/env python3

from two_opt import TwoOpt
import reader

xy = reader.read_xy("input/berlin52.tsp")
t = TwoOpt(xy)
t.optimize()
print("local optimum: " + str(t.tour.tour_length()))

def double_bridge(t):
    original = t.tour.node_ids[:]
    original_length = t.tour.tour_length()
    t.tour.double_bridge_perturbation()
    t.optimize()
    if original_length < t.tour.tour_length():
        t.tour.reset(original)

for i in range(50):
    double_bridge(t)
    print("local optimum: " + str(t.tour.tour_length()))



