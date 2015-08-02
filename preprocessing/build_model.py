from __future__ import print_function
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC
import settings


def make_training_set(df):
    """
    Returns a dataframe of training values, and a Series of targets.
    Also records these as .csv files in the CLEANED_PATH directory.
    """
    last_df = df[df['Label'] != 0].copy()

    y = last_df['Label']
    X = last_df.drop(['Timestamp', 'Label'], axis=1).copy()

    # Rebuild indices
    length = X.shape[0]
    X.index = range(length)
    y.index = range(length)

    most_recent = get_most_recent()
    X.to_csv(settings.CLEANED_PATH + 'X' + most_recent)
    y.to_csv(settings.CLEANED_PATH + 'y' + most_recent)

    return X, y


def find_best_params(X, y):
    """
    Finds best parameters for training set X and y by doing a grid search
    along with cross validation. Returns best parameters as a dictionary.
    """
    print(__doc__)

    # Split the dataset in two equal parts
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=0)

    # Set the parameters by cross-validation
    tuned_parameters = [{'kernel': ['rbf', 'poly', 'sigmoid'],
                        'gamma': [1e-3, 1e-4],
                         'C': [1, 10, 100, 1000]},
                        {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]

    scores = ['precision']

    for score in scores:
        print("# Tuning hyper-parameters for %s" % score)
        print()

        clf = GridSearchCV(SVC(C=1), tuned_parameters, cv=5,
                           scoring='%s' % score)
        clf.fit(X_train, y_train)

        print("Best parameters set found on development set:")
        print()
        print(clf.best_params_)
        print()
        print("Grid scores on development set:")
        print()
        for params, mean_score, scores in clf.grid_scores_:
            print("%0.3f (+/-%0.03f) for %r"
                  % (mean_score, scores.std() * 2, params))
        print()

        print("Detailed classification report:")
        print()
        print("The model is trained on the full development set.")
        print("The scores are computed on the full evaluation set.")
        print()
        y_true, y_pred = y_test, clf.predict(X_test)
        print(classification_report(y_true, y_pred))
        print()

    return clf.best_params_


def fit_model(X, y):
    """Finds best parameters for model, returns trained linear SVC."""
    params = find_best_params(X, y)
    if 'gamma' in params:
        clf = SVC(C=params['C'], kernel=params['kernel'],
                  gamma=params['gamma'])
    else:
        clf = SVC(C=params['C'], kernel=params['kernel'])
    clf.fit(X, y)
    return clf
