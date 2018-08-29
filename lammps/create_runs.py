"""
Generate multiple runs with different seed numbers for given directory.
Creates any number of runs in a given directory by copying all the files
in the source directory and changing the seed number for the input files.

 >>> python create_runs.py /sim/dir
"""
import os
import sys
import glob
import shutil
from lammps_init import *


simdir = os.path.abspath(sys.argv[1])
n_runs = int(input('Enter number of runs: '))

# All files in the src directory (simdir) will be copied to each run directory
src_files = [os.path.join(simdir, i) for i in os.listdir(simdir) if not os.path.isdir(i)]
print(src_files)

# Input file format (change if input file is named differently)
in_file = os.path.basename(glob.glob(os.path.join(simdir, 'in.*'))[0])

seed = 223456
for run in range(1, n_runs + 1):
    print('%s -> %s' % (simdir, run))

    # Create run directory
    rundir = os.path.join(simdir, str(run))
    os.makedirs(rundir, exist_ok=True)

    # Copy all files from src directory to run directory
    for f in src_files:
        shutil.copy(f, rundir)

    # Change seed number
    in_lines = read_lines(os.path.join(rundir, in_file))
    in_lines = change_seed(in_lines, seed=seed)
    write_lines(in_lines, os.path.join(rundir, in_file))
    seed += 1

# Delete source files
cleanup = input('Delete source files? (y/n): ')
cleanup = {'y': True, 'n': False}[cleanup]
if cleanup:
    for f in src_files:
        os.remove(f)
print('Done!')
