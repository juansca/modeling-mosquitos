from scipy.stats import zscore
import pandas as pd
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
        self.out_dir = out_dir
        Path(out_dir).mkdir(parents=True,
                            exist_ok=True)

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

        df = pd.read_csv(in_path, sep=',', usecols=USECOLS)
        df = df.dropna()

        result = df.apply(zscore)

        result['Week'] = np.arange(0, df.shape[0])
        results = self._splitter(result, n_inst, p_overlap)

        fname_without_ext = in_path.stem
        data_files = []
        for i, r in enumerate(results):
            out = Path(out_path, fname_without_ext + str(i) + '.csv')
            data_files.append(out)
            r.to_csv(out, sep=',', header=USECOLS_STRING)

        self.data_files = data_files

    def train_test_split(self, p_eval=0.2):
        out_dir = self.out_dir

        val_out_dir = Path(out_dir, 'val')
        val_out_dir.mkdir(parents=True, exist_ok=True)
        train_out_dir = Path(out_dir, 'train')
        train_out_dir.mkdir(parents=True, exist_ok=True)

        for data_file in self.data_files:
            fname = data_file.stem

            df = pd.read_csv(data_file, sep=',', usecols=USECOLS)

            val_limit = int(df.shape[0] * p_eval)
            validation = df[df.shape[0] - val_limit:]
            train = df[:df.shape[0] - val_limit]

            v_file = Path(val_out_dir, fname + '_val' + '.csv')
            validation.to_csv(v_file, sep=',', header=USECOLS_STRING)

            t_file = Path(train_out_dir, fname + '_train' + '.csv')
            train.to_csv(t_file, sep=',', header=USECOLS_STRING)
