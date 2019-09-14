#!/usr/bin/env python3

def read_xy(file_path):
    xy = []
    with open(file_path, "r") as f:
        for line in f:
            if "NODE_COORD_SECTION" in line:
                break
        for line in f:
            line = line.strip().split()
            if not line:
                continue
            if "EOF" in line or "-1" in line:
                break
            xy.append((float(line[1]), float(line[2])))
    return xy

def read_tour(file_path):
    tour = []
    with open(file_path, "r") as f:
        for line in f:
            if "TOUR_SECTION" in line:
                break
        for line in f:
            line = line.strip()
            if not line:
                continue
            if "EOF" in line or "-1" in line:
                break
            tour.append(int(line) - 1)
    return tour

if __name__ == "__main__":
    for c in read_xy("input/berlin52.tsp"):
        print(c)
    print("tour:")
    for t in read_tour("input/berlin52.opt.tour"):
        print(t)

