import json
from multiprocessing import freeze_support

from card_fuzz import dedupe_card_names, get_cdb_cards
from tfidf import load_dataset

if __name__ == '__main__':
    freeze_support()

    X_train, feature_names = load_dataset(verbose=True)
    
    cards = get_cdb_cards()
    matches = dedupe_card_names(cards, feature_names.tolist())

    # list(zip(feature_names, matches))
    poss_matches = list(filter(lambda m: m[1], zip(feature_names, matches)))
    # print(len(poss_matches))

    with open("card_matches.json", 'w') as f:
        json.dump(poss_matches, f)
