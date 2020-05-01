import spacy

from reviews.rhymes import is_rhyme, is_alliteration, find_alliterations, find_rhymes

nlp = spacy.load("en_core_web_sm", disable=['ner', 'textcat'])


def test_is_rhyme():
    assert is_rhyme(['greenery', 'scenery'])
    assert not is_rhyme(['greenery', 'cat'])
    assert is_rhyme(['love', 'belove', 'glove'])
    assert not is_rhyme(['love', 'belove', 'dog'])


def test_is_rhyme_should_work_only_for_lowercase():
    assert not is_rhyme(['LOVE', 'belove'])


def test_is_alliteration():
    assert is_alliteration(['adult', 'adultery'])
    assert not is_alliteration(['adult', 'rabbit'])
    assert is_alliteration(['infant', 'infancy'])
    assert not is_alliteration(['infant', 'adultery'])
    assert not is_alliteration(['veni', 'vidi', 'vici'])  # only English words
    assert not is_alliteration(['do', 'do'])

def test_find_alliterations():
    doc = nlp("Infant's don't enjoy infancy, like adults do adultery.")
    assert list(find_alliterations(doc)) == [('infant', 'infancy'), ('adults', 'adultery')]

def test_find_rhymes():
    doc = nlp("The love belongs to those who belove.")
    assert list(find_rhymes(doc)) == [('love', 'belove'), ('to', 'who')]