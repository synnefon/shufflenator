from enum import Enum
from random import randint

from shuffle_scorers import SCORE_FUNCTION_MAP


class ShuffledDeck:
    def __init__(self, card_list, permutation, score_type):
        self.card_list = card_list
        self.permutation = permutation
        self.score_type = score_type
        self.score = SCORE_FUNCTION_MAP[score_type](card_list)

    def __eq__(self, other):
        if isinstance(other, ShuffledDeck):
            return self.card_list == other.card_list
        return False

    def __hash__(self):
        return hash(tuple(self.card_list))

    def print(self):
        print(self.permutation, ":", self.score)

def format_response(original_deck, card_piles):
    return ShuffledDeck(
        [card for pile in card_piles for card in pile],
        original_deck.permutation + (len(card_piles),),
        original_deck.score_type
    )

def shuffle(pile_selector, deck, num_piles):
    piles = [[] for _ in range(num_piles)]

    for idx in range(len(deck.card_list)):
        pile = pile_selector(idx)
        piles[pile].insert(0, deck.card_list[idx])

    return format_response(deck, piles)

def pile_shuffle(deck, num_piles): 
    pile_selector = lambda idx: idx % num_piles
    return shuffle(pile_selector, deck, num_piles)

def random_pile_shuffle(deck, num_piles):
    pile_selector = lambda _: randint(0, num_piles-1)
    return shuffle(pile_selector, deck, num_piles)

def cut_deck(deck):
    half_way = int(len(deck.card_list)/2)
    pile_selector = lambda idx: idx + half_way if idx < half_way else idx - half_way
    return shuffle(pile_selector, deck, len(deck.card_list))

SHUFFLE_STRAT = Enum('shuffle type', ['PILE', 'RANDOM_PILE'])
SHUFFLE_FUNCTION_MAP = {
    SHUFFLE_STRAT.PILE: pile_shuffle,
    SHUFFLE_STRAT.RANDOM_PILE: random_pile_shuffle
}
