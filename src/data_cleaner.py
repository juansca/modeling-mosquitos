from scipy.stats import zscore
from pandas import read_csv
import numpy as np
from pathlib import Path

from constants import USECOLS

USECOLS_STRING = ",".join(USECOLS)


class DataCleaner():
    """Clean, select and parse data."""

    def __init__(self, in_file, out_file):
        """
        Init Method.

        Args:
            in_file: Input data filename
            out_file: Output data filename or dir in the case of splitting
        """

        self.in_file = Path(in_file)
        self.out_file = Path(out_file)

    def _overlap(self, a, b, p):
        split_point = int(p * len(a))
        return np.concatenate([a, b[:split_point]])

    def _splitter(self, df, n_splits, p=0.25):
        n_cols = df.shape[0]
        ratio = int(n_cols / n_splits)
        spliting_indexes = [i for i in range(ratio, n_cols - ratio, ratio)]

        dfs = np.split(df, spliting_indexes, axis=0)
        for i in range(len(dfs) - 1):
            dfs[i] = self._overlap(dfs[i], dfs[i+1], p)
        return dfs

    def clean(self, n_inst=None, p_overlap=0):
        """
        Clean the data on input filename.

        Args:
            n_inst:     Number of instances to generate from data
            p_overlap:  Percentage of overlapping between the instances
        """
        in_path = self.in_file
        out_path = self.out_file

        df = read_csv(in_path, sep=',', usecols=USECOLS)
        df = df.dropna()

        result = df.apply(zscore)

        result['Week'] = np.arange(0, df.shape[0])

        if n_inst is None:
            result.to_csv(out_path, sep=',', index=False)
        else:
            nsplit = int(n_inst)
            p = float(p_overlap)

            results = self._splitter(result, nsplit, p)

            fname_without_ext = in_path.stem

            for i, r in enumerate(results):
                out = Path(out_path, fname_without_ext, str(i), '.csv')
                fmt = ",".join(["%s"] * df.shape[1])
                np.savetxt(out, r, fmt=fmt, delimiter=',', header=USECOLS_STRING)
