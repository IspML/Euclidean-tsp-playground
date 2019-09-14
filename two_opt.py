#/usr/bin/env python3

import reader
from tour import Tour

class TwoOpt:
    def __init__(self, xy):
        self.tour = Tour(xy)
    def sequence(self, start = 0):
        return range(start, self.tour.n)
    def improve_once(self):
        for si in self.sequence():
            igain = self.tour.next_length(si)
            for sj in self.sequence(si + 2):
                jgain = self.tour.next_length(sj)
                cost = self.tour.length(si, sj) + self.tour.length(si + 1, sj + 1)
                improvement = igain + jgain - cost
                if improvement > 0:
                    self.tour.swap(si, sj)
                    return improvement
        return 0
    def optimize(self):
        original = self.tour.tour_length()
        while self.improve_once() > 0:
            pass
        optimized = self.tour.tour_length()
        improvement = original - optimized
        assert(improvement >= 0)
        return improvement

def popt(t):
    ref_length = t.tour.tour_length()
    original = t.tour.node_ids[:]
    popped = t.tour.random_pop()
    pre_opt = t.tour.tour_length()
    improvement = t.optimize()
    if improvement > 0:
        t.tour.insert(popped)
        t.optimize()
        improvement = ref_length - t.tour.tour_length()
        if improvement > 0:
            return improvement
    t.tour.reset(original)
    return improvement


if __name__ == "__main__":
    xy = reader.read_xy("input/berlin52.tsp")
    t = TwoOpt(xy)
    t.optimize()
    t.tour.show(call_show = False)

    for i in range(200):
        print(popt(t))

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
