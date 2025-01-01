from collections import Counter
from enum import Enum
import numpy as np

def calc_adjacent_term_differences(cards):
    deck_len = len(cards)
    adjacent_term_differences = []
    for idx in range(deck_len):
        next_idx = (idx+1) % deck_len
        diff = (cards[next_idx] - cards[idx])
        if diff < 0:
            diff += deck_len
        adjacent_term_differences.append(diff)
    return adjacent_term_differences

def calc_average_neighbor_dist(cards):
    return sum(calc_adjacent_term_differences(cards)) / len(cards)

def calc_location_delta(cards):
    total_location_delta = 0
    for idx in range(len(cards)):
        delta = abs(idx - cards[idx])
        total_location_delta += delta
    return total_location_delta / len(cards)

def calc_shannon_entropy(cards):
    adjacent_term_differences = calc_adjacent_term_differences(cards)
    term_counts = {}
    for diff in adjacent_term_differences:
        term_counts[diff] = term_counts.get(diff, 0) + 1 
    p_counts = [c / len(cards) for c in term_counts.values()]
    ln_p_counts = [abs(np.log(p) * p) for p in p_counts if p > 0]
    return sum(ln_p_counts)

SCORE_TYPE = Enum('score type', ['SHANNON_ENTROPY', 'NEIGHBOR_DIST', 'LOCATION_DELTA'])
SCORE_FUNCTION_MAP = {
    SCORE_TYPE.SHANNON_ENTROPY: calc_shannon_entropy,
    SCORE_TYPE.NEIGHBOR_DIST: calc_average_neighbor_dist,
    SCORE_TYPE.LOCATION_DELTA: calc_location_delta
}
