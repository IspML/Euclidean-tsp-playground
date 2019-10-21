#!/usr/bin/env python3

# Breaks a k-move into disjoint sets of smaller k-moves.
# Also determines if the smaller k-moves are atomic.

from kmove import KMove

class Disjoiner:
    def __init__(self, removals, additions):
        self.removed_edges = list(tuple(removals))
        self.added_edges = list(tuple(additions))
        self.kmoves = []
        self.make_disjoint()
    def extract_adjacent_edges(self, points, edges):
        removed = []
        for edge in edges:
            if edge[0] in points or edge[1] in points:
                removed.append(edge)
                points.update(edge)
        for r in removed:
            edges.remove(r)
        return removed
    def pop_edge_set(self):
        disjoint_removals = []
        disjoint_additions = []
        points = set(self.removed_edges[-1])
        disjoint_removals += self.extract_adjacent_edges(points, self.removed_edges)
        disjoint_additions += self.extract_adjacent_edges(points, self.added_edges)
        while True:
            removed = self.extract_adjacent_edges(points, self.removed_edges)
            if not removed:
                break
            disjoint_removals += removed
            removed = self.extract_adjacent_edges(points, self.added_edges)
            if not removed:
                break
            disjoint_additions += removed
        self.kmoves.append(KMove(disjoint_removals, disjoint_additions))
    def make_disjoint(self):
        self.pop_edge_set()
        while self.removed_edges:
            self.pop_edge_set()
        assert(not self.added_edges)

    def independent_move(self, move):
        frequencies = {}
        for edge in move[0]:
            for point in edge:
                if point not in frequencies:
                    frequencies[point] = 0
                frequencies[point] += 1
                if frequencies[point] > 1:
                    return False
        return True
    def get_independent_moves(self, removals, additions):
        independent_moves = []
        new_removals = set(removals)
        new_additions = set(additions)
        for move in self.kmoves:
            if self.independent_move(move):
                independent_moves.append((move[0], move[1]))
                for edge in move[0]:
                    new_removals.remove(edge)
                for edge in move[1]:
                    new_additions.remove(edge)
        return independent_moves, list(new_removals), list(new_additions)

