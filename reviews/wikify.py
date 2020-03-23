import spacy
from itertools import chain, islice
from tqdm import tqdm

import jsonlines
from reviews.yelp import read_reviews

nlp = spacy.load("en_core_web_sm")


def get_reviews(limit=None):
    reviews = chain(
        islice(read_reviews('data/groundtruth-humorous-train.jl'), limit),
        islice(read_reviews('data/groundtruth-nonhumorous-train.jl'), limit),
        islice(read_reviews('data/groundtruth-humorous-dev.jl'), limit),
        islice(read_reviews('data/groundtruth-nonhumorous-dev.jl'), limit))
    return tqdm(reviews, desc='Reading reviews...')


def wikify(review):
    doc = nlp(review['text'])
    return [
        {
            'entity': e.text,
            'label': e.label_,
            'kb_id_': e.kb_id_
        }
        for e in doc.ents
    ]


with jsonlines.open('data/wikified.jl', 'w') as out:
    for review in get_reviews():
        out.write({
            'review_id': review['review_id'],
            'entities': wikify(review)
        })
