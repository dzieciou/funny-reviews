Reproducing the work of [Identifying Humor in Reviews using Background Text Sources](https://www.aclweb.org/anthology/D17-1051/).

# Running experiments

Download [Yelp dataset](https://www.yelp.com/dataset/download) and unpack to `data/yelp-dataset`.

Run the followning commands:

```bash
conda env create --file environment.yml
conda activate funny-reviews
python reviews/create_groundtruth.py
python reviews/create_samples.py
python reviews/vectorize.py
python reviews/train.py
```