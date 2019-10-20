#!/usr/bin/env python3

from matplotlib import pyplot as plt
import plot_util

instance_file = "../../data/xqf131.tsp"
optimal_tour_file = "../../data/xqf131.tour"
optimal_tour_file = None
optimal_tour_file = "../output/order_test.txt"
ref_edges = plot_util.read_edge_list(optimal_tour_file)
coordinates = plot_util.read_point_file_path(instance_file)
old_edges = plot_util.read_edge_list("../output/old_edges_example.txt")
new_edges = plot_util.read_edge_list("../output/new_edges_example.txt")
old_edges = plot_util.read_edge_list("../output/old_edges_test.txt")
new_edges = plot_util.read_edge_list("../output/new_edges_test.txt")
kmove_edges = plot_util.read_edge_list("../output/kmove_edges.txt")
kmove_edges = None

def plot_edges(coordinates, edges, markers, linewidth=1):
    total_length = 0
    for e in edges:
        p1 = coordinates[e[0]]
        p2 = coordinates[e[1]]
        x = [p1[0], p2[0]]
        y = [p1[1], p2[1]]
        plt.plot(x, y, markers, linewidth=linewidth)
        plt.text(p1[0], p1[1], str(e[0]))
        plt.text(p2[0], p2[1], str(e[1]))
        dx = x[1] - x[0]
        dy = y[1] - y[0]
        total_length += round((dx ** 2 + dy ** 2) ** 0.5)
    print("total edge length: " + str(total_length))

if kmove_edges:
    plot_edges(coordinates, kmove_edges, "b-", 2)
plot_edges(coordinates, old_edges, "r-x")
plot_edges(coordinates, new_edges, "r:x", 2)
if optimal_tour_file:
    plot_edges(coordinates, ref_edges, ":k")

plt.gca().set_aspect("equal")
plt.show()

