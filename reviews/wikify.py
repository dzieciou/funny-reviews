import spacy
from itertools import chain, islice
from tqdm import tqdm

import jsonlines

from reviews.wikifiers.brank import BrankWikifier
from reviews.yelp import read_reviews

nlp = spacy.load("en_core_web_sm")


def get_reviews(limit=10):
    reviews = chain(
        islice(read_reviews('data/groundtruth-humorous-train.jl'), limit),
        islice(read_reviews('data/groundtruth-nonhumorous-train.jl'), limit),
        islice(read_reviews('data/groundtruth-humorous-dev.jl'), limit),
        islice(read_reviews('data/groundtruth-nonhumorous-dev.jl'), limit))
    return tqdm(reviews, desc='Reading reviews...')


wikifier = BrankWikifier('vanfmxwemngacoystnhmrlcblktwvs')


def wikify(review):
    for e in wikifier.wikify(review['text']):
        yield {
            'entity': e.phrase,
            'kb_id': e.kb_id,
            'kb_url': e.kb_url
        }


with jsonlines.open('data/wikified.jl', 'w', flush=True) as out:
    for review in get_reviews():
        out.write({
            'review_id': review['review_id'],
            'entities': list(wikify(review))
        })
