"""
Functions to write atomic coordinates in commmon chemical formats.
"""
import os


def write_pdb(file_name, atoms, coordinates, header='mol'):
    """ Write given atomic coordinates to file in pdb format """
    with open(file_name, 'w') as pdb_file:
        pdb_file.write('HEADER    ' + header + '\n')
        format = 'HETATM%5d%3s  MOL     1     %8.3f%8.3f%8.3f  1.00  0.00          %2s\n'
        for atom_index, (atom_name, atom_coor) in enumerate(zip(atoms, coordinates), start=1):
            x, y, z = atom_coor
            pdb_file.write(format % (atom_index, atom_name, x, y, z, atom_name.rjust(2)))
        pdb_file.write('END\n')


def write_xyz(file_name, atoms, coordinates, header='mol'):
    """ Write given atomic coordinates to file in xyz format """
    with open(file_name, 'w') as xyz_file:
        xyz_file.write(str(len(coordinates)) + '\n')
        xyz_file.write(header + '\n')
        format = '%s %.4f %.4f %.4f\n'
        for atom, coor in zip(atoms, coordinates):
            xyz_file.write(format % (atom, coor[0], coor[1], coor[2]))


def write_cif(file_name, atoms, coordinates, header='mol', cell=[1, 1, 1, 90, 90, 90]):
    """ Write given atomic coordinates to file in cif format """
    with open(file_name, 'w') as cif_file:
        cif_file.write('data_%s\n' % header)
        cif_file.write('_cell_length_a                  %7.4f\n' % cell[0])
        cif_file.write('_cell_length_b                  %7.4f\n' % cell[1])
        cif_file.write('_cell_length_c                  %7.4f\n' % cell[2])
        cif_file.write('_cell_angle_alpha               %7.4f\n' % cell[3])
        cif_file.write('_cell_angle_beta                %7.4f\n' % cell[4])
        cif_file.write('_cell_angle_gamma               %7.4f\n' % cell[5])
        cif_file.write('loop_\n')
        cif_file.write('_atom_site_label\n')
        cif_file.write('_atom_site_type_symbol\n')
        cif_file.write('_atom_site_fract_x\n')
        cif_file.write('_atom_site_fract_y\n')
        cif_file.write('_atom_site_fract_z\n')
        cif_format = '%s%-4i %2s %7.4f %7.4f %7.4f\n'
        for i, (atom, coor) in enumerate(zip(atoms, coordinates)):
            cif_file.write(cif_format % (atom, i, atom, coor[0], coor[1], coor[2]))
