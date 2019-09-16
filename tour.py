#!/usr/bin/env python3

import reader
import basic
import random
import random_util
import math
from matplotlib import pyplot as plt

class Tour:
    def __init__(self, xy):
        self.xy = xy
        self.reset([x for x in range(len(xy))])
    def reset(self, node_ids):
        self.node_ids = node_ids
        self.n = len(node_ids)
    def randomize(self):
        random.shuffle(self.node_ids)
    def random_pop(self, num = 1):
        popped = []
        si = random.randrange(self.n)
        while num > 0:
            if si == self.n:
                si = 0
            popped.append(self.node_ids.pop(si))
            num -= 1
            self.n -= 1
        return popped
    def remove_last_xy(self):
        i = len(self.xy) - 1
        self.node_ids.remove(i)
        self.n -= 1
        self.xy.pop()
        self.check()
    def insert_new_node(self, xy):
        i = len(self.xy)
        self.xy.append(xy)
        self.insert(i)
    def insert(self, i):
        min_si = None
        min_cost = math.inf
        for si in range(self.n):
            cost = basic.distance(self.xy, self.node_id(si), i)
            cost += basic.distance(self.xy, self.node_id(si + 1), i)
            cost -= self.next_length(si)
            #print(cost)
            assert(cost >= -1)
            if cost < min_cost:
                min_cost = cost
                min_si = si
        self.node_ids.insert(min_si + 1, i)
        self.n += 1
    def bisect(self):
        new_node_ids = []
        new_xy = self.xy[:]
        for si in range(self.n):
            i = self.node_ids[si]
            j = self.next_id(si)
            new_node_ids.append(i)
            length = self.next_length(si)
            if length > 1:
                new_node_ids.append(len(new_xy))
                new_xy.append(basic.midpoint(self.xy, i, j))
        return new_xy, new_node_ids

    # checks for index validity.
    def node_id(self, sequence_id):
        if sequence_id < 0:
            sequence_id += self.n
        elif sequence_id >= self.n:
            sequence_id -= self.n
        return self.node_ids[sequence_id]
    def next_id(self, sequence_id):
        return self.node_id(sequence_id + 1)
    def prev_id(self, sequence_id):
        return self.node_id(sequence_id - 1)
    def next_length(self, si):
        assert(si < self.n and si >= 0)
        return basic.distance(self.xy, self.node_id(si), self.node_id(si + 1))
    def length(self, si, sj):
        i = self.node_id(si)
        j = self.node_id(sj)
        return basic.distance(self.xy, i, j)
    def swap(self, si, sj):
        si, sj = min(si, sj), max(si, sj)
        assert(sj - si > 1)
        self.node_ids[si + 1 : sj + 1] = self.node_ids[sj : si : -1]
        self.check()
    def check(self):
        seen = set()
        for n in self.node_ids:
            assert(n not in seen)
            seen.add(n)
        assert(len(self.node_ids) == self.n)
    def double_bridge_perturbation(self):
        # first make two cycles, then merge.
        si = random.randrange(self.n)
        sj = random_util.restricted(self.n, si + 3, 5)
        si, sj = (min(si, sj), max(si, sj))
        new_cycle = self.node_ids[si + 1 : sj + 1]
        # now pick new location in each cycle for merge locations.
        new_si = random.randrange(len(new_cycle))
        # rearrange new_cycle so that it can be spliced back.
        if new_si + 1 < len(new_cycle):
            new_cycle = new_cycle[new_si + 1 : len(new_cycle)] + new_cycle[ : new_si + 1]
        self.node_ids[si + 1 : sj + 1] = []
        si = random.randrange(len(self.node_ids))
        self.node_ids[si : si + 1] = [self.node_ids[si]] + new_cycle
        assert(len(self.node_ids) == self.n)
    def tour_length(self):
        total = 0
        for si in range(self.n):
            total += self.next_length(si)
        return total
    def plot(self, markers = "x-"):
        xy = [self.xy[self.node_id(i)] for i in range(self.n)]
        x = [x_[0] for x_ in xy]
        x.append(x[0])
        y = [x_[1] for x_ in xy]
        y.append(y[0])
        plt.plot(x, y, markers)
    def plot_seq(self):
        for si in range(self.n):
            plt.text(self.xy[self.node_id(si)][0], self.xy[self.node_id(si)][1], str(si) + ", " + str(self.node_id(si)))
    def show(self):
        plt.show()

    def connectivity(self):
        return [(self.node_id(i - 1), self.node_id(i + 1)) for i in range(self.n)]

if __name__ == "__main__":
    xy = reader.read_xy("input/berlin52.tsp")
    tour = Tour(xy)
    opt = reader.read_tour("input/berlin52.opt.tour")
    tour.reset(opt)
    print("optimal tour length: " + str(tour.tour_length()))
