#!/usr/bin/env python3

class AdjacencyMap:
    def __init__(self, order):
        self.adjacents = {}
        for i in range(len(order)):
            prev = i - 2
            mid = i - 1
            self.adjacents[order[mid]] = [order[prev], order[i]]
    # returns false if this adjacency map does not produce a full, single cycle.
    def generate_order(self):
        start = 0
        order = [start, self.adjacents[start][0]]
        seen = set(order)
        while len(order) < len(self.adjacents):
            copy = self.adjacents[order[-1]][:]
            copy.remove(order[-2])
            order.append(copy[0])
            if order[-1] in seen:
                return None
            seen.add(order[-1])
            if order[0] in self.adjacents[order[-1]]:
                break
        if len(order) == len(self.adjacents):
            return order
        #print(str(len(order)) + " != " + str(len(self.adjacents)))
        return None
    def remove_edges(self, edges):
        for edge in edges:
            self.adjacents[edge[0]].remove(edge[1])
            self.adjacents[edge[1]].remove(edge[0])
    def add_edges(self, edges):
        for edge in edges:
            self.adjacents[edge[0]].append(edge[1])
            self.adjacents[edge[1]].append(edge[0])
    def apply_kmove(self, kmove):
        self.remove_edges(kmove.removals)
        self.add_edges(kmove.additions)
    def check(self):
        for point in self.adjacents:
            assert(len(self.adjacents[point]) == 2)
    def print(self):
        for point in self.adjacents:
            print(str(point) + ": " + str(self.adjacents[point]))

