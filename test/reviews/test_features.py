import spacy

from reviews.features import (
    length,
    unigrams_frequency,
    alliteration,
    letters_to_others
)

nlp = spacy.load("en_core_web_sm", disable=['ner', 'textcat'])


def test_length():
    doc = nlp('12345')
    assert length(doc) == 5


def test_unigrams_frequency():
    corpus = ('Cat is in the room', 'Room is a big room')

    def reviews_reader():
        return ({'text': review} for review in corpus)

    frequency = unigrams_frequency(reviews_reader)
    assert 2 in frequency[1]  # room
    assert 2 not in frequency[0]


def test_alliteration():
    doc = nlp("Infant's don't enjoy infancy, like adults do adultery. "
              "The love belongs to those who belove.")
    assert alliteration(doc) == 5


def test_letters_to_others():
    assert letters_to_others(nlp('12345')) == 0.0
    assert letters_to_others(nlp('A b ')) == 1.0

