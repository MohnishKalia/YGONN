import json
from multiprocessing import freeze_support

from card_fuzz import dedupe_card_names, get_cdb_cards
from tfidf import load_dataset

if __name__ == '__main__':
    freeze_support()

    X_train, feature_names = load_dataset(verbose=True)

    features_sums = X_train.sum(axis=0) # type: ignore
    features = sorted(list(zip(feature_names, features_sums.A1)), key=lambda kv: -kv[1])

    ygo_features = list(filter(lambda kv: (kv[1] >= 0.15), features))
    ygo_feature_names = [cn for cn,_ in ygo_features]

    cards = get_cdb_cards()
    matches = dedupe_card_names(cards, ygo_feature_names)

    poss_matches = list(filter(lambda m: m[1], zip(ygo_feature_names, matches)))

    with open("card_matches.json", 'w') as f:
        json.dump(poss_matches, f)
