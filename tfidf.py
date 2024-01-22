# https://scikit-learn.org/stable/auto_examples/text/plot_document_classification_20newsgroups.html

from time import time
from sklearn.feature_extraction.text import TfidfVectorizer

def size_mb(docs):
    return sum(len(s.encode("utf-8")) for s in docs) / 1e6

def load_dataset(filepath="reddit_complex.txt", verbose=False):
    with open(filepath, "r") as f:
        train_data = f.readlines()

    # Extracting features from the training data using a sparse vectorizer
    t0 = time()
    vectorizer = TfidfVectorizer(
        sublinear_tf=True, min_df=0.0, stop_words="english", analyzer='word', ngram_range=(1,3)
    )
    X_train = vectorizer.fit_transform(train_data)
    duration_train = time() - t0

    feature_names = vectorizer.get_feature_names_out()

    if verbose:
        # compute size of loaded data
        data_train_size_mb = size_mb(train_data)

        print(
            f"{len(train_data)} documents - "
            f"{data_train_size_mb:.2f}MB (training set)"
        )
        print(
            f"vectorize training done in {duration_train:.3f}s "
            f"at {data_train_size_mb / duration_train:.3f}MB/s"
        )
        print(f"n_samples: {X_train.shape[0]}, n_features: {X_train.shape[1]}")

    return X_train, feature_names
