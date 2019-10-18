#!/usr/bin/env python3

from matplotlib import pyplot as plt
import util

instance_file = "../../data/pbn423.tsp"
instance_file = "../../data/xrb14233.tsp"

optimal_tour_file = "../../data/pbn423.tour"
optimal_tour_file = "../../data/xrb14233.tour"

cycle1_file = "../output/cycle0_margin_1.txt"
cycle2_file = "../output/cycle1_margin_1.txt"

coordinates = util.read_point_file_path(instance_file)
cycle1 = util.read_edge_list(cycle1_file)
cycle2 = util.read_edge_list(cycle2_file)

def plot_cycle(coordinates, edges, markers):
    xx = [coordinates[e[0]][0] for e in edges]
    xx.append(xx[0])
    yy = [coordinates[e[0]][1] for e in edges]
    yy.append(yy[0])
    plt.plot(xx, yy, markers)

plot_cycle(coordinates, cycle1, "g-x")
plot_cycle(coordinates, cycle2, "r-x")
util.read_and_plot_tour(coordinates, optimal_tour_file, ":k")

plt.gca().set_aspect("equal")
plt.show()

