#!/usr/bin/env python3

from kmove import KMove

class Combiner:
    def __init__(self, kmoves):
        self.kmoves = kmoves
        self.combos = []
        self.find_combos()
        self.combos.sort(key = lambda x : x.improvement, reverse = True)

    def find_combos(self, current_remove_set = set(), current_addition_set = set(), current_improvement = 0, start_index = 0):
        if start_index >= len(self.kmoves):
            return
        new_move = self.kmoves[start_index]
        if current_improvement + new_move.improvement <= 0:
            return
        for edge in new_move.removals:
            if edge in current_remove_set:
                self.find_combos(current_remove_set, current_addition_set, current_improvement, start_index + 1)
                return
        for edge in new_move.additions:
            if edge in current_addition_set:
                self.find_combos(current_remove_set, current_addition_set, current_improvement, start_index + 1)
                return
        new_removals = list(current_remove_set) + list(new_move.removals)
        new_additions = list(current_addition_set) + list(new_move.additions)
        kmove = KMove(new_removals, new_additions)
        current_improvement += new_move.improvement
        kmove.improvement = current_improvement

        self.combos.append(kmove)
        self.find_combos(set(new_removals), set(new_additions), current_improvement, start_index + 1)

    def print_combo(self, removes, adds, improvement):
        print("removes: " + str(removes))
        print("adds: " + str(adds))
        print("improvement: " + str(improvement))
