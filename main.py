from thefuzz import process, utils, fuzz
from time import time
import sqlite3
import numpy as np

def get_cdb_cards(cdb_filepath="./cards.cdb", query_end="where (d.type & 0x10) != 0x10") -> list[tuple[int, str]]:
    """
    get cards from a cdb with a certain filter

    Args:
        cdb_filepath str: the path to the card database
        query_end str: the condition to put at the end of the select query

    Returns:
        list[tuple[int, str]]: list of cards in card database (cdb), with (id, name)
    """

    con = sqlite3.connect(cdb_filepath)
    cur = con.cursor()

    res = cur.execute(f"""
        select t.id, t.name, t.desc, d.type
        from texts t
        inner join datas d
            on t.id = d.id
        {query_end}
    """)
    cards = res.fetchall()
    con.close();

    if len(cards) == 0:
        raise ValueError("Card DB had no cards")
    
    return cards;


def dedupe_card_names(cards: list[tuple[int, str]], target_cns: list[str]) -> list[list[tuple[str, int, int]]]:
    """
    from a cdb of cards, and target_cns card names, 
    dedupe to only existing card ids

    Args:
        cards (list[tuple[int, str]]): list of cards in card database (cdb), with (id, name)
        target_cns (list[str]): strings to dedupe into card names

    Returns:
        list[tuple[str, int, int]]: list of (processed card name, score, card id)
    """

    t0 = time()
    cards_dict = {card[0]:card for card in cards}
    processed_cards_dict = {k:utils.full_process(v[1], True) for k, v in cards_dict.items()}
    # target_cns = process.dedupe(target_cns)
    print(f"Time to pre-process cards: {(time() - t0):.3f}s")

    times = []
    matches = []
    for cn in target_cns:
        t0 = time()
        # maybe sort by recency, but no release date data
        bests = process.extractBests(cn, processed_cards_dict, score_cutoff=80)
        matches.append(bests)
        times.append(time() - t0)

    print(f"{len(target_cns)} card names: mean {np.mean(times):.3f}s, median {np.median(times):.3f}s, min {np.min(times):.3f}s, max {np.max(times):.3f}s")

    return matches
