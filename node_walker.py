#!/usr/bin/env python3

# this walks edges in a k-opt move (alternating removed and added edges) to try to decompose a k-opt move into smaller k-opt moves.

from plot import plot_util
import basic
import reader
import nearest_neighbor
import merger
import tour
import two_opt
from adjacency_map import AdjacencyMap
import sys
import disjoiner
import combiner
import random
import double_bridge

class Neighbors:
    def __init__(self):
        self.removes = []
        self.adds = []
    def removal(self, new_removal):
        self.removes.append(new_removal)
    def addition(self, new_addition):
        self.adds.append(new_addition)
    def junction(self):
        return len(self.removes) == 2 and len(self.adds) == 2
    def one_way(self):
        return len(self.removes) == 1 and len(self.adds) == 1
    def check(self):
        assert(self.junction() or self.one_way())

class Junction:
    def __init__(self, node_id):
        self.node_id = node_id
        self.removals = []
        self.additions = []
    def addition(self, edge):
        for point in edge:
            if point == self.node_id:
                continue
            self.additions.append(point)
            break
    def removal(self, edge):
        for point in edge:
            if point == self.node_id:
                continue
            self.removals.append(point)
            break
    def check(self):
        return len(self.removals) == 2 and len(self.additions) == 2
    def print(self):
        print("junction:")
        print("\tnode_id: " + str(self.node_id))
        print("\tremovals: " + str(self.removals))
        print("\tadditions: " + str(self.additions))

def find_junctions(removals, additions):
    assert(len(removals) == len(additions))
    frequency = {}
    for edge in removals:
        for point in edge:
            if point not in frequency:
                frequency[point] = 0
            frequency[point] += 1
    junction_points = [x for x in frequency if frequency[x] == 2]
    junctions = {}
    for point in junction_points:
        junctions[point] = Junction(point)
    for edge in removals:
        for point in edge:
            if point in junctions:
                junctions[point].removal(edge)
    for edge in additions:
        for point in edge:
            if point in junctions:
                junctions[point].addition(edge)
    return junctions

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

def traverse_path(path, junction_points, removal_map, addition_map):
    while True:
        if path.last in junction_points:
            path.junctions.append(path.last)
            break
        if path.last_removed:
            next_point = addition_map[path.last]
            path.addition(next_point)
        else:
            next_point = removal_map[path.last]
            path.removal(next_point)
    path.junctions = (min(path.junctions), max(path.junctions))

def traverse_paths(junction, junction_points, removal_map, addition_map):
    new_paths = []
    new_paths.append(InterJunctionPath(junction, removal = True, first = True))
    new_paths.append(InterJunctionPath(junction, removal = True, first = False))
    new_paths.append(InterJunctionPath(junction, removal = False, first = True))
    new_paths.append(InterJunctionPath(junction, removal = False, first = False))
    # index by junctions.
    for p in new_paths:
        traverse_path(p, junction_points, removal_map, addition_map)
    return new_paths

def remove_junction_paths(paths, removed_paths, include_path_edges = True):
    for p in removed_paths:
        paths.remove(p)
    if not paths:
        return
    for r in removed_paths:
        to_merge = []
        j = r.junctions[0]
        for p in paths:
            if j in p.junctions:
                to_merge.append(p)
        print(len(to_merge))
        assert(len(to_merge) == 2)
        to_merge[0].merge(to_merge[1], j)
        if include_path_edges:
            to_merge[0].merge(r, j)
        paths.remove(to_merge[1])

def print_kmove(kmove):
    print("removals: " + str(kmove[0]))
    print("additions: " + str(kmove[1]))
    if len(kmove) > 2:
        print("improvement: " + str(kmove[2]))

def find_paths(junctions, removals, additions):
    # junction nodes will have arbitrary map entries, but they won't be used anyways.
    removal_map = {}
    for edge in removals:
        removal_map[edge[0]] = edge[1]
        removal_map[edge[1]] = edge[0]
    addition_map = {}
    for edge in additions:
        addition_map[edge[0]] = edge[1]
        addition_map[edge[1]] = edge[0]
    junction_points = [junctions[x].node_id for x in junctions]
    paths = []
    for key in junctions:
        new_paths = traverse_paths(junctions[key], junction_points, removal_map, addition_map)
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

def get_alternate_nodes(junction, excluded_nodes):
    removal = None
    addition = None
    for p in junction.removals:
        if p not in excluded_nodes:
            assert(removal == None)
            removal = p
    for p in junction.additions:
        if p not in excluded_nodes:
            assert(addition == None)
            addition = p
    return removal, addition # the paths list should not contain any trivial / fake paths.
def remove_independent_kmoves(paths, junctions, removal_map, addition_map):
    kmoves = []
    clean = False
    while not clean:
        removed_paths = []
        removed_junctions = []
        clean = True
        for p in paths:
            if p.cyclic() and p.even_edge_count():
                clean = False
                kmoves.append((p.removals, p.additions))
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
                new_removal, new_addition = get_alternate_nodes(junctions[j], excluded_nodes)
                removal_map[new_removal] = j
                removal_map[j] = new_removal
                addition_map[new_addition] = j
                addition_map[j] = new_addition
                if j not in removed_junctions:
                    removed_junctions.append(j)
                removed_paths.append(p)
        for r in removed_junctions:
            junctions.pop(r)
        remove_junction_paths(paths, removed_paths, include_path_edges = False)
    return kmoves

def find_kmoves(xy, paths):
    kmoves = [make_kmove(xy, paths)]
    for p in paths:
        start_junction = p.junctions[0]
        search_junction = p.junctions[1]
        find_kmove(xy, kmoves, paths, start_junction, [p], search_junction)
    return kmoves

def make_kmove(xy, path_list):
    removals = []
    additions = []
    for p in path_list:
        removals += p.removals
        additions += p.additions
    removals.sort()
    additions.sort()
    improvement = basic.edge_cost_sum(xy, removals) - basic.edge_cost_sum(xy, additions)
    return (tuple(removals), tuple(additions), improvement)

def find_kmove(xy, kmoves, paths, start_junction, current_path, junction):
    for p in paths:
        if p in current_path:
            continue
        if current_path[-1].compatible(p, junction):
            current_path.append(p)
            assert(junction in p.junctions)
            new_junction = p.junctions[0]
            if junction == p.junctions[0]:
                new_junction = p.junctions[1]
            if new_junction == start_junction and current_path[0].compatible(p, start_junction):
                new_move = make_kmove(xy, current_path)
                k_remove = len(new_move[0])
                k_add = len(new_move[1])
                assert(k_remove == k_add)
                if new_move not in kmoves:
                    kmoves.append(new_move)
            else:
                find_kmove(xy, kmoves, paths, start_junction, current_path, new_junction)
            current_path.pop()

def filter_impossible_kmoves(kmoves):
    max_improvement = 0
    for kmove in kmoves:
        if kmove[2] > 0:
            max_improvement += kmove[2]
    nontrivial_kmoves = []
    for kmove in kmoves:
        if kmove[2] + max_improvement > 0:
            nontrivial_kmoves.append(kmove)
    return nontrivial_kmoves

def compute_improvements(xy, kmoves):
    new_kmoves = []
    for kmove in kmoves:
        improvement = basic.edge_cost_sum(xy, kmove[0]) - basic.edge_cost_sum(xy, kmove[1])
        new_kmoves.append((kmove[0], kmove[1], improvement))
    return new_kmoves
def get_all_kmoves(xy, old_edges, new_edges):
    d = disjoiner.Disjoiner(old_edges, new_edges)
    disjoint_kmoves, old_edges, new_edges = d.get_independent_moves(old_edges, new_edges)
    junctions = find_junctions(old_edges, new_edges)
    nontrivial_paths, easy_kmoves = find_paths(junctions, old_edges, new_edges)
    # junction correctness check.
    for key in junctions:
        junctions[key].check()
    kmoves = find_kmoves(xy, nontrivial_paths)
    kmoves += compute_improvements(xy, easy_kmoves)
    kmoves += compute_improvements(xy, disjoint_kmoves)
    kmoves.sort(key = lambda x : x[2], reverse = True)
    return filter_impossible_kmoves(kmoves)

def find_combos(kmoves, current_remove_set = set(), current_addition_set = set(), current_improvement = 0, start_index = 0):
    if start_index >= len(kmoves):
        return []
    new_move = kmoves[start_index]
    if current_improvement + new_move[2] <= 0:
        return []
    for edge in new_move[0]:
        if edge in current_remove_set:
            return find_combos(kmoves, current_remove_set, current_addition_set, current_improvement, start_index + 1)
    for edge in new_move[1]:
        if edge in current_addition_set:
            return find_combos(kmoves, current_remove_set, current_addition_set, current_improvement, start_index + 1)
    new_removals = list(current_remove_set) + list(new_move[0])
    new_additions = list(current_addition_set) + list(new_move[1])
    current_improvement += new_move[2]
    combos = [(new_removals, new_additions, current_improvement)]
    combos += find_combos(kmoves, set(new_removals), set(new_additions), current_improvement, start_index + 1)
    combos.sort(key = lambda x : x[2], reverse = True)
    return combos

def do_kmove(order, kmove):
    m = AdjacencyMap(order)
    m.check()
    m.apply_kmove(kmove)
    m.check()
    return m.generate_order()

def tour_diff(order1, order2):
    edges1 = basic.edges_from_order(order1)
    edges2 = basic.edges_from_order(order2)
    old_edges, new_edges = merger.edge_diff(edges1, edges2)
    return list(old_edges), list(new_edges)

def opt2(order):
    optimizer = two_opt.TwoOpt(xy)
    optimizer.tour.reset(order)
    optimizer.optimize()
    return optimizer.tour.node_ids

def merge_old(best_tour, new_tour):
    old_edges, new_edges = tour_diff(best_tour, new_tour)
    kmoves = get_all_kmoves(xy, old_edges, new_edges)
    combos = find_combos(kmoves)
    for combo in combos:
        new_order = do_kmove(best_tour, combo)
        if new_order:
            print("improved through merge by " + str(combo[-1]))
            return new_order
    return None

def merge(xy, best_tour, new_tour):
    old_edges, new_edges = tour_diff(best_tour, new_tour)
    if not old_edges:
        return best_tour
    d = disjoiner.Disjoiner(old_edges, new_edges)
    kmoves = []
    for kmove in d.kmoves:
        kmove.find_atomic_kmoves(xy)
        kmoves += kmove.atomic_kmoves
    for kmove in kmoves:
        kmove.compute_improvement(xy)
    kmoves.sort(key = lambda x : x.improvement, reverse = True)
    c = combiner.Combiner(kmoves)
    for combo in c.combos:
        new_order = do_kmove(best_tour, combo)
        if new_order:
            print("improved through merge by " + str(combo.improvement))
            #combo.sort()
            #combo.print()
            return new_order
    return best_tour

def merge_double_bridge(xy, best_order, start_point):
    original_length = len(best_order)
    trial_order = double_bridge.perturbed_climb(xy, best_order, 1)
    trial_length = basic.tour_length(xy, trial_order)
    print("trial tour length: " + str(trial_length))

    old_edges, new_edges = tour_diff(best_order, trial_order)
    basic.write_edges(old_edges, "output/old_edges_test.txt")
    basic.write_edges(new_edges, "output/new_edges_test.txt")

    best_order = merge(xy, best_order, trial_order)
    new_length = basic.tour_length(xy, best_order)
    print("new length: " + str(new_length))
    assert(trial_length >= new_length)
    assert(len(best_order) == original_length)
    return best_order


def merge_nn(xy, best_order, start_point):
    original_length = len(best_order)
    trial_order = nearest_neighbor.generate_tour(xy, start_point)
    trial_order = opt2(trial_order)
    trial_order = double_bridge.perturbed_climb(xy, trial_order, 1)
    trial_length = basic.tour_length(xy, trial_order)
    print("trial tour length: " + str(trial_length))

    old_edges, new_edges = tour_diff(best_order, trial_order)
    basic.write_edges(old_edges, "output/old_edges_test.txt")
    basic.write_edges(new_edges, "output/new_edges_test.txt")

    best_order = merge(xy, best_order, trial_order)
    new_length = basic.tour_length(xy, best_order)
    print("new length: " + str(new_length))
    assert(trial_length >= new_length)
    assert(len(best_order) == original_length)
    return best_order

if __name__ == "__main__":
    xy = reader.read_xy("../data/xqf131.tsp")

    order = [i for i in range(len(xy))]
    random.shuffle(order)
    order = opt2(order)
    print("initial tour length: " + str(basic.tour_length(xy, order)))
    for i in range(1000):
        basic.write_edges_from_order(order, "output/order_test.txt")
        print("merge iteration: " + str(i))
        premerge_length = basic.tour_length(xy, order)
        #order = merge_nn(xy, order, i)
        order = merge_double_bridge(xy, order, i)
        postmerge_length = basic.tour_length(xy, order)
        if postmerge_length != premerge_length:
            order = opt2(order)
            postmerge_climb_length = basic.tour_length(xy, order)
            if postmerge_climb_length != postmerge_length:
                print("post-merge hill climb: " + str(postmerge_climb_length))
