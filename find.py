from reviews.yelp import read_reviews

original = [review["review_id"] for review in read_reviews(
    "D:\\Projects-intellij\\funny-reviews\\data\\samples\\groundtruth-nonhumorous-train.jl")]
wikified = [review["review_id"] for review in read_reviews(
    "D:\\Projects-intellij\\funny-reviews\\data\\wikified_by_glow2\\groundtruth-nonhumorous-train.jl")]

print(set(wikified) - set(original))
