import re
from itertools import islice, chain

from tqdm import tqdm

from reviews.yelp import read_reviews


def get_reviews(limit=None):
    reviews = chain(
        islice(read_reviews('data/wikified_by_glow2/groundtruth-humorous-train.jl'), limit),
        islice(read_reviews('data/wikified_by_glow2/groundtruth-nonhumorous-train.jl'), limit),
        islice(read_reviews('data/wikified_by_glow2/groundtruth-humorous-dev.jl'), limit),
        islice(read_reviews('data/wikified_by_glow2/groundtruth-nonhumorous-dev.jl'), limit))
    return tqdm(reviews, desc='Reading reviews...')

all_wikilinks = set()
for review in get_reviews():
    wikilinks = re.findall(r'<a href="([^"]+)"', review['wikified'])
    all_wikilinks.update(wikilinks)
print(all_wikilinks)