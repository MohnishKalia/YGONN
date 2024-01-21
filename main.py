from thefuzz import process, utils
import sqlite3

con = sqlite3.connect("./cards.cdb")
cur = con.cursor()

res = cur.execute("""
    select t.id, t.name, t.desc, d.type
    from texts t
    inner join datas d
        on t.id = d.id;
""")

cards = res.fetchall()

if len(cards) == 0:
    raise ValueError("Card DB had no cards")

def dedupe_card_names(cards: list[tuple[int, str]], target_cns: list[str]) -> list[tuple[str, int, int]]:
    """
    from a cdb of cards, and target_cns card names, 
    dedupe to only existing card ids

    Args:
        cards (list[tuple[int, str]]): list of cards in card database (cdb), with (id, name)
        target_cns (list[str]): strings to dedupe into card names

    Returns:
        list[tuple[str, int, int]]: list of (processed card name, score, card id)
    """

    cards_dict = {card[0]:card for card in cards}
    processed_cards_dict = {k:utils.full_process(v[1], True) for k, v in cards_dict.items()}

    # print(processed_cards_dict[99940363])

    matches = []
    for cn in target_cns:
        # maybe sort by recency, but no release date data
        matches.append(process.extractBests(cn, processed_cards_dict, score_cutoff=90)[0])
    return matches

matches = dedupe_card_names(cards, ["endymion", "frost monarch", "gagaga"])
print(matches)
