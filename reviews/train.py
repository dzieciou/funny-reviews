import numpy as np
from sklearn.ensemble import AdaBoostClassifier
from sklearn.linear_model import Perceptron
from sklearn.model_selection import cross_validate
from sklearn.naive_bayes import GaussianNB
from sklearn.utils import shuffle
import pathlib

from reviews.prepare_data import configurations


# TODO What about saving X and y

def score(clf, X, y):
    scores = cross_validate(clf, X, y, cv=5, scoring=['accuracy'])
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores['test_accuracy'].mean(),
                                           scores['test_accuracy'].std() * 2))

for extractors in configurations:
    name = '-'.join(extractors)
    directory = f'data/prepared/{name}'
    pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
    X = np.load(f'{directory}/X.npy')
    y = np.load(f'{directory}/y.npy')
    X, y = shuffle(X, y)

    # TODO I cannot find Averaged Perceptor in scikit-learn:
    #      https://github.com/CogComp/lbjava/blob/master/lbjava/src/main/java/edu/illinois/cs/cogcomp/lbjava/learn/BinaryMIRA.java
    # TODO How to use tickeness=5 and learning_rate=0.05
    clf1 = Perceptron(tol=1e-3, random_state=0, n_jobs=-1)

    # TODO Naive Bayer (NB) is a family of classifiers. We should make sure which one is used in
    #      LEARNING TO LAUGH (AUTOMATICALLY): COMPUTATIONAL MODELS FOR HUMOR RECOGNITION
    #      https://ccc.inaoep.mx/~villasen/bib/LEARNING%20TO%20LAUGH%20(AUTOMATICALLY).pdf
    clf2 = GaussianNB()

    # TODO Original paper uses BinaryMIRA as a weak classifier:
    #      https://github.com/CogComp/lbjava/blob/master/lbjava/src/main/java/edu/illinois/cs/cogcomp/lbjava/learn/BinaryMIRA.java
    #      I cannot find it in scikit-learn
    clf3 = AdaBoostClassifier(n_estimators=100, random_state=0)

    for clf in [clf1, clf2, clf3]:
        score(clf, X, y)
