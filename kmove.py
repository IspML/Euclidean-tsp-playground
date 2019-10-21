#!/usr/bin/env python3

import basic
import junction
import inter_junction_path

class KMove:
    def __init__(self, removals, additions):
        self.removals = list(removals)
        self.additions = list(additions)
        self.removals.sort()
        self.additions.sort()
        self.removals = tuple(removals)
        self.additions = tuple(additions)
        self.atomic_kmoves = []
        self.check()

    def sort(self):
        self.removals = list(self.removals)
        self.removals.sort()
        self.removals = tuple(self.removals)
        self.additions = list(self.additions)
        self.additions.sort()
        self.additions = tuple(self.additions)
    def print(self):
        print(str(len(self.removals)) + "-opt move:")
        print("removals: " + str(self.removals))
        print("additions: " + str(self.additions))
        print("improvement: " + str(self.improvement))
        print()
    def print_atomic_kmoves(self):
        for am in self.atomic_kmoves:
            am.print()
    def find_atomic_kmoves(self, xy):
        self.find_junctions()
        if len(self.junctions) == 0:
            self.atomic_kmoves = [KMove(self.removals, self.additions)]
            return
        self.find_paths()
        # junction correctness check.
        for point in self.junctions:
            self.junctions[point].check()
        self.find_kmoves(xy)
        self.atomic_kmoves.sort(key = lambda x : x.compute_improvement(xy), reverse = True)
        self.filter_impossible_kmoves(xy)
        #self.print_atomic_kmoves()

    def find_kmoves(self, xy):
        self.atomic_kmoves += [self.make_kmove(xy, self.paths)] # this should not be neccessary.
        for p in self.paths:
            start_junction = p.junctions[0]
            search_junction = p.junctions[1]
            self.find_kmove(xy, start_junction, [p], search_junction)

    def find_kmove(self, xy, start_junction, current_path, junction):
        for p in self.paths:
            if p in current_path:
                continue
            if current_path[-1].compatible(p, junction):
                current_path.append(p)
                assert(junction in p.junctions)
                new_junction = p.junctions[0]
                if junction == p.junctions[0]:
                    new_junction = p.junctions[1]
                if new_junction == start_junction and current_path[0].compatible(p, start_junction):
                    new_move = self.make_kmove(xy, current_path)
                    new_move.check()
                    found = False
                    for kmove in self.atomic_kmoves:
                        if new_move.equals(kmove):
                            found = True
                            break
                    if not found:
                        self.atomic_kmoves.append(new_move)
                else:
                    self.find_kmove(xy, start_junction, current_path, new_junction)
                current_path.pop()

    def make_kmove(self, xy, path_list):
        removals = []
        additions = []
        for p in path_list:
            removals += p.removals
            additions += p.additions
        removals.sort()
        additions.sort()
        kmove = KMove(removals, additions)
        kmove.compute_improvement(xy)
        return kmove

    def find_paths(self):
        self.populate_paths()
        self.remove_trivial_paths_and_junctions()
        if len(self.junctions) == 0:
            self.atomic_kmoves = [KMove(self.removals, self.additions)]
            return
        # to make walking easier, remove independent kmoves.
        # junction nodes will have arbitrary map entries, but they won't be used anyways.
        self.remove_independent_kmoves()

    # eliminate "fake" junctions that are practically one-way.
    def remove_trivial_paths_and_junctions(self):
        removed_paths = True
        while removed_paths:
            removed_paths = []
            for p in self.paths:
                if p.cyclic() and p.odd_edge_count():
                    removed_paths.append(p)
            # remove junctions.
            for r in removed_paths:
                junction = r.junctions[0]
                if junction in self.junctions:
                    self.junctions.pop(junction)
            # fix path ways for those that include removed junctions.
            self.remove_junction_paths(removed_paths)
    def remove_junction_paths(self, removed_paths, include_path_edges = True):
        for p in removed_paths:
            self.paths.remove(p)
        if not self.paths:
            return
        for r in removed_paths:
            to_merge = []
            j = r.junctions[0]
            for p in self.paths:
                if j in p.junctions:
                    to_merge.append(p)
            assert(len(to_merge) == 2)
            to_merge[0].merge(to_merge[1], j)
            if include_path_edges:
                to_merge[0].merge(r, j)
            self.paths.remove(to_merge[1])

    def remove_independent_kmoves(self):
        removal_map = self.compute_removal_map()
        addition_map = self.compute_addition_map()
        removed_paths = True
        while removed_paths:
            removed_paths = []
            removed_junctions = []
            for p in self.paths:
                if p.cyclic() and p.even_edge_count():
                    self.atomic_kmoves.append(KMove(p.removals, p.additions))
                    j = p.junctions[0]
                    junction_edges = p.get_edges(j)
                    assert(len(junction_edges) == 2)
                    # set the one-way maps to skip the independent kmoves.
                    excluded_nodes = []
                    for je in junction_edges:
                        other = je[0]
                        if je[0] == j:
                            other = je[1]
                        excluded_nodes.append(other)
                    assert(len(excluded_nodes) == 2)
                    new_removal, new_addition = self.junctions[j].get_alternate_nodes(excluded_nodes)
                    removal_map[new_removal] = j
                    removal_map[j] = new_removal
                    addition_map[new_addition] = j
                    addition_map[j] = new_addition
                    if j not in removed_junctions:
                        removed_junctions.append(j)
                    removed_paths.append(p)
            for r in removed_junctions:
                self.junctions.pop(r)
            self.remove_junction_paths(removed_paths, include_path_edges = False)

    # gather paths from junctions, adding only unique ones.
    def populate_paths(self):
        self.compute_addition_map()
        self.compute_removal_map()
        self.paths = []
        for junction_point in self.junctions:
            new_paths = self.traverse_paths(self.junctions[junction_point])
            for np in new_paths:
                self.paths.append(np)
                for p in self.paths[:-1]:
                    if p.equals(np):
                        self.paths.pop()
                        break

    def traverse_paths(self, junction):
        new_paths = []
        new_paths.append(inter_junction_path.InterJunctionPath(junction, removal = True, first = True))
        new_paths.append(inter_junction_path.InterJunctionPath(junction, removal = True, first = False))
        new_paths.append(inter_junction_path.InterJunctionPath(junction, removal = False, first = True))
        new_paths.append(inter_junction_path.InterJunctionPath(junction, removal = False, first = False))
        # index by junctions.
        for p in new_paths:
            self.traverse_path(p)
        return new_paths

    def traverse_path(self, path):
        while True:
            if path.last in self.junction_points:
                path.junctions.append(path.last)
                break
            if path.last_removed:
                next_point = self.addition_map[path.last]
                path.addition(next_point)
            else:
                next_point = self.removal_map[path.last]
                path.removal(next_point)
        path.junctions = (min(path.junctions), max(path.junctions))

    def find_junctions(self):
        frequency = self.removal_point_frequency()
        self.junction_points = [x for x in frequency if frequency[x] == 2]
        self.junctions = {}
        for point in self.junction_points:
            self.junctions[point] = junction.Junction(point)
        if len(self.junctions) == 0:
            return
        for edge in self.removals:
            for point in edge:
                if point in self.junctions:
                    self.junctions[point].removal(edge)
        for edge in self.additions:
            for point in edge:
                if point in self.junctions:
                    self.junctions[point].addition(edge)

    def removal_point_frequency(self):
        frequency = {}
        for edge in self.removals:
            for point in edge:
                if point not in frequency:
                    frequency[point] = 0
                frequency[point] += 1
        return frequency

    def filter_impossible_kmoves(self, xy):
        max_improvement = 0
        for kmove in self.atomic_kmoves:
            if kmove.improvement > 0:
                max_improvement += kmove.improvement
        nontrivial_kmoves = []
        for kmove in self.atomic_kmoves:
            if kmove.improvement + max_improvement > 0:
                nontrivial_kmoves.append(kmove)
        self.atomic_kmoves = nontrivial_kmoves

    def compute_removal_map(self):
        self.removal_map = {}
        for edge in self.removals:
            self.removal_map[edge[0]] = edge[1]
            self.removal_map[edge[1]] = edge[0]
        return self.removal_map
    def compute_addition_map(self):
        self.addition_map = {}
        for edge in self.additions:
            self.addition_map[edge[0]] = edge[1]
            self.addition_map[edge[1]] = edge[0]
        return self.addition_map

    def check(self):
        assert(len(self.removals) == len(self.additions))
    def compute_improvement(self, xy):
        gain = basic.edge_cost_sum(xy, self.removals)
        loss = basic.edge_cost_sum(xy, self.additions)
        self.improvement = gain - loss
        return self.improvement
    def equals(self, other):
        #if self.improvement != other.improvement:
        #    return False
        if len(self.removals) != len(other.removals) or len(self.additions) != len(other.additions):
            return False
        if self.removals != other.removals:
            return False
        if self.additions != other.additions:
            return False
        return True


