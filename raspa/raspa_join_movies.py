"""
Join RASPA movie output pdb files for the adsorbent and adsorbate.

Example: python raspa_join_movies.py framework.pdb adsorbate.pbd

Typical RASPA movie output names:
- framework: Framework_0_final.pdb
- adsorbate: Movie_IRMOF-1_2.2.2_298.000000_10.000000_component_CH4_0.pdb
"""
import os
import sys


filename = 'movies_joined.pdb'
framework = os.path.abspath(sys.argv[1])
component = os.path.abspath(sys.argv[2])

with open(framework, 'r') as fil:
    framework_lines = fil.readlines()

# Assuming there are only two extra lines other than atomic coordinates (remarks and crystal cell)
n_framework_atoms = len(framework_lines) - 2

with open(component, 'r') as fil:
    component_lines = fil.readlines()

i = 0
for line in component_lines:
    if line[:4] == 'ATOM':
        i += 1
        atom_idx = str(n_framework_atoms + i)
        new_line = line[:11 - len(atom_idx)] + atom_idx + line[11:]
        framework_lines.append(new_line)

with open(filename, 'w') as fil:
    for line in framework_lines:
        fil.write(line)
print('Saved as -> %s' % filename)
