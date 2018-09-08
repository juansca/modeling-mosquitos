#!/usr/bin/env python3
"""Run a model to tune the hyperparameters

Usage:
  ./main_tune.py -i <s> --model <s> param <n> ...
  ./main_tune.py -h | --help
"""

from src.utils import load_data, stats
from sklearn.decomposition import PCA
from models.models import MODELS
import pandas as pd
import sys


def can_cast(s, caster=int):
    try:
        caster(s)
        return True
    except ValueError:
        return False


if __name__ == '__main__':
    argv, opts = sys.argv[1:], {}
    for i in range(0, len(argv) - 1, 2):
        opts[argv[i]] = argv[i+1]

    fixed_opts = ['-i', '--sp', '-p', '--model']
    params = {k: v for k, v in opts.items() if k not in fixed_opts}
    opts = {k: v for k, v in opts.items() if k in fixed_opts}

    for k, v in params.items():
        if can_cast(v, int):
            params[k] = int(v)
        elif can_cast(v, float):
            params[k] = float(v)

    model = MODELS[opts['--model']]

    if '-p' in opts:
        params = dict(pd.read_csv(opts['-p']))
        params = {k: v[0] for k, v in params.items()}

    n_cols, weeks, y, X = load_data(filename=opts['-i'])

    try:
        model.pca
    except AttributeError:
        pass
    else:
        pca = PCA(n_components=params['n_components'])
        del params['n_components']
        X = pca.fit(X).transform(X)

    model = model(**params)
    scores, mean, std_dev = stats(X, y, model)

    # This is for irace read from stdout
    print(mean)
