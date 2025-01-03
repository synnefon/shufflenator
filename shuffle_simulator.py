from shufflers import SHUFFLE_FUNCTION_MAP, ShuffledDeck, cut_deck
from multiprocessing.pool import ThreadPool
import time

MT_CUTOFF = 5_000

def run_perm_multi(shuffled_decks, pile_divisions, shuffle_function):
    num_threads = int(len(shuffled_decks) / MT_CUTOFF)
    chunks = [shuffled_decks[i*MT_CUTOFF:(i+1)*MT_CUTOFF] for i in range(num_threads+1)]
    pool = ThreadPool(processes=num_threads)

    threads = [pool.apply_async(run_perm, (chunk, pile_divisions, shuffle_function)) for chunk in chunks]
    
    result_lists = [t.get() for t in threads]
    results = [x for xs in result_lists for x in xs]
    return results

def run_perm(shuffled_decks, pile_divisions, shuffle_function):
    if len(shuffled_decks) > MT_CUTOFF:
        return run_perm_multi(shuffled_decks, pile_divisions, shuffle_function)
    
    new_decks = []
    for deck in shuffled_decks:
        for num_piles in pile_divisions:
            res = shuffle_function(deck, num_piles)
            new_decks.append(res)

    return new_decks

def shuffle_decks(
        shuffle_strat,
        score_type,
        max_shuffles,
        deck_size,
        min_num_piles,
        max_num_piles,
    ):

    pile_divisions = [i for i in range(min_num_piles, max_num_piles+1)]
    base_card_list = [i for i in range(deck_size)]
    shuffle_function = SHUFFLE_FUNCTION_MAP[shuffle_strat]

    shuffled_decks = [ShuffledDeck(base_card_list, (), score_type)]
    
    best = None
    for i in range(max_shuffles):
        print("ITERATION", i+1)
        new_decks = run_perm(shuffled_decks, pile_divisions, shuffle_function)

        shuffled_decks.extend(d for d in new_decks)
        shuffled_decks = list(set(shuffled_decks))
        shuffled_decks.sort(key=lambda deck: deck.score, reverse=True)
        
        best = shuffled_decks[0]
    
    return best
