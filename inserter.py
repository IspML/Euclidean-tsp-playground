#!/usr/bin/env python3

import basic
import reader
from two_opt import TwoOpt
import random_util
import sys
from box import Box

def inserter(t):
    best = t.tour.node_ids[:]
    best_length = t.tour.tour_length()
    print("local optimum: " + str(best_length))
    improved = True
    while improved:
        improved = False
        for si in range(t.tour.n):
            for sj in range(si + 2, t.tour.n):
                t.tour.insert_new_node(t.tour.midpoint(si, sj))
                t.optimize()
                t.tour.remove_last_xy()
                new_length = t.tour.tour_length()
                if new_length < best_length:
                    t.optimize()
                    best_length = t.tour.tour_length()
                    best = t.tour.node_ids[:]
                    print("best length: " + str(best_length))
                    improved = True
                else:
                    t.tour.reset(best)

if __name__ == "__main__":
    xy = reader.read_xy("input/berlin52.tsp")
    t = TwoOpt(xy)
    t.optimize()
    t.tour.plot()

    inserter(t)


    t.tour.validate()
    print("final length: " + str(t.tour.tour_length()))
    t.tour.plot()
    t.tour.show()

