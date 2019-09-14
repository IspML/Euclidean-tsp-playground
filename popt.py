#/usr/bin/env python3

import reader
from tour import Tour
from two_opt import TwoOpt

def popt(t, pops = 1):
    ref_length = t.tour.tour_length()
    original = t.tour.node_ids[:]

    # pop, then optimize.
    prepop = t.tour.tour_length()
    popped = []
    for _ in range(pops):
        popped += t.tour.random_pop()
        assert(t.optimize() >= 0)
    reduction = prepop - t.tour.tour_length()
    assert(reduction >= 0)
    for p in popped:
        t.tour.insert(p)
        t.optimize()
    improvement = ref_length - t.tour.tour_length()
    if improvement < 0:
        t.tour.reset(original)
    improvement = ref_length - t.tour.tour_length()
    return improvement

def sequence_popt(t, pops = 1):
    ref_length = t.tour.tour_length()
    original = t.tour.node_ids[:]

    # pop, then optimize.
    prepop = t.tour.tour_length()
    popped = t.tour.random_pop(pops)
    assert(t.optimize() >= 0)
    reduction = prepop - t.tour.tour_length()
    assert(reduction >= 0)
    for p in popped:
        t.tour.insert(p)
        t.optimize()
    improvement = ref_length - t.tour.tour_length()
    if improvement < 0:
        t.tour.reset(original)
    improvement = ref_length - t.tour.tour_length()
    return improvement

if __name__ == "__main__":
    xy = reader.read_xy("input/berlin52.tsp")
    t = TwoOpt(xy)
    t.optimize()

    for i in range(200):
        #print(sequence_popt(t, 10))
        print(popt(t, 4))
        print(t.tour.tour_length())

    print("final length: " + str(t.tour.tour_length()))

    """
    new_xy, new_node_ids = t.tour.bisect()
    new_tour = Tour(new_xy)
    new_tour.reset(new_node_ids)
    new_xy, new_node_ids = new_tour.bisect()
    t = TwoOpt(new_xy)
    t.tour.reset(new_node_ids)
    t.tour.show(call_show = True, markers = "xr:")
    t.optimize()
    """
