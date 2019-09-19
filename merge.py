#!/usr/bin/env python3

# tour-merging strategies aimed at identifying and preserving improved sections of tours
# that would otherwise be thrown away if the overall tour length is worse.

import inserter
import deleter
import reader
from two_opt import TwoOpt
import popt

def edge_diff(tour1, tour2):
    edges1 = tour1.tour.edges()
    edges2 = tour2.tour.edges()
    return edges1.symmetric_difference(edges2)

if __name__ == "__main__":
    xy = reader.read_xy("input/berlin52.tsp")
    t1 = TwoOpt(xy)
    t1.optimize()
    deleter.deleter(t1)
    print("tour1 length: " + str(t1.tour.tour_length()))

    t2 = TwoOpt(xy)
    t2.optimize()
    deleter.deleter(t2)
    for i in range(10):
        popt.sequence_popt(t2, 3)
    print("tour2 length: " + str(t2.tour.tour_length()))

    diff = edge_diff(t1, t2)
    print("diff edges: " + str(len(diff)))

    t1.tour.plot(markers="x:r")
    t2.tour.plot(markers="x:b")
    t2.tour.show()


