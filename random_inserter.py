#!/usr/bin/env python3

import basic
import reader
from two_opt import TwoOpt
import random_util
import sys
from box import Box

def generate_random_midpoint(tour):
    si, sj = random_util.random_pair(tour.n, pad = 1)
    midpoint = basic.midpoint(tour.xy, tour.node_id(si), tour.node_id(sj))
    tour.insert_new_node(midpoint)

if __name__ == "__main__":
    xy = reader.read_xy("input/berlin52.tsp")
    xy = reader.read_xy("input/xqf131.tsp")
    t = TwoOpt(xy)
    t.optimize()
    t.tour.plot()

    best = t.tour.node_ids[:]
    best_length = t.tour.tour_length()
    print("local optimum: " + str(best_length))
    b = Box(t.tour.xy)

    points = 30

    for i in range(1000):
        print("iteration: " + str(i))
        #t.tour.plot()
        for p in range(points):
            t.tour.insert_new_node(b.random_xy())
        #t.tour.plot(":rx")
        #t.tour.show()
        t.optimize()
        for p in range(points):
            t.tour.remove_last_xy()
        t.optimize()
        new_length = t.tour.tour_length()
        if new_length < best_length:
            best_length = t.tour.tour_length()
            best = t.tour.node_ids[:]
            print("best length: " + str(best_length))
        else:
            t.tour.reset(best)

