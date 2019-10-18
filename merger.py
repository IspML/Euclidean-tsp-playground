#!/usr/bin/env python3

# tour-merging strategies aimed at identifying and preserving improved sections of tours
# that would otherwise be thrown away if the overall tour length is worse.

import inserter
import deleter
import reader
from two_opt import TwoOpt
import popt
import math
from itertools import combinations
import basic
from matplotlib import pyplot as plt
import sys

def count_num_tries(n):
    combos = 0
    nf = math.factorial(n)
    for r in range(n - 3, n - 1):
        combos += nf / math.factorial(n - r) / math.factorial(r)
    print("combos: " + str(combos))

def edge_diff(edges, other_edges):
    diff = edges - other_edges
    other_diff = other_edges - edges
    assert(len(diff) == len(other_diff))
    return diff, other_diff

def match_sets(edges, other_edges):
    if len(other_edges) < len(edges):
        return None
    points = set()
    for e in edges:
        points.add(e[0])
        points.add(e[1])
    compatible_edges = []
    compatible_points = set()
    for e in other_edges:
        if e[0] in points and e[1] in points:
            compatible_edges.append(e)
            compatible_points.add(e[0])
            compatible_points.add(e[1])
    if len(compatible_edges) < len(edges):
        return None
    if compatible_points != points:
        return None
    if len(compatible_edges) != len(edges):
        cc = combinations(compatible_edges, len(compatible_edges) - 1)
        for c in cc:
            compatible_points = set()
            for e in c:
                compatible_points.add(c[0])
                compatible_points.add(c[1])
            if compatible_points == points:
                return c
        return None
    assert(len(compatible_edges) == len(edges))
    return compatible_edges

def calculate_gain(xy, export_edges, import_edges):
    gain = 0
    for e in export_edges:
        gain += basic.edge_cost(xy, e)
    for e in import_edges:
        gain -= basic.edge_cost(xy, e)
    return gain

MAX_CANDIDATE_CHECKS = 1000000
candidate_checks = 0

def try_n_set(xy, edges, other_edges, n):
    global candidate_checks
    global MAX_CANDIDATE_CHECKS
    assert(len(edges) == len(other_edges))
    cc = combinations(edges, n)
    best_export = None
    best_import = None
    best_gain = -math.inf
    for c in cc:
        matched_set = match_sets(c, other_edges)
        if matched_set:
            gain = calculate_gain(xy, c, matched_set)
            if gain > best_gain:
                best_export = c
                best_import = matched_set
                best_gain = gain
        candidate_checks += 1
        if candidate_checks >= MAX_CANDIDATE_CHECKS:
            print("MAX_CANDIDATE_CHECKS reached.")
            break
    if best_gain <= 0:
        return None
    return best_gain, best_export, best_import

def try_all_sets(xy, edges, other_edges):
    global candidate_checks
    global MAX_CANDIDATE_CHECKS
    costs = [basic.edge_cost(xy, e) for e in edges]
    costs.sort(reverse = True)
    other_costs = [basic.edge_cost(xy, e) for e in other_edges]
    other_costs.sort()
    assert(len(edges) == len(other_edges))
    candidates = []
    candidate_checks = 0
    for i in range(3, len(edges) + 1):
        max_export = sum(costs[:i])
        min_import = sum(other_costs[:i])
        if max_export <= min_import:
            continue
        candidate = try_n_set(xy, edges, other_edges, i)
        if candidate:
            candidates.append(candidate)
        if candidate_checks >= MAX_CANDIDATE_CHECKS:
            break
    candidates.sort(reverse = True)
    return candidates

def compute_move_improvement(xy, move):
    removes = basic.edge_cost_sum(xy, move[0])
    additions = basic.edge_cost_sum(xy, move[1])
    return removes - additions

class Merger:
    def __init__(self, removed_edges, added_edges):
        self.removed_edges = list(removed_edges)
        self.added_edges = list(added_edges)
        self.moves = []
        self.make_disjoint()



    def pop_edge_set(self):
        disjoint_edges1 = []
        disjoint_edges2 = []
        points = set(self.removed_edges[-1])
        removed = extract_adjacent_edges(points, self.removed_edges)
        disjoint_edges1 += removed
        removed = extract_adjacent_edges(points, self.added_edges)
        disjoint_edges2 += removed
        while True:
            removed = extract_adjacent_edges(points, self.removed_edges)
            if not removed:
                break
            disjoint_edges1 += removed
            removed = extract_adjacent_edges(points, self.added_edges)
            if not removed:
                break
            disjoint_edges2 += removed
        self.moves.append((disjoint_edges1, disjoint_edges2))
    def make_disjoint(self):
        self.pop_edge_set()
        while self.removed_edges:
            self.pop_edge_set()
        assert(not self.added_edges)

# each move is a tuple (improvement, move)
# move is (removed_edges, added_edges)
def combine_moves(current_moves, all_moves, index = 0, margin = 0):
    for i in range(index, len(all_moves)):
        m = all_moves[i]
        improvement = m[0] + margin
        if improvement > 0:
            current_moves.append(m)
            combine_moves(current_moves, all_moves, start + 1, margin + improvement)
        improvement = compute_move_improvement(m)
        improvements.append((improvement, m))

def list_from_adjacents(adjacents):
    start = 0
    ordered = [start, adjacents[start][0]]
    while len(ordered) < len(adjacents):
        nxt = adjacents[ordered[-1]][:]
        nxt.remove(ordered[-2])
        ordered.append(nxt[0])
        if ordered[-1] == start:
            return None
    return ordered

def plot_connectivity(xy, cc):
    for i in range(len(cc)):
        c = cc[i]
        for j in c:
            x = [xy[i][0], xy[j][0]]
            y = [xy[i][1], xy[j][1]]
            plt.plot(x, y, "x-")

def feasible(tour, export_edges, import_edges):
    cc = tour.connectivity()
    for e in export_edges:
        cc[e[0]].remove(e[1])
        cc[e[1]].remove(e[0])
    for e in import_edges:
        cc[e[0]].append(e[1])
        if len(cc[e[0]]) > 2:
            return None
        cc[e[1]].append(e[0])
        if len(cc[e[1]]) > 2:
            return None
        cc[e[0]].sort()
        cc[e[1]].sort()
    for c in cc:
        if len(c) != 2:
            return None
    return list_from_adjacents(cc)

def merge(climber, other_node_ids):
    print("attempting merge")
    exportable, importable = edge_diff(climber.tour.edges(), basic.edges_from_order(other_node_ids))
    candidates = try_all_sets(climber.tour.xy, exportable, importable)
    for c in candidates:
        node_ids = feasible(climber.tour, c[1], c[2])
        if node_ids:
            climber.tour.reset(node_ids)
            climber.tour.validate()
            print("merge improvement found: " + str(c[0]) + " gained with edges:")
            print(c[1])
            print(c[2])
            print("improved merged length: " + str(climber.tour.tour_length()))
            climber.optimize()
            print("post-merge hill climb: " + str(climber.tour.tour_length()))
            return True
    print("no improving merge found.")
    return False

def make_edge_map(edges):
    edge_map = {}
    for e in edges:
        if min(e) not in edge_map:
            edge_map[min(e)] = []
        edge_map[min(e)].append(e)
    return edge_map

def extract_adjacent_edges(points, edge_pool):
    removed = []
    for e in edge_pool:
        if e[0] in points or e[1] in points:
            removed.append(e)
            points.add(e[0])
            points.add(e[1])
    for r in removed:
        edge_pool.remove(r)
    return removed

def write_edges(edges, output_file_path):
    with open(output_file_path, "w") as f:
        for e in edges:
            e = [str(x) for x in e]
            f.write(" ".join(e) + "\n")

if __name__ == "__main__":
    xy = reader.read_xy("input/berlin52.tsp")
    xy = reader.read_xy("input/xqf131.tsp")
    t1 = TwoOpt(xy)
    t1.optimize()
    #deleter.deleter(t1)
    print("tour1 length: " + str(t1.tour.tour_length()))

    t2 = TwoOpt(xy)
    for i in range(1000):
        t2.tour.reset(t1.tour.node_ids)
        improvement = popt.sequence_popt(t2, 40)
        new_tour_length = t2.tour.tour_length()
        print("iteration " + str(i) + " best tour length: " + str(t1.tour.tour_length()))
        print("iteration " + str(i) + " new_tour length: " + str(new_tour_length))
        if new_tour_length < t1.tour.tour_length():
            t1.tour.reset(t2.tour.node_ids)
            continue

        exportable, importable = edge_diff(t1.tour.edges(), t2.tour.edges())
        write_edges(exportable, "output/old_edges.txt")
        write_edges(importable, "output/new_edges.txt")

        merger = Merger(exportable, importable)
        print("found " + str(len(merger.moves)) + " moves")
        for m in merger.moves:
            print(calculate_gain(xy, m[0], m[1]))
            assert(len(m) == 2)
            print(m[0])
            print(m[1])
        if merge(t1, t2.tour.node_ids):
            sys.exit()
    print("final tour length: " + str(t1.tour.tour_length()))

