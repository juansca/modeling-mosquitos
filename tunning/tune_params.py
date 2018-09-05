"""Tune parameters for given models.

Usage:
  tune_params.py --model <name>

Options:
  --model <name>           model name to tune params.
                           Options: svr, rdmforest, pcardmforest, dtr, knnr,
                           mlpr, svr, pcaknnr, pcadtr, linear, ridge.
                           If you want to tune all the models together, just
                           put on this parameter 'all'.
  --help                   show this screen
"""

from docopt import docopt
from pathlib import Path
import pandas as pd
from rpy2.robjects import pandas2ri
from rpy2.robjects import default_converter
from rpy2.robjects.conversion import localconverter
from rpy2.robjects import r
import subprocess


SCENARIO = "/.scenario"
PARAMS = "parameters/"
LOG = "results/{}.Rdata"


def create_command(scenario_path: Path, param_path: Path, log_file: Path):
    cmd = "irace -s {} -p {} -l {};".format(scenario_path.as_posix(),
                                            param_path.as_posix(),
                                            log_file.as_posix())

    return cmd


def tune_model(scenario, params, log):
    irace_command = create_command(scenario, params, log)

    # Run irace
    process = subprocess.Popen(irace_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    # Load the irace output and transdorm it to a csv file
    pandas2ri.activate()

    r.load(log.as_posix())

    r.library('irace')

    b = r.getFinalElites(r.iraceResults, n=0)

    with localconverter(default_converter + pandas2ri.converter):
        r_pd_params = b

    out_csv = Path(log.stem, '.csv')
    r_pd_params.to_csvfile(out_csv.as_posix(), sep=',')

    # Import to pandas to pythonic cleaning
    py_pd_params = pd.read_csv(out_csv)
    py_pd_params = py_pd_params.drop(['.ID.', '.PARENT.'])

    # Giving the correct order to rows
    correct_table = {}
    for c in py_pd_params.columns:
        rows = []
        for j in py_pd_params[c].keys():
            rows.append(py_pd_params[c][j])
            print(py_pd_params[c][j])
        correct_table[c] = rows

    correct_table = pd.DataFrame(data=correct_table)
    correct_table.to_csv(out_csv)


if __name__ == "__main__":
    opts = docopt(__doc__)

    model = opts['--model'].lower()

    scenario = Path(SCENARIO)

    if model == 'all':
        for model in Path(PARAMS).glob('*'):
            params = Path(PARAMS, model)
            log = Path(LOG.format(model))
            print("Tunning hyperparameters for {}".format(model))
            tune_model(scenario, params, log)
    else:
        params = Path(PARAMS.format(model))
        log = Path(LOG.format(model))

        print("Tunning hyperparameters for {}".format(model))
        tune_model(scenario, params, log)

    print('Hyperparameters succesfully tunned!')
