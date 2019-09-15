#!/usr/bin/env python3

import random

class Box:
    def __init__(self, xy):
        x = [c[0] for c in xy]
        y = [c[1] for c in xy]
        self.xmin = min(x)
        self.xmax = max(x)
        self.ymin = min(y)
        self.ymax = max(y)
        self.dx = self.xmax - self.xmin
        self.dy = self.ymax - self.ymin
    def random_xy(self):
        rx = random.random() * self.dx + self.xmin
        ry = random.random() * self.dy + self.ymin
        return rx, ry

