"""Plot input data (not predictions) of different cities.

Usage:
  ./plotdata.py [--skipcols <n>] [--nolag] <file> ...

Options:
  --skipcols <n>           plot the data skipping the first <n> cols
  --nolag                  only plot variables with no lag
  --help                   show this screen
"""
from docopt import docopt
from pandas import read_csv
from scipy.stats import zscore
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from utils import get_filename_from_path
from constants import XTICKS_HEATMAP
import numpy as np
import seaborn as sns


class PlotData():
    def __init__(self, no_lag=True, skip_columns=0):
        self.no_lag = no_lag
        self.skip_columns = skip_columns
        sns.set()

    def _drop_columns(self, df):
        skipcols = self.skip_columns
        columns = df.columns.values.tolist()
        dropcols = [x for x in range(len(columns) - skipcols)]
        df = df.drop(df.columns[dropcols], axis=1)
        if self.no_lag:
            dropcols = [c for c in columns if 'lag' in c]
            df = df.drop(dropcols, axis=1)
        return df

    def plot(self, filenames):
        for i, filename in enumerate(filenames):
            df = self._drop_columns(read_csv(filename, sep=','))
            df = df.dropna()
            df = df.apply(zscore)

            fig = plt.figure(i)

            step = int(df.shape[0] / XTICKS_HEATMAP)
            xticklabels = np.arange(0, df.shape[0], step)

            ax = sns.heatmap(np.transpose(df), cmap='YlGnBu',
                             xticklabels=xticklabels)

            ax.xaxis.set_major_locator(MaxNLocator(integer=True))

            fig.suptitle(get_filename_from_path(filename))
            plt.yticks(rotation='horizontal')

        plt.show()