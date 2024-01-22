FILES = $(wildcard reddit_posts/*)

all: card_matches.txt

card_matches.txt: tfidf_reddit.py tfidf.py reddit_complex.txt
	python ./tfidf_reddit.py

reddit_complex.txt: preprocess_reddit.py $(FILES)
	python ./preprocess_reddit.py

clean:
	rm -f card_matches.txt reddit_complex.txt
