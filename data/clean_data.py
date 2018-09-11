"""Clean Data.

Usage:
  ./clean_data.py -i <file> -o <dir> [--instances <n>] [--overlap <f>]

Options:
  -i <file>              Evaluate dataset path
  -o <dir>               Directory where the evaluation plot result will be
                         saved
  --instances <n>        Number of instances to generate from data [default: 1]
  --overlap <f>          Percentage of overlapping between the instances.
                         [default: 0]
"""

from data.data_cleaner import DataCleaner
from docopt import docopt
from pathlib import Path


if __name__ == '__main__':
    opts = docopt(__doc__)

    out_dir = Path(opts['-o'])
    in_file = Path(opts['-i'])

    instances = int(opts['--instances'])
    overlap = float(opts['--overlap'])

    out_dir.mkdir(parents=True, exist_ok=True)

    print("Cleaning data from {} and saving {} instances\
 with {} overlapping".format(in_file, instances, overlap))
    dc = DataCleaner(in_file, out_dir)
    dc.clean(instances, overlap)
