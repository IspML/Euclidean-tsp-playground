#!/usr/bin/env python3

# decomposes a k-move into smaller, "atomic" k-moves.
# must not contain separate disjoint moves.
# separate disjoint moves with no junction will not be captured.

import kmove

class Decomposer:
    def __init__(self, kmove):
        self.atomic_kmoves = []
        self.junctions = kmove.find_junctions()
        self.paths = find_paths(kmove)
        kmoves = get_all_kmoves(xy, kmove)
    def find_paths(self, kmove):
        # junction nodes will have arbitrary map entries, but they won't be used anyways.
        removal_map = {}
        for edge in kmove.removals:
            removal_map[edge[0]] = edge[1]
            removal_map[edge[1]] = edge[0]
        addition_map = {}
        for edge in kmove.additions:
            addition_map[edge[0]] = edge[1]
            addition_map[edge[1]] = edge[0]
        paths = []
        for key in junctions:
            new_paths = traverse_paths(kmove.junctions[key], kmove.junction_points, removal_map, addition_map)
            for np in new_paths:
                paths.append(np)
                for p in paths[:-1]:
                    if p.equals(np):
                        paths.pop()
                        break
        # eliminate "fake" junctions if path shows them to be practically one-way.
        filtered_paths = paths[:]
        cleaned = False
        while not cleaned:
            cleaned = True
            removed_paths = []
            for p in filtered_paths:
                if p.cyclic() and p.odd_edge_count():
                    removed_paths.append(p)
                    cleaned = False
            for r in removed_paths:
                junction = r.junctions[0]
                if junction in junctions:
                    junctions.pop(junction)
            # fix path ways for those that include removed junctions.
            remove_junction_paths(filtered_paths, removed_paths)
        # to make walking easier, remove independent kmoves.
        easy_kmoves = remove_independent_kmoves(filtered_paths, junctions, removal_map, addition_map)
        return filtered_paths, easy_kmoves

