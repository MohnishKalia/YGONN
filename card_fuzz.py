import concurrent.futures
import math
import multiprocessing
import sqlite3
from itertools import islice
from time import time

import numpy as np
from thefuzz import process, utils, fuzz


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

# https://www.geeksforgeeks.org/break-list-chunks-size-n-python/
def chunk(arr, arr_size): 
    arr = iter(arr) 
    return iter(lambda: tuple(islice(arr, arr_size)), ()) 

def process_chunk(tcns_chunk: list[str], cards_dict):
    matches = []
    times = []
    for cn in tcns_chunk:
        t0 = time()
        # maybe sort by recency, but no release date data
        bests = process.extractBests(cn, cards_dict, score_cutoff=80, scorer=fuzz.ratio)
        matches.append(bests)
        times.append(time() - t0)
    return matches, times

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
    print(f"dedupe_card_names: Time to pre-process cards: {(time() - t0):.3f}s")
    
    # accelerate CPU fuzzy search by using Process multiprocessing
    t0 = time()
    chunked_cns = list(chunk(target_cns, math.ceil(len(target_cns) / multiprocessing.cpu_count())))
    totalMatches = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        dicts = [processed_cards_dict for _ in chunked_cns]
        results = executor.map(process_chunk, chunked_cns, dicts)
        for tcns_chunk, (matches, times) in zip(chunked_cns, results):
            print(f"process_chunk: {len(tcns_chunk)} card names: mean {np.mean(times):.3f}s, median {np.median(times):.3f}s, min {np.min(times):.3f}s, max {np.max(times):.3f}s")
            totalMatches += matches

    print(f"dedupe_card_names: Time to fuzzy search cards: {(time() - t0):.3f}s")
    return totalMatches
