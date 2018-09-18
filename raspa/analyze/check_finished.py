"""
Read RASPA simulations
"""
import os
import sys
import glob
import yaml
from raspa_output import parse_output

run_dir = sys.argv[1]
results_file = '%s_results.yaml' % os.path.basename(os.path.abspath(run_dir))
finished, warnings = 0, 0
all_results = []
n_mofs = len(os.listdir(run_dir))
for i, mof in enumerate(os.listdir(run_dir)):
    print('\rReading results... %3i / %3i' % (i + 1, n_mofs), end='')
    mof_dir = os.path.join(run_dir, mof)
    ads_path = glob.glob(os.path.join(mof_dir, 'Output', 'System_0', '*.data'))[0]
    results = parse_output(ads_path, verbose=False, save=False)
    all_results.append(results)
    if results['finished'] == True:
        finished += 1
    if len(results['warnings']) > 0:
        warnings += 1

print('%i / %i finished' % (finished, n_mofs))
print('%i / %i warnings' % (warnings, n_mofs))

with open(results_file, 'w') as resfile:
    yaml.dump(all_results, resfile)
print('Results saved -> %s' % (results_file))
