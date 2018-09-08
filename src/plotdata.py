"""Plot input data (not predictions) of different cities."""
from src.utils import get_filename_from_path
from data.constants import XTICKS_HEATMAP

from pandas import read_csv
from scipy.stats import zscore
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import seaborn as sns


class PlotData():
    def __init__(self, no_lag=True, skip_columns=0):
        self.no_lag = no_lag
        self.skip_columns = skip_columns

    def _drop_columns(self, df):
        skipcols = self.skip_columns
        columns = df.columns.values.tolist()
        dropcols = [x for x in range(len(columns) - skipcols)]
        df = df.drop(df.columns[dropcols], axis=1)
        if self.no_lag:
            dropcols = [c for c in columns if 'lag' in c]
            df = df.drop(dropcols, axis=1)
        return df

    def plot_heatmap(self, filenames, dpi=300):
        sns.set()

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

    def generate_curve_plot(self, weeks, y_true, y_pred,
                            xlabel='Weeks', ylabel='Normalized abundance',
                            label_true='Ground truth',
                            label_pred='Model', dpi=300):
        self.dpi = dpi
        plt.clf()

        plt.plot(weeks, y_true,
                 color='c', linestyle='dashed', label=label_true)

        plt.plot(weeks, y_pred,
                 color='g', linestyle='solid', label=label_pred)

        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        plt.legend()

    def plot_result(self):
        if len(plt.get_fignums()) == 0:
            raise SavingWithoutPlot('Trying to show a figure before plot it')
        plt.show()

    def save_plot_result(self, filename):
        if len(plt.get_fignums()) == 0:
            raise SavingWithoutPlot('Trying to save a figure before plot it')
        plt.savefig(filename, format='eps', dpi=self.dpi)


class SavingWithoutPlot(Exception):
    """
    This class represent an exception ocurred when try to show or save a
    figure before plot it.
    """
    pass
