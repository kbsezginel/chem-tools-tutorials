"""
Convert symmetry to P1 and fill unit cell for given cif file.

Usage:
python fill_unit_cell.py non-P1.cif P1.cif
"""
import os
import sys
import subprocess


def read_space_group(cif_file):
    """
    Read space group from cif file.
    """
    space_group = None
    with open(cif_file, 'r') as cif:
        cif_lines = cif.readlines()
    for line in cif_lines:
        if 'space_group_name_H-M' in line:
            space_group = line.split("'")[1]
            break
    if space_group is not None:
        return space_group
    else:
        print('Space group not found')


def obabel_fill_unit_cell(cif_file, p1_file):
    """
    Convert symmetry to P1 using openbabel.
    """
    subprocess.run(['obabel', '-icif', cif_file, '-ocif', '-O', p1_file, '--fillUC', 'strict'])


cif_file = sys.argv[1]
p1_file = sys.argv[2]
sg = read_space_group(cif_file)
print('Converting %s with space group: %s' % (cif_file, sg))
obabel_fill_unit_cell(cif_file, p1_file)
sg = read_space_group(p1_file)
print('%s created with space group: %s' % (p1_file, sg))
