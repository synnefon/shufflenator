from shuffle_scorers import SCORE_TYPE
from shufflers import SHUFFLE_FUNCTION_MAP, SHUFFLE_STRAT, ShuffledDeck, cut_deck

MIN_PILES = 1
MAX_PILES = 10
DECK_SIZE = 100
MAX_SHUFFLES = 6
CUT_DECK = False

SHUFFLE_STRATEGY = SHUFFLE_STRAT.PILE
SCORER = SCORE_TYPE.SHANNON_ENTROPY



def shuffle_decks(shuffle_strat, score_type, max_shuffles=MAX_SHUFFLES, should_cut_deck=False):
    PILE_DIVISIONS = [i for i in range(MIN_PILES, MAX_PILES+1)]
    BASE_CARD_LIST = [i for i in range(DECK_SIZE)]
    shuffle_function = SHUFFLE_FUNCTION_MAP[shuffle_strat] if not should_cut_deck \
        else cut_deck(SHUFFLE_FUNCTION_MAP[shuffle_strat](deck, num_piles))

    shuffled_decks = [ShuffledDeck(BASE_CARD_LIST, (), score_type)]
    best = None

    for i in range(max_shuffles):
        print(i+1, "ROUNDS")
        new_decks = []
        for deck in shuffled_decks:
            for num_piles in PILE_DIVISIONS:
                new_decks.append(shuffle_function(deck, num_piles))
        shuffled_decks.extend(d for d in new_decks)
        shuffled_decks = list(set(shuffled_decks))
        shuffled_decks.sort(key=lambda deck: deck.score, reverse=True)

        for deck in shuffled_decks[0: 5]:
            deck.print()
            best = shuffled_decks[0]

        print()
    print(shuffled_decks)
    return best
    

# shuffle_decks(SHUFFLE_STRATEGY, SCORER, CUT_DECK)
