#!/usr/bin/env python3

from matplotlib import pyplot as plt
from two_opt import TwoOpt
import reader
import mst

def plot_edges(tour, edges, markers = "x:k"):
    linewidth = 2.0
    if ":" in markers:
        linewidth = 3.0
    for e in edges:
        c0 = tour.xy[e[0]]
        c1 = tour.xy[e[1]]
        plt.plot([c0[0], c1[0]], [c0[1], c1[1]], markers, linewidth = linewidth)

if __name__ == "__main__":
    xy = reader.read_xy("input/berlin52.tsp")
    t = TwoOpt(xy)
    t.optimize()
    t.tour.plot()
    t.tour.plot_seq()

    edges = mst.prim(t.tour.xy)

    diff_edges = mst.get_new_mst_edges(t.tour, edges)
    print("diff edges from 2-opt: " + str(len(diff_edges)))

    opt = reader.read_tour("input/berlin52.opt.tour")
    t.tour.reset(opt)

    t.tour.plot(markers = "r^:")

    diff_edges = mst.get_new_mst_edges(t.tour, edges)
    print("diff edges from optimal: " + str(len(diff_edges)))
    plot_edges(t.tour, diff_edges)

    t.tour.show()


