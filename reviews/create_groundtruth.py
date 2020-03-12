import jsonlines
from itertools import islice
from tqdm import tqdm

from reviews.yelp import read_reviews

FUNNY_THRESHOLD = 5


def is_humorous(review):
    if review['funny'] == 0:
        return False
    elif review['funny'] >= FUNNY_THRESHOLD:
        return True
    else:
        return None


def read(fpath, limit=None):
    for review in tqdm(islice(read_reviews(fpath), limit),
                       desc='Reading reviews...'):
        yield review


def create(from_fpath, humorous_fpath, nonhumorous_fpath):
    humorous_file = jsonlines.open(humorous_fpath, 'w')
    nonhumorous_file = jsonlines.open(nonhumorous_fpath, 'w')
    for review in read(from_fpath, limit=None):
        humorous = is_humorous(review)
        if humorous is not None:
            review = {
                'review_id': review['review_id'],
                'text': review['text'],
                'humorous': humorous
            }
            if humorous:
                humorous_file.write(review)
            else:
                nonhumorous_file.write(review)
    humorous_file.close()
    nonhumorous_file.close()


create('data/yelp-dataset/yelp_academic_dataset_review.json',
       'data/groundtruth-humorous.jl',
       'data/groundtruth-nonhumorous.jl')
