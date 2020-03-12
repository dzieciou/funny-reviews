import jsonlines
from tqdm import tqdm

def read_reviews(fpath):
    with jsonlines.open(fpath) as reviews:
        for review in reviews:
            yield review
