import cmudict
from itertools import product, combinations

pronunciations_dict = cmudict.dict()


def _is_vowel_with_primary_stress(phoneme):
    return phoneme.endswith('1')


def _is_vowel_with_secondary_stress(phoneme):
    return phoneme.endswith('0')


def _rhyme_phonemes(word):
    pronunciations = pronunciations_dict[word]
    for phonemes in pronunciations:
        index = next((i for i, phoneme
                      in enumerate(phonemes)
                      if _is_vowel_with_primary_stress(phoneme)), None)
        if index is not None:
            yield tuple(phonemes[index:])


def _alliteration_phonemes(word):
    pronunciations = pronunciations_dict[word]
    for phonemes in pronunciations:
        index = next((i for i, phoneme
                      in enumerate(phonemes)
                      if _is_vowel_with_primary_stress(phoneme)), None)
        if index is not None:
            yield tuple(phonemes[:index + 1])
        index = next((i for i, phoneme
                      in enumerate(phonemes)
                      if _is_vowel_with_secondary_stress(phoneme)), None)
        if index is not None:
            yield tuple(phonemes[:index + 1])


def is_rhyme(words):
    if len(set(words)) != len(words):  # same words are not rhymes
        return False
    words_phonemes = [tuple(_rhyme_phonemes(word)) for word in words]
    for phonemes in product(*words_phonemes):
        if len(set(phonemes)) == 1:  # all the same
            return True
    return False


def is_alliteration(words):
    if len(set(words)) != len(words):  # same words are not alliterations
        return False
    words_phonemes = [tuple(_alliteration_phonemes(word)) for word in words]
    for phonemes in product(*words_phonemes):
        if len(set(phonemes)) == 1:  # all the same
            return True
    return False


def normalize(word):
    return word.lower()


def find_alliterations(doc, max_length=3):
    for sent in doc.sents:
        words = [normalize(token.text) for token in sent]
        for length in range(2, max_length):
            alliterations = (c for c in combinations(words, length) if
                             is_alliteration(c))
            yield from alliterations


def find_rhymes(doc, max_length=3):
    for sent in doc.sents:
        words = [normalize(token.text) for token in sent]
        for length in range(2, max_length):
            rhymes = (c for c in combinations(words, length) if is_rhyme(c))
            yield from rhymes
