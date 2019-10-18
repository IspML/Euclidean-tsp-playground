#!/usr/bin/env python3

import matplotlib.pyplot as plt
import plot_util

import sys

if len(sys.argv) < 4:
    print("inputs: point_file_path first_tour_file_path second_tour_file_path")
    sys.exit()

coordinates = plot_util.read_point_file_path(sys.argv[1])
x = [c[0] for c in coordinates]
y = [c[1] for c in coordinates]
plt.plot(x, y, "xk")

def read_and_plot_tour(tour_file_path, color):
    tour = []
    with open(tour_file_path, "r") as f:
        for line in f:
            if "TOUR_SECTION" in line:
                break
        for line in f:
            line = line.strip()
            if "-1" in line or "EOF" in line or not line:
                break
            fields = line.strip().split()
            tour.append((int(fields[0])))

    for i in range(len(tour) - 1):
        c = coordinates[tour[i] - 1]
        n = coordinates[tour[i + 1] - 1]
        plt.plot([c[0], n[0]], [c[1], n[1]], color)
    c = coordinates[tour[-1] - 1]
    n = coordinates[tour[0] - 1]
    plt.plot([c[0], n[0]], [c[1], n[1]], color)
    plt.axis("equal")

read_and_plot_tour(sys.argv[2], "b")
read_and_plot_tour(sys.argv[3], ":r")

def plot_coord(i):
    plt.plot(coordinates[i][0], coordinates[i][1], "og")

if len(sys.argv) > 4:
    plot_coord(int(sys.argv[4]))

plt.show()
