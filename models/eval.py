"""Evaluate a model

Usage:
  ./eval.py -i <file> -m <model> [-o <file>]

Options:
  -i <file>         Evaluate dataset path
  -m <model>        Model you want to evaluate as pickle format
  -o <dir>          Directory where the evaluation plot result will be saved
"""
from src.utils import load_data, stats, save_data
from src.plotdata import PlotData
from docopt import docopt
from pathlib import Path
import pickle
from sklearn.metrics import mean_squared_error


class BadModelName(Exception):
    pass


if __name__ == '__main__':
    opts = docopt(__doc__)

    # Load model
    model_file = Path(opts['-m'])

    model_pkl = open(model_file, 'rb')
    model = pickle.load(model_pkl)
    model_pkl.close()

#    try:
#        model.pca
#        pca = PCA(n_components=params['n_components'])
#        del params['n_components']
#        X = pca.fit(X).transform(X)
#    except AttributeError:
#        pass

    # Load data
    data_file = Path(opts['-i'])
    n_cols, weeks, y, X = load_data(filename=data_file)

    # Get stats from the prediction
    scores, mean, std_dev = stats(X, y, model)

    # Predict and save results and metrics
    y_true, y_pred = y, model.predict(X)

    MSE = mean_squared_error(y_true, y_pred)

    print("The MSE of the prediction is {}".format(MSE))

    if opts['-o'] is not None:
        file_plot_path = Path(opts['-o'], model_file.stem + '.eps')
        file_data_path = Path(opts['-o'], model_file.stem + '.csv')

    else:
        root_dir = Path(Path(__file__).parent, 'evaluations', data_file.stem)
        root_dir.mkdir(parents=True, exist_ok=True)

        file_plot_path = Path(root_dir, model_file.stem + '.eps')
        file_data_path = Path(root_dir, model_file.stem + '.csv')

    my_plotter = PlotData()
    my_plotter.generate_curve_plot(weeks, y_true, y_pred)
    my_plotter.save_plot_result(file_plot_path)

    save_data(file_data_path, weeks, y_true, y_pred)
