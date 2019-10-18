#!/usr/bin/env python3

# this walks edges in a k-opt move (alternating removed and added edges) to try to decompose a k-opt move into smaller k-opt moves.

from plot import plot_util
import basic

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
    for r in removed_paths:
        to_merge = []
        j = r.junctions[0]
        for p in paths:
            if j in p.junctions:
                to_merge.append(p)
        assert(len(to_merge) == 2)
        to_merge[0].merge(to_merge[1], j)
        if include_path_edges:
            to_merge[0].merge(r, j)
        paths.remove(to_merge[1])

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
                junctions.pop(p.junctions[0])
                cleaned = False
        # fix path ways for those that include removed junctions.
        remove_junction_paths(filtered_paths, removed_paths)
    # to make walking easier, remove independent kmoves.
    easy_kmoves = remove_independent_kmoves(filtered_paths, junctions, removal_map, addition_map)
    print(str(len(easy_kmoves)) + " easy kmoves.")

    print(str(len(filtered_paths)) + " junction paths")
    for p in filtered_paths:
        p.print()
    return filtered_paths

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
    return removal, addition

# the paths list should not contain any trivial / fake paths.
def remove_independent_kmoves(paths, junctions, removal_map, addition_map):
    kmoves = []
    removed_paths = []
    for p in paths:
        if p.cyclic() and p.even_edge_count():
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
            junctions.pop(j)
            removed_paths.append(p)
    remove_junction_paths(paths, removed_paths, include_path_edges = False)
    return kmoves

def find_kmoves(paths):
    kmoves = []
    for p in paths:
        start_junction = p.junctions[0]
        search_junction = p.junctions[1]
        find_kmove(kmoves, paths, start_junction, [p], search_junction)
    return kmoves

def make_kmove(path_list):
    removals = []
    additions = []
    for p in path_list:
        removals += p.removals
        additions += p.additions
    removals.sort()
    additions.sort()
    return (tuple(removals), tuple(additions))

def find_kmove(kmoves, paths, start_junction, current_path, junction):
    for p in paths:
        if p in current_path:
            continue
        if current_path[-1].compatible(p, junction):
            if current_path[0].compatible(p, start_junction):
                new_move = make_kmove(current_path)
                if new_move not in kmoves:
                    kmoves.append(new_move)
                return
            else:
                assert(junction in p.junctions)
                new_junction = p.junctions[0]
                if junction == p.junctions[0]:
                    new_junction = p.junctions[1]
                current_path.append(p)
                find_kmove(kmoves, paths, start_junction, current_path, new_junction)
                current_path.pop()

class NodeWalker:
    def __init__(self, removed_edges, added_edges):
        self.make_walk_map(removed_edges, added_edges)

    def make_walk_map(self, removed_edges, added_edges):
        self.walk_map = {}
        for e in removed_edges:
            self.removal(e)
        for e in added_edges:
            self.addition(e)
    def pick_start(self):
        start = None
        for key in self.walk_map:
            if self.walk_map[key].one_way():
                start = key
        assert(start != None)
        return start
    def last_neighbors(self):
        return self.walk_map[self.history[-1]]
    def revisiting(self, next_point):
        return [i for i in self.branch_indices if next_point == self.history[i]]
    def step(self):
        next_point = self.last_neighbors().removes[0]
        if not self.remove_next:
            next_point = self.last_neighbors().adds[0]
        if not self.last_neighbors().one_way():
            # branch if not revisited.
            revisit_indices = self.revisiting(next_point)
            if revisit_indices:
                if len(revisit_indices) > 1:
                    print("multiple revisits!")
                for i in revisit_indices:
                    length = len(self.history) - i + 1
                    if length % 2 == 0:
                        self.kmoves.append(self.history[i - 1 : length])
            return False
        self.history.append(next_point)
        self.remove_next = not self.remove_next
        return True
    def walk(self):
        start = self.pick_start()
        self.history = [start]
        self.branch_indices = [] # index after branch root.
        self.kmoves = []
        self.remove_next = True
        while self.step():
            pass
        self.write_history("output/kmove_edges.txt")

    def write_history(self, output_file_path):
        basic.write_walk_edges(self.history, output_file_path)

    def check_made(self, edge):
        for p in edge:
            if p not in self.walk_map:
                self.walk_map[p] = Neighbors()
    def removal(self, edge):
        self.check_made(edge)
        self.walk_map[edge[0]].removal(edge[1])
        self.walk_map[edge[1]].removal(edge[0])
    def addition(self, edge):
        self.check_made(edge)
        self.walk_map[edge[0]].addition(edge[1])
        self.walk_map[edge[1]].addition(edge[0])

if __name__ == "__main__":
    old_edges = plot_util.read_edge_list("output/old_edges_example.txt")
    new_edges = plot_util.read_edge_list("output/new_edges_example.txt")
    luke = NodeWalker(old_edges, new_edges)
    luke.walk()
    junctions = find_junctions(old_edges, new_edges)
    nontrivial_paths = find_paths(junctions, old_edges, new_edges)
    kmoves = find_kmoves(nontrivial_paths)
    print("found " + str(len(kmoves)) + " kmoves.")
    for k in kmoves:
        print("removals: " + str(k[0]))
        print("additions: " + str(k[1]))
    # correctness checks.
    print(str(len(junctions)) + " junctions.")
    for key in junctions:
        junctions[key].check()
        junctions[key].print()

