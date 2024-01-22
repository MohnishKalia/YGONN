# %%
from tfidf import load_dataset

X_train, feature_names = load_dataset(verbose=True)

# %%
len(feature_names)

# %%
from main import get_cdb_cards, dedupe_card_names

cards = get_cdb_cards()

matches = dedupe_card_names(cards, feature_names.tolist())

# %%
import json
# list(zip(feature_names, matches))
poss_matches = list(filter(lambda m: m[1], zip(feature_names, matches)))
# print(len(poss_matches))

with open("card_matches.txt", 'w') as f:
    json.dump(poss_matches, f)
