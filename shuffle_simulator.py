from shufflers import SHUFFLE_FUNCTION_MAP, ShuffledDeck, cut_deck

def shuffle_decks(
        shuffle_strat,
        score_type,
        max_shuffles,
        deck_size,
        min_num_piles,
        max_num_piles,
        should_cut_deck=False
    ):
    
    PILE_DIVISIONS = [i for i in range(min_num_piles, max_num_piles+1)]
    BASE_CARD_LIST = [i for i in range(deck_size)]
    shuffle_function = SHUFFLE_FUNCTION_MAP[shuffle_strat] if not should_cut_deck \
        else cut_deck(SHUFFLE_FUNCTION_MAP[shuffle_strat](deck, num_piles))

    shuffled_decks = [ShuffledDeck(BASE_CARD_LIST, (), score_type)]
    best = None

    for _ in range(max_shuffles):
        new_decks = []
        for deck in shuffled_decks:
            for num_piles in PILE_DIVISIONS:
                new_decks.append(shuffle_function(deck, num_piles))
        shuffled_decks.extend(d for d in new_decks)
        shuffled_decks = list(set(shuffled_decks))
        shuffled_decks.sort(key=lambda deck: deck.score, reverse=True)

        for deck in shuffled_decks[0: 5]:
            best = shuffled_decks[0]

    return best
