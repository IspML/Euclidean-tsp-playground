#!/usr/bin/env python3

import matplotlib.pyplot as plt

import sys

def read_point_file_path(point_file_path):
    coordinates = []
    with open(point_file_path, "r") as f:
        for line in f:
            if "NODE_COORD_SECTION" in line:
                break
        for line in f:
            line = line.strip()
            if "EOF" in line or not line:
                break
            fields = line.strip().split()
            coordinates.append((float(fields[1]), float(fields[2])))
    return coordinates

def read_edge_list(file_path):
    edges = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                edge = [int(x) for x in line.strip().split()]
                edges.append(edge)
    return edges

def read_and_plot_tour(coordinates, tour_file_path, markers):
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

    x = []
    y = []
    for i in tour:
        c = coordinates[i - 1]
        x.append(c[0])
        y.append(c[1])
    x.append(x[0])
    y.append(y[0])
    plt.plot(x, y, markers)
