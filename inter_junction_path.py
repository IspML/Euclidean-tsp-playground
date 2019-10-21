#!/usr/bin/env python3

class InterJunctionPath:
    def __init__(self, junction, removal = True, first = True):
        self.removals = []
        self.additions = []
        self.last = junction.node_id
        if removal:
            if first:
                self.removal(junction.removals[0])
            else:
                self.removal(junction.removals[1])
        else:
            if first:
                self.addition(junction.additions[0])
            else:
                self.addition(junction.additions[1])
        self.junctions = [junction.node_id] # junctions that bound this path.
        self.last_removed = removal
        self.cost = None # TODO: populate.

    def odd_edge_count(self):
        edge_count = len(self.removals) + len(self.additions)
        return edge_count % 2 == 1
    def even_edge_count(self):
        edge_count = len(self.removals) + len(self.additions)
        return edge_count % 2 == 0
    def cyclic(self):
        return self.junctions[0] == self.junctions[1]
    def removal(self, next_point):
        edge = (min(self.last, next_point), max(self.last, next_point))
        self.removals.append(edge)
        self.last = next_point
        self.last_removed = True
    def addition(self, next_point):
        edge = (min(self.last, next_point), max(self.last, next_point))
        self.additions.append(edge)
        self.last = next_point
        self.last_removed = False
    def get_edges(self, point):
        edges = []
        for edge in self.removals:
            if point in edge:
                edges.append(edge)
        for edge in self.additions:
            if point in edge:
                edges.append(edge)
        return edges

    def print(self):
        print("junction path:")
        print("\tjunctions: " + str(self.junctions))
        print("\tremovals: " + str(self.removals))
        print("\tadditions: " + str(self.additions))

    def equals(self, other):
        for j in self.junctions:
            if j in other.junctions:
                continue
            return False
        if len(self.removals) != len(other.removals):
            return False
        for r in self.removals:
            if r in other.removals:
                continue
            return False
        if len(self.additions) != len(other.additions):
            return False
        for r in self.additions:
            if r in other.additions:
                continue
            return False
        return True

    def merge(self, other, removed_junction):
        self.removals += other.removals
        self.additions += other.additions
        new_junctions = list(self.junctions)
        new_junctions += list(other.junctions)
        while removed_junction in new_junctions:
            new_junctions.remove(removed_junction)
        self.junctions = new_junctions
        assert(len(self.junctions) == 2)

    def compatible(self, other, junction):
        # common junction
        if junction not in other.junctions or junction not in self.junctions:
            return False
        edges = self.get_edges(junction)
        assert(len(edges) == 1)
        other_edges = other.get_edges(junction)
        assert(len(other_edges) == 1)
        if edges[0] in self.removals:
            return other_edges[0] in other.additions
        return other_edges[0] in other.removals

