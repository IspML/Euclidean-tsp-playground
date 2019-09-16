#!/usr/bin/env python3

import basic
import reader
import math

def get_new_mst_edges(tour, mst_edges):
    c = tour.connectivity()
    new_edges = []
    for e in mst_edges:
        if e[1] in c[e[0]]:
            assert(e[0] in c[e[1]])
            continue
        new_edges.append(e)
    return new_edges

def compute_sorted_edges(xy, node_id):
    edges = []
    for i in range(len(xy)):
        if i == node_id:
            continue
        edges.append((basic.distance(xy, node_id, i), i))
        edges.sort(reverse=True)
    return edges

def prim(xy, node_ids = None):
    if not node_ids:
        node_ids = [i for i in range(len(xy))]
    remaining_edges = []
    for i in range(len(xy)):
        remaining_edges.append(compute_sorted_edges(xy, i))
    mst_nodes = set()
    start_node = 0
    mst_nodes.add(start_node)
    start_edge = remaining_edges[start_node].pop()
    mst_nodes.add(start_edge[1])
    mst_edges = []
    mst_edges.append((start_node, start_edge[1]))
    while len(mst_nodes) < len(node_ids):
        min_edge = None
        min_length = math.inf
        for mst_node in mst_nodes:
            e = remaining_edges[mst_node]
            while e and e[-1][1] in mst_nodes:
                e.pop()
            if not e:
                continue
            if e[-1][0] < min_length:
                min_edge = (mst_node, e[-1][1])
                min_length = e[-1][0]
        assert(min_edge[0] in mst_nodes)
        assert(min_edge[1] not in mst_nodes)
        mst_nodes.add(min_edge[1])
        mst_edges.append(min_edge)
    assert(len(mst_edges) == len(node_ids) - 1)
    return mst_edges

if __name__ == "__main__":
    xy = reader.read_xy("input/berlin52.tsp")
    print(prim(xy, [x for x in range(len(xy))]))



