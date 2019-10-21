#!/usr/bin/env python3

class Junction:
    def __init__(self, node_id):
        self.node_id = node_id
        self.removals = []
        self.additions = []
    def addition(self, edge):
        for point in edge:
            if point == self.node_id:
                continue
            self.additions.append(point)
            break
    def removal(self, edge):
        for point in edge:
            if point == self.node_id:
                continue
            self.removals.append(point)
            break

    def get_alternate_nodes(self, excluded_nodes):
        removal = None
        addition = None
        for p in self.removals:
            if p not in excluded_nodes:
                assert(removal == None)
                removal = p
        for p in self.additions:
            if p not in excluded_nodes:
                assert(addition == None)
                addition = p
        return removal, addition # the paths list should not contain any trivial / fake paths.

    def check(self):
        return len(self.removals) == 2 and len(self.additions) == 2
    def print(self):
        print("junction:")
        print("\tnode_id: " + str(self.node_id))
        print("\tremovals: " + str(self.removals))
        print("\tadditions: " + str(self.additions))



