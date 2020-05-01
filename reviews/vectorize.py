import logging

import numpy as np
from itertools import islice, chain
from tqdm import tqdm
import pathlib
from reviews import features
from reviews.features import Vectorizer
from reviews.yelp import read_reviews
import reviews.logconf


def get_reviews(limit=100
):
    reviews = chain(
        islice(read_reviews('data/samples/groundtruth-humorous-train.jl'), limit),
        islice(read_reviews('data/samples/groundtruth-nonhumorous-train.jl'), limit),
        islice(read_reviews('data/samples/groundtruth-humorous-dev.jl'), limit),
        islice(read_reviews('data/samples/groundtruth-nonhumorous-dev.jl'), limit))
    return tqdm(reviews, desc='Reading reviews...')


def prepare(extractors):
    logging.info(f"Preparing data with extractors: {extractors}")
    name = '-'.join(extractors)
    extractors = [getattr(features, e) for e in extractors]
    vectorizer = Vectorizer(extractors)
    X, y = vectorizer.vectorize(get_reviews)
    directory = f'data/prepared/{name}'
    pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
    np.save(f'{directory}/X.npy', X)
    np.save(f'{directory}/y.npy', y)


configurations = (
    ('C1',),
    ('C2',),
    ('C3',),
    ('C4',),
    ('E1',),
    ('E2',),
  # Once we have generative models working those features can be implemented and used
  # ('A1',),
  # ('A2',),
  # ('D2',),
  # ('U2',),DONE
  # ('A1', 'U2',),
  # ('A2', 'D2',),
  # ('D2', 'U2',),
  # ('A2', 'D2', 'U2',),
  # ('D2', 'U2', 'C1',),
  # ('A2', 'D2', 'C1',),
  # ('A1', 'D2', 'U2', 'C1',),
  # ('A2', 'D2', 'U2', 'C1',),
)

if __name__ == '__main__':
    for extractors in configurations:
        prepare(extractors)
