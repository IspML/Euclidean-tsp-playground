#!/usr/bin/env python3

import basic
import reader
from two_opt import TwoOpt
import random_util
import sys
from box import Box
import inserter

def deleter(t, deletions = 1):
    best = t.tour.node_ids[:]
    best_length = t.tour.tour_length()
    print("local optimum: " + str(best_length))
    improved = True
    while improved:
        improved = False
        for si in range(t.tour.n):
            popped = []
            for d in range(deletions):
                popped.append(t.tour.pop(si + d))
            t.optimize()
            for p in popped:
                t.tour.insert(p)
            t.optimize()
            t.tour.validate()
            new_length = t.tour.tour_length()
            if new_length < best_length:
                best_length = new_length
                best = t.tour.node_ids[:]
                t.tour.validate()
                print("best length: " + str(best_length))
                improved = True
            else:
                t.tour.reset(best)
                t.tour.validate()

if __name__ == "__main__":
    xy = reader.read_xy("input/berlin52.tsp")
    t = TwoOpt(xy)
    t.optimize()

    deleter(t)
    #inserter.inserter(t)

    t.tour.validate()
    print("final length: " + str(t.tour.tour_length()))
    t.tour.plot()
    t.tour.show()

