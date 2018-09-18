"""
Cleanup RASPA simulation outputs.
"""
import os
import sys
import shutil
import glob


working_dir = sys.argv[-1]
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
