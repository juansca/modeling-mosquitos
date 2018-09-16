"""Train a model

Usage:
  ./train.py -i <file> --model <model> [-p <file>]
  ./train.py -h | --help

Options:
  -i <file>         Train/Val dataset path
  --model <model>   Model you want to train, is mandatory that it was on
                    models.py file.
  -p <file>         CSV file where are saved the hyperparameters (in case of
                    tunning module was used).
"""
from utils.utils import load_data, stats, print_stats
import pandas as pd
from sklearn.decomposition import PCA
from models import MODELS
from docopt import docopt
from pathlib import Path
import pickle


class BadModelName(Exception):
    pass


def train_model(train_path: Path, model_name: str, hparams: Path):
    hparams = pd.read_csv(hparams)
    params = dict()
    for i in hparams:
        if i == 'model' and hparams[i][0] != model_name:
            msg = "Your modelname does not match with the hyperparameters file"
            raise BadModelName(msg)
        if i != 'Unnamed: 0' and i != 'model':
            params[i] = hparams[i][0]

    # Get the data
    n_cols, weeks, y, X = load_data(filename=train_path)

    # Get the model
    model = MODELS[model_name]
    try:
        model.pca
        pca = PCA(n_components=params['n_components'])
        del params['n_components']
        X = pca.fit(X).transform(X)
    except AttributeError:
        pass

    # Get stats from the model
    model = model(**params)
    scores, mean, std_dev = stats(X, y, model)
    print_stats(scores, mean, std_dev)

    # Train and save
    print("Training a {}...".format(model_name))
    model.fit(X, y)

    print("Saving the model...")
    trained_model_dir = Path(Path(__file__).parents[1], 'trained')
    trained_model_dir.mkdir(parents=True, exist_ok=True)
    trained_model_file = Path(trained_model_dir, model_name + '.pkl')

    f = open(trained_model_file, 'wb')
    pickle.dump(model, f)
    f.close()
    print("Model saved succesfuly")


if __name__ == '__main__':
    opts = docopt(__doc__)
    model_name = opts['--model']

    # Get parameters
    hparams = Path(opts['-p'])
    train_path = Path(opts['-i'])
    train_model(train_path, model_name, hparams)
