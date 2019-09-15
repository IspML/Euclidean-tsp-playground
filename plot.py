#!/usr/bin/env python3

from matplotlib import pyplot as plt
from two_opt import TwoOpt
import reader
import mst

xy = reader.read_xy("input/berlin52.tsp")
t = TwoOpt(xy)
t.optimize()
t.tour.plot()

opt = reader.read_tour("input/berlin52.opt.tour")
t.tour.reset(opt)

t.tour.plot(markers = "r^:")

edges = mst.prim(t.tour.xy)
for e in edges:
    c0 = t.tour.xy[e[0]]
    c1 = t.tour.xy[e[1]]
    plt.plot([c0[0], c1[0]], [c0[1], c1[1]], "x:k", linewidth = 2.0)

t.tour.show()




