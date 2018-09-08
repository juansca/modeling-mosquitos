#!/usr/bin/env python3

###############################################################################
# This script is the command that is executed every run.
# Check the examples in examples/
#
# This script is run in the execution directory (execDir, --exec-dir).
#
# PARAMETERS:
# argv[1] is the candidate configuration number
# argv[2] is the instance ID
# argv[3] is the seed
# argv[4] is the instance name
# The rest (argv[5:]) are parameters to the run
#
# RETURN VALUE:
# This script should print one numerical value: the cost that must be minimized.
# Exit with 0 if no error, with 1 in case of error
###############################################################################

import datetime
import os.path
import os
import re
import subprocess
import sys

# FIXME: group together everything that needs to be edited by the user and put
# in functions everything that does NOT to be edited.

# This example is for the ACOTSP software. Compare it with
# examples/acotsp/target-runner
# exe = "~/bin/executable"
ROOT_DIR = os.getcwd()
exe = os.path.join(ROOT_DIR, "model_tunner.py")
fixed_params = ""


# This is an example of reading a number from the output.
def parse_output(out):
    match = re.search(r'[-+0-9.eE]+', out.strip())
    if match:
        return match.group(0)
    else:
        return "No match"


def target_runner_error(msg):
    now = datetime.datetime.now()
    print(str(now) + " error: " + msg)
    sys.exit(1)


def check_executable(fpath):
    fpath = os.path.expanduser(fpath)
    if not os.path.isfile(fpath):
        target_runner_error(str(fpath) + " not found")
    if not os.access(fpath, os.X_OK):
        target_runner_error(str(fpath) + " is not executable")


def touch(path):
    with open(path, 'a'):
        os.utime(path, None)


def create_out_err_files(candidate_id, instance_id):
    out_components = ["c", str(candidate_id), "-",
                      str(instance_id), ".stdout"]
    out_file = ''.join(out_components)

    error_components = ["c", str(candidate_id), "-",
                        str(instance_id), ".stderr"]
    error_file = ''.join(error_components)

    touch(out_file)
    touch(error_file)
    if not os.path.isfile(out_file):
        target_runner_error("output file {} not found.".format(out_file))

    if not os.path.isfile(error_file):
        target_runner_error("Error file {} not found.".format(error_file))

    return out_file, error_file


def create_command(exe, fixed_params, instance, cand_params):
    cmd = [exe] + fixed_params.split() + ["-i"] + cand_params

    return cmd


if len(sys.argv) < 5:
    print("\nUsage: ./target-runner.py <candidate_id> <instance_id> <instance_path_name> <list of parameters>\n")
    sys.exit(1)


# Get the parameters as command line arguments.
candidate_id = sys.argv[1]
instance_id = sys.argv[2]
instance = sys.argv[3]
cand_params = sys.argv[4:]


# Check the executable file
exe = os.path.expanduser(exe)
check_executable(exe)


# Define the stdout and stderr files and check it.
out_file, err_file = create_out_err_files(candidate_id, instance_id)


# Build the command, run it and save the output to a file,
# to parse the result from it.
#
# Stdout and stderr files have to be opened before the call().
#
# Exit with error if something went wrong in the execution.

command = create_command(exe, fixed_params, instance, cand_params)

with open(out_file, 'w') as outf:
    with open(err_file, 'w') as errf:
        return_code = subprocess.call(command, stdout=outf, stderr=errf)
        outf.close()
        errf.close()

if return_code != 0:
    target_runner_error("command returned code " + str(return_code))


with open(out_file, 'r') as of:
    cost = parse_output(of.read())

print(cost)

os.remove(out_file)
os.remove(err_file)
sys.exit(0)
