import numpy as np
from sklearn.ensemble import AdaBoostClassifier
from sklearn.linear_model import Perceptron
from sklearn.model_selection import cross_validate
from sklearn.naive_bayes import MultinomialNB
from sklearn.utils import shuffle
import pathlib

from reviews.prepare_data import configurations
import reviews.logconf
import logging


# TODO What about saving X and y

def score(clf, X, y):
    scores = cross_validate(clf, X, y, cv=5, scoring=['accuracy'])
    logging.info("Accuracy of %s: %0.2f (+/- %0.2f)"
                 % (clf.__class__.__name__,
                    scores['test_accuracy'].mean(),
                    scores['test_accuracy'].std() * 2))


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
        score(clf, X, y)


for extractors in configurations:
    name = '-'.join(extractors)
    data_dir = f'data/prepared/{name}'
    train(data_dir)
