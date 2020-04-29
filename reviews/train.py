import numpy as np
from sklearn.ensemble import AdaBoostClassifier
from sklearn.linear_model import Perceptron
from sklearn.model_selection import cross_validate
from sklearn.naive_bayes import MultinomialNB
from sklearn.utils import shuffle
import pandas as pd

from reviews.vectorize import configurations
import reviews.logconf
import logging


def score(clf, X, y):
    scores = cross_validate(clf, X, y, cv=5, scoring=['accuracy'])
    avg_accuracy = scores['test_accuracy'].mean()
    var_accuracy = scores['test_accuracy'].std() * 2
    return avg_accuracy, var_accuracy


def train(data_dir):
    logging.info(f'Training on data from {data_dir}')
    X = np.load(f'{data_dir}/X.npy')
    y = np.load(f'{data_dir}/y.npy')
    X, y = shuffle(X, y)

    # TODO I cannot find Averaged Perceptor in scikit-learn:
    #      https://github.com/CogComp/lbjava/blob/master/lbjava/src/main/java/edu/illinois/cs/cogcomp/lbjava/learn/BinaryMIRA.java
    # TODO How to use tickeness=5 and learning_rate=0.05
    clf1 = Perceptron(tol=1e-3, random_state=0, n_jobs=-1)

    clf2 = MultinomialNB()

    # TODO Original paper uses BinaryMIRA as a weak classifier:
    #      https://github.com/CogComp/lbjava/blob/master/lbjava/src/main/java/edu/illinois/cs/cogcomp/lbjava/learn/BinaryMIRA.java
    #      I cannot find it in scikit-learn
    clf3 = AdaBoostClassifier(n_estimators=100, random_state=0)

    for clf in [clf1, clf2, clf3]:
        avg_accuracy, var_accuracy = score(clf, X, y)
        clf_name = clf.__class__.__name__
        yield {'data_dir': data_dir,
               'clf_name': clf_name,
               'accuracy': avg_accuracy,
               'variance': var_accuracy}
        logging.info("Accuracy of %s: %0.4f (+/- %0.2f)"
                     % (clf.__class__.__name__,
                        avg_accuracy,
                        var_accuracy))

def train_configurations():
    scores = []
    for extractors in configurations:
        name = '-'.join(extractors)
        data_dir = f'data/prepared/{name}'
        scores.extend(list(train(data_dir)))
    return pd.DataFrame(scores)

scores = train_configurations()
fname = 'data/scores.tsv'
scores.to_csv(fname, sep='\t')
logging.info(f'Scores saved to {fname}')
