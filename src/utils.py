import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from sklearn.model_selection import cross_val_score


def smoothing(xs):
    n = len(xs)
    for i in range(1, n - 1):
        xs[i] = sum([xs[j] for j in [i - 1, i, i + 1]]) / 3
    xs[0] = xs[1]
    xs[n - 1] = xs[n - 2]

    return xs


def save_data(filename, weeks, y_true, y_pred):
    """Save the predictions to a csv."""
    assert len(weeks) == len(y_true)
    assert len(y_pred) == len(y_true)
    X = np.transpose(np.array([weeks, y_true, y_pred]))
    np.savetxt(filename, X, delimiter=',')


def load_data(filename='data/all.csv'):
    """Load the training data set."""

    data = np.loadtxt(filename, delimiter=',', skiprows=1)
    n_rows, n_cols = data.shape
    assert n_cols > 3

    weeks = data[:, 0]
    ts = smoothing(data[:, 1])
    xs = data[:, 2:]

    return n_cols, weeks, ts, xs


def stats(xs, ts, model, n_splits=5):
    cv = TimeSeriesSplit(n_splits)
    scores = cross_val_score(model, xs, ts, cv=cv.split(xs),
                             scoring='neg_mean_squared_error')
    scores = np.sqrt(-scores)

    mean = scores.mean()
    std_dev = scores.std()

    return scores, mean, std_dev


def print_stats(scores, mean, std_dev, title='Stats'):
    print()
    print(title)
    print('-' * len(title))
    print('')
    print('Model Scores: ', scores)
    print('Mean Score: ', mean)
    print('Standard Deviation of Score: ', std_dev)




def get_filename_from_path(path):
    """Given a path, return the name of the file with no extension."""
    name = path.split('/')[-1].split('.')[0]
    return name.capitalize()
