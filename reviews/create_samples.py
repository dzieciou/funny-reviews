import jsonlines
from sklearn.utils.random import sample_without_replacement
from tqdm import tqdm

# TODO Add logging of original stastistics, final output statistics in form of TSV file
# TODO Add logging of line counting
from reviews.yelp import read_reviews


def get_reviews(fpath, indexes):
    last = max(indexes)
    with jsonlines.open(fpath) as reviews:
        for i, review in enumerate(reviews):
            if i in indexes:
                yield review
            if i == last:
                return


def save(fpath, reviews):
    with jsonlines.open(fpath, 'w') as f:
        for review in reviews:
            f.write(review)


def count_lines(fpath):
    count = 0
    with jsonlines.open(fpath) as lines:
        for _ in lines:
            count += 1
    return count


count_reviews = count_lines


def sample_multiple(n_population, *n_samples_list):
    population = range(n_population)
    for n_samples in n_samples_list:
        indexes = sample_without_replacement(n_population, n_samples)
        sample = [population[i] for i in indexes]
        yield sample
        remaining = set(range(n_population)) - set(indexes)
        population = [population[i] for i in remaining]
        n_population = len(population)


def sample_reviews(fpath, n_samples_list, fnames):
    n_reviews = count_reviews(fpath)
    samples = sample_multiple(n_reviews, *n_samples_list)
    for fname, sample in zip(fnames, samples):
        with jsonlines.open(fname, 'w') as output:
            for i, review in tqdm(enumerate(read_reviews(fpath)),
                                  total=n_reviews,
                                  desc=f'Sampling to {fname}...'):
                if i in sample:
                    output.write(review)


SIZE = 12000*5
DEV_SIZE = 5000*5

sample_reviews('data/groundtruth-humorous.jl',
               [SIZE, DEV_SIZE],
               ['data/groundtruth-humorous-train.jl',
                'data/groundtruth-humorous-dev.jl'])

sample_reviews('data/groundtruth-nonhumorous.jl',
               [SIZE, DEV_SIZE],
               ['data/groundtruth-nonhumorous-train.jl',
                'data/groundtruth-nonhumorous-dev.jl'])
