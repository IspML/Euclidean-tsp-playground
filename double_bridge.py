#!/usr/bin/env python3

from two_opt import TwoOpt
import reader
import merger

xy = reader.read_xy("input/berlin52.tsp")
xy = reader.read_xy("input/xqf131.tsp")
best_climber = TwoOpt(xy)
best_climber.optimize()
best_length = best_climber.tour.tour_length()
print("local optimum: " + str(best_length))

test_climber = TwoOpt(xy)
for i in range(1000):
    test_climber.tour.reset(best_climber.tour.node_ids)
    test_climber.tour.double_bridge_perturbation()
    test_climber.optimize()

    print("iteration " + str(i) + " best tour length: " + str(best_length))
    test_tour_length = test_climber.tour.tour_length()
    print("iteration " + str(i) + " test tour length: " + str(test_tour_length))
    if test_tour_length < best_length:
        best_climber.tour.reset(test_climber.tour.node_ids)
        best_length = best_climber.tour.tour_length()
        continue
    merger.merge(best_climber, test_climber.tour.node_ids)
    best_length = best_climber.tour.tour_length()
print("final tour length: " + str(best_length))

