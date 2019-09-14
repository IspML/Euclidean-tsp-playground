#!/usr/bin/env python3

import reader
from two_opt import TwoOpt

xy = reader.read_xy("input/berlin52.tsp")
t = TwoOpt(xy)
t.optimize()
print("local optimum: " + str(t.tour.tour_length()))

for i in range(50):
    t.tour.randomize()
    t.optimize()
    print("local optimum: " + str(t.tour.tour_length()))



