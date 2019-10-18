#!/usr/bin/env python3

import basic
import reader
from tour import Tour
import random
from two_opt import TwoOpt
import merger
import sys

def sort_nearest(xy, ref_point):
    ixy = []
    for i in range(len(xy)):
        ixy.append((i, xy[i]))
    ixy.sort(key = lambda x : basic.distance(xy, x[0], ref_point))
    return [x[0] for x in ixy][1:]

def generate_nearest_map(xy):
    return [sort_nearest(xy, i) for i in range(len(xy))]

def get_nearest_unused(nearest, used):
    for n in nearest:
        if n not in used:
            used.add(n)
            return n
    assert("could not get nearest neighbor...")

def generate_tour(xy, start):
    new_order = [start]
    used = set(new_order)
    nearest = generate_nearest_map(xy)
    while len(new_order) < len(xy):
        current_nearest = nearest[new_order[-1]]
        new = get_nearest_unused(current_nearest, used)
        new_order.append(new)
    return new_order

def generate_random_tour(xy):
    return generate_tour(xy, random.randrange(len(xy)))

def cycle_tours(xy):
    o1 = TwoOpt(xy)
    order = generate_tour(xy, random.randrange(len(xy)))
    o1.tour.reset(order)
    o1.optimize()
    histogram = {}
    o2 = TwoOpt(xy)
    for i in range(1, len(xy)):
        order = generate_tour(xy, random.randrange(len(xy)))
        o2.tour.reset(order)
        o2.optimize()
        length1 = o1.tour.tour_length()
        length2 = o2.tour.tour_length()
        if not merger.merge(o1, o2.tour.node_ids) and length2 < length1:
            o1.tour.reset(o2.tour.node_ids)
            length1 = length2
        if length2 not in histogram:
            histogram[length2] = 0
        histogram[length2] += 1
        print(str(i) + " tour length: " + str(length2))
        print("best tour length after merge: " + str(length1))
    histogram_list = []
    for length in histogram:
        histogram_list.append((length, histogram[length]))
    histogram_list.sort()
    for tup in histogram_list:
        print(str(tup[0]) + ": " + str(tup[1]))

if __name__ == "__main__":
    xy = reader.read_xy("input/berlin52.tsp")
    xy = reader.read_xy("input/xqf131.tsp")
    cycle_tours(xy)
    sys.exit()
    o1 = TwoOpt(xy)
    o1.tour.reset(generate_random_tour(xy))
    o1.optimize()
    print("tour1 length: " + str(o1.tour.tour_length()))

    o2 = TwoOpt(xy)
    for i in range(1000):
        o2.tour.reset(generate_random_tour(xy))
        o2.optimize()
        new_tour_length = o2.tour.tour_length()
        print("iteration " + str(i) + " best tour length: " + str(o1.tour.tour_length()))
        print("iteration " + str(i) + " new_tour length: " + str(new_tour_length))
        if new_tour_length < o2.tour.tour_length():
            o1.tour.reset(o2.tour.node_ids)
            continue
        merger.merge(o1, o2.tour.node_ids)
    print("final tour length: " + str(o1.tour.tour_length()))
