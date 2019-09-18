#!/usr/bin/env python3

import reader
from two_opt import TwoOpt

xy = reader.read_xy("input/berlin52.tsp")
xy = reader.read_xy("input/xqf131.tsp")
t = TwoOpt(xy)
t.optimize()
print("local optimum: " + str(t.tour.tour_length()))

best_length = t.tour.tour_length()
best = t.tour.node_ids[:]

for i in range(50):
    print(i)
    t.tour.randomize()
    t.optimize()
    new_length = t.tour.tour_length()
    if new_length < best_length:
        best = t.tour.node_ids[:]
        best_length = new_length
        print("best length: " + str(best_length))
    else:
        t.tour.reset(best)


