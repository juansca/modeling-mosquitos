from scipy.stats import zscore
from pandas import read_csv
import numpy as np
from pathlib import Path

from data.constants import USECOLS

USECOLS_STRING = ",".join(USECOLS)


class DataCleaner():
    """Clean, select and parse data."""

    def __init__(self, in_file, out_dir):
        """
        Init Method.

        Args:
            in_file: Input data filename
            out_dir: Output data dir
        """

        self.in_file = Path(in_file)
        self.out_dir = Path(out_dir)

    def _overlap(self, a, b, p):
        split_point = int(p * len(a))
        return np.concatenate([a, b[:split_point]])

    def _splitter(self, df, n_splits, p=0.25):
        n_cols = df.shape[0]
        ratio = int(n_cols / n_splits)
        spliting_indexes = [i for i in range(ratio,
                                             (n_cols - ratio) + 1,
                                             ratio)]

        dfs = np.split(df, spliting_indexes, axis=0)

        for i in range(len(dfs) - 1):
            dfs[i] = self._overlap(dfs[i], dfs[i+1], p)
        return dfs

    def clean(self, n_inst=1, p_overlap=0):
        """
        Clean the data on input filename.

        Args:
            n_inst:     Number of instances to generate from data
            p_overlap:  Percentage of overlapping between the instances
        """
        in_path = self.in_file
        out_path = self.out_dir

        df = read_csv(in_path, sep=',', usecols=USECOLS)
        df = df.dropna()

        result = df.apply(zscore)

        result['Week'] = np.arange(0, df.shape[0])
        results = self._splitter(result, n_inst, p_overlap)

        fname_without_ext = in_path.stem
        for i, r in enumerate(results):
            out = Path(out_path, fname_without_ext + str(i) + '.csv')
            fmt = ",".join(["%s"] * df.shape[1])
            np.savetxt(out, r, fmt=fmt, delimiter=',', header=USECOLS_STRING)
