"""Clean Data.

Usage:
  ./clean_data.py -i <file> -o <dir> [--p_eval <float>] [--instances <n>] [--overlap <f>]

Options:
  -i <file>              Evaluate dataset path
  -o <dir>               Directory where the evaluation plot result will be
                         saved
  --p_eval <float>       Percentage to evaluation dataset. [default: 0.2]
  --instances <n>        Number of instances to generate from data [default: 1]
  --overlap <f>          Percentage of overlapping between the instances.
                         [default: 0]
"""

from data.data_cleaner import DataCleaner
from docopt import docopt
from pathlib import Path


class InstancesHasNotValidationData(Exception):
    pass


if __name__ == '__main__':
    opts = docopt(__doc__)

    out_dir = Path(opts['-o'])
    in_file = Path(opts['-i'])

    p_eval = float(opts['--p_eval'])
    instances = int(opts['--instances'])
    overlap = float(opts['--overlap'])

    if instances > 1 and p_eval > 0:
        raise InstancesHasNotValidationData('If you want to generate instances,\
 all the dataset will be used')

    print("Cleaning data from {} and saving {} instances\
 with {} overlapping and {} reserved to evaluation".format(in_file,
                                                           instances,
                                                           overlap,
                                                           p_eval))
    dc = DataCleaner(in_file, out_dir)
    dc.clean(instances, overlap)
    dc.train_test_split(p_eval)
