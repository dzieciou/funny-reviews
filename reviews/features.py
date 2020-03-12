from collections import defaultdict
from statistics import mean

import numpy as np
import spacy
from nltk.corpus import wordnet as wn
from sklearn.feature_extraction.text import CountVectorizer

from reviews.rhymes import find_alliterations, find_rhymes

nlp = spacy.load("en_core_web_sm", disable=['ner', 'textcat'])


def unigrams_frequency(reviews_reader):
    vectorizer = CountVectorizer(stop_words='english', max_features=100)
    texts = (review['text'] for review in reviews_reader())
    features = vectorizer.fit_transform(texts).toarray().tolist()
    features = {id_: vector for id_, vector in enumerate(features)}
    return features


def length(doc):
    return len(doc.text)


def letters_to_others(doc):
    letters = [ch for ch in doc.text if ch.isupper() or ch.islower()]
    return len(letters) / length(doc)


def average_word_length(doc):
    return mean([len(token.text) for token in doc if _is_word(token)])


def alliteration(doc):
    return len(list(find_alliterations(doc))) + len(list(find_rhymes(doc)))


def ambiguity(doc):
    nouns = [token.text for token in doc if token.pos_ == 'NOUN']
    synsets_count = [len([_noun_synsets(noun) for noun in nouns])]
    return mean(synsets_count)


def incongruity(doc):
    # TODO
    return 0


def incongruity_enthropy(doc):
    # TODO
    return 0


def unexpectedness_max_deviation(doc):
    # TODO
    return 0


def unexpectedness(doc):
    # TODO
    return 0


def _is_word(token):
    return token.pos_ in ('ADJ', 'ADP', 'ADV', 'AUX', 'CONJ', 'CCONJ', 'DET',
                          'INTJ', 'NOUN', 'NUM', 'PART', 'PRON', 'PROPN',
                          'SCONJ', 'VERB')


def _noun_synsets(word):
    return [synset for synset in wn.synsets(word) if synset.pos() == 'n']


def merge_dicts(d1, d2):
    return {**d1, **d2}


C1 = unigrams_frequency
C2 = length
C3 = average_word_length
C4 = letters_to_others
E1 = alliteration
E2 = ambiguity
A1 = incongruity
A2 = incongruity_enthropy
D2 = unexpectedness_max_deviation
U2 = unexpectedness


class Vectorizer:
    CORPUS_EXTRACTORS = [unigrams_frequency]

    def __init__(self, extractors):
        self.corpus_extrs = [e for e in extractors if
                             e in self.CORPUS_EXTRACTORS]
        self.doc_extrs = [e for e in extractors if
                          e not in self.CORPUS_EXTRACTORS]

    def review2label(self, review):
        return 1 if review['humorous'] else 0

    def review2features(self, review):
        doc = nlp(review['text'])
        # TODO What if extractor returns multiple numbers (array)
        return [extractor(doc) for extractor in self.doc_extrs]

    def corpus2features(self, review_reader):
        for extractor in self.corpus_extrs:
            yield extractor(review_reader)

    def vectorize(self, reviews_reader):
        features = defaultdict(list)
        labels = {}
        for id_, review in enumerate(reviews_reader()):
            labels[id_] = self.review2label(review)
            features[id_].extend(self.review2features(review))

        for corpus_features in self.corpus2features(reviews_reader):
            for id_ in corpus_features:
                features[id_].extend(corpus_features[id_])

        X = [v for k, v in sorted(features.items())]
        y = [v for k, v in sorted(labels.items())]
        return np.array(X), np.array(y)
