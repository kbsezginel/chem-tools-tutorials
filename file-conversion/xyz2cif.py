"""
Convert xyz file to cif file with a defined cell.
The cell dimensions are entered as input.
Currently, only works for orthogonal cells.

Usage:
 >>> python xyz2cif.py mymolecule.xyz
"""
import os
import sys
import glob


def read_xyz(file_name):
    """ Read single or multiple xyz formatted molecules

    Args:
        - file_name (str): Path to the xyz file

    Returns:
        - list: list of dictionaries with 'atoms' and 'coordinates' keys for each molecule in xyz file
     """
    with open(file_name, 'r') as f:
        xyz_lines = f.readlines()
    mol_start = []
    mol_idx = 0
    for line_idx, line in enumerate(xyz_lines):
        if len(line.split()) == 1 and line.split()[0].isdigit() and line_idx != mol_idx + 1:
            mol_idx = line_idx
            mol_start.append(mol_idx)
    mol_start.append(len(xyz_lines))
    molecules = []
    for i in range(len(mol_start) - 1):
        mol_lines = xyz_lines[mol_start[i] + 2:mol_start[i + 1]]
        molecule = dict(atoms=[], coordinates=[])
        for line in mol_lines:
            molecule['atoms'].append(line.split()[0])
            molecule['coordinates'].append([float(i) for i in line.split()[1:4]])
        molecules.append(molecule)
    return molecules


def write_cif(file_name, atoms, coordinates, header='mol', cell=[1, 1, 1, 90, 90, 90], fractional=False, spacegroup='P1'):
    """ Write given atomic coordinates to file in cif format """
    with open(file_name, 'w') as cif_file:
        cif_file.write('data_%s\n' % header)
        cif_file.write('_cell_length_a                   %7.4f\n' % cell[0])
        cif_file.write('_cell_length_b                   %7.4f\n' % cell[1])
        cif_file.write('_cell_length_c                   %7.4f\n' % cell[2])
        cif_file.write('_cell_angle_alpha                %7.4f\n' % cell[3])
        cif_file.write('_cell_angle_beta                 %7.4f\n' % cell[4])
        cif_file.write('_cell_angle_gamma                %7.4f\n' % cell[5])
        cif_file.write("_symmetry_space_group_name_Hall  '%s'\n" % spacegroup)
        cif_file.write("_symmetry_space_group_name_H-M   '%s'\n" % spacegroup)
        cif_file.write('loop_\n')
        cif_file.write('_atom_site_label\n')
        cif_file.write('_atom_site_type_symbol\n')
        cif_file.write('_atom_site_fract_x\n')
        cif_file.write('_atom_site_fract_y\n')
        cif_file.write('_atom_site_fract_z\n')
        cif_format = '%s%-4i %2s %7.4f %7.4f %7.4f\n'
        if fractional:
            coordinates = fractional_coordinates(coordinates, cell=cell[:3])
        for i, (atom, coor) in enumerate(zip(atoms, coordinates)):
            cif_file.write(cif_format % (atom, i, atom, coor[0], coor[1], coor[2]))


def fractional_coordinates(coordinates, cell=[1, 1, 1]):
    """ Convert cartesian coordinates to fractional coordinates (ONLY ORTHOGONAL CELLS!) """
    frac_coor = []
    for coor in coordinates:
        frac_coor.append([cr / cl for (cr, cl) in zip(coor, cell)])
    return frac_coor


####################################################################################################
xyz_file = os.path.abspath(sys.argv[1])
cell = input('Please enter cell [a b c alpha beta gamma]: ')
cif_file = input('Please enter output cif file name: ')


cell = [float(i) for i in cell.split()]
packed_xyz = read_xyz(xyz_file)[0]
write_cif(cif_file, packed_xyz['atoms'], packed_xyz['coordinates'], cell=cell, fractional=True)
print('Saved -> %s' % cif_file)
