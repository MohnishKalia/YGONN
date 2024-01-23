FILES = $(wildcard reddit_posts/*)

all: card_matches.json

card_matches.json: tfidf_reddit.py tfidf.py card_fuzz.py reddit_complex.txt
	python ./tfidf_reddit.py

reddit_complex.txt: preprocess_reddit.py $(FILES)
	python ./preprocess_reddit.py

clean:
	rm -f card_matches.txt reddit_complex.txt
