"""
Cleanup RASPA simulation outputs.

Cleanup simulation files and copy output file to simulation directory
>>> python raspa_cleanup.py sim_dir

Cleanup simulation files and copy output file to given second directory (copy_dir)
>>> python raspa_cleanup.py sim_dir copy_dir
"""
import os
import sys
import shutil
import glob


working_dir = sys.argv[1]
if len(sys.argv) > 2:
    out_dir = sys.argv[2]
else:
    out_dir = working_dir

output_file = glob.glob(os.path.join(working_dir, 'Output', 'System_0', '*.data'))[0]
shutil.copy(output_file, os.path.join(out_dir, 'raspa_out.data'))
to_remove = ['Output', 'Restart', 'Movies', 'VTK', 'out.raspa']

for out_file in to_remove:
    out_file = os.path.join(working_dir, out_file)
    if os.path.exists(out_file):
        if os.path.isdir(out_file):
            shutil.rmtree(out_file)
        else:
            os.remove(out_file)
