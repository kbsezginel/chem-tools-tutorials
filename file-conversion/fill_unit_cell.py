"""
Convert symmetry to P1 and fill unit cell for given cif file using OpenBabel.

Usage:
python fill_unit_cell.py non-P1.cif P1.cif
"""
import os
import sys
import subprocess


def obabel_fill_unit_cell(cif_file, p1_file):
    """
    Convert symmetry to P1 using openbabel.
    """
    subprocess.run(['obabel', '-icif', cif_file, '-ocif', '-O', p1_file, '--fillUC', 'strict'])


cif_file = os.path.abspath(sys.argv[1])
p1_file = os.path.abspath(sys.argv[2])
print('Converting %s to P1' % cif_file)
obabel_fill_unit_cell(cif_file, p1_file)
print('Done! -> %s' % p1_file)
