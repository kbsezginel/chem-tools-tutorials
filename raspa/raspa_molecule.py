"""
Generates molecule definition files for RASPA.

Usage:
 >>> python raspa_molecule.py molecule.xyz [molecule.def]

The second argument is optional. If not given a .def file with the same name as the molecule file
will be written in the same directory with the molecule file.
"""
# Author: Kutay B. Sezginel
# Date: May 2018
from angstrom import Molecule
import os
import sys


def write_raspa_molecule(molecule, raspa_molecule_file, code='drg', properties=None):
    """
    Write RASPA molecule definition file (rigid molecule):
    - Molecule: Angstrom Molecule object
        - coordinates: list of atomic positions -> [[x1, y1, z1], [x2, y2, z2], ...]
        - elements: list of atom names          -> ['C', 'O', ...]
        - bonds: list of bonds                  -> [[0, 1], [0, 2], [1, 5], ...]
    - raspa_molecule_file: File name for .def file

    Optional arguments:
    - code: force field code for RASPA    -> 'drg'
    - properties: molecule properties as  -> [critical_temperature, critical_pressure, accentric_factor]
    """
    if properties is None:
        t_critical = 550
        p_critical = 2600000.0
        acentric_factor = 0.38
    else:
        t_critical, p_critical, acentric_factor = properties

    mol_name = os.path.basename(raspa_molecule_file).split('.')[0]
    elements, coordinates, bonds = molecule.atoms, molecule.coordinates, molecule.bonds
    with open(raspa_molecule_file, 'w') as rm:
        rm.write(
            "# critical constants: Temperature [T], Pressure [Pa], and Acentric factor [-]\n" +
            "%.4f\n%.1f\n%.4f\n" % (t_critical, p_critical, acentric_factor) +
            "# Number of Atoms\n%i\n" % len(elements) +
            "# Number of Groups\n1\n# %s-group\nrigid\n" % mol_name +
            "# Number of Atoms\n%i\n# Atomic Positions\n" % len(elements)
        )
        for i, (atom, coor) in enumerate(zip(elements, coordinates)):
            rm.write('%2i %2s_%3s % 5.4f % 5.4f % 5.4f\n' % (i, atom, code, coor[0], coor[1], coor[2]))

        rm.write(
            "# Chiral centers Bond  BondDipoles Bend  UrayBradley InvBend  Torsion Imp." +
            " Torsion Bond/Bond Stretch/Bend Bend/Bend Bend/Torsion IntraVDW IntraCoulomb\n" +
            "               0  %3i            0    0            0       0            0" % len(bonds) +
            "             0            0         0         0       0        0            0\n" +
            "# Bond stretch: atom n1-n2, type, parameters\n"
        )
        # Write bonds
        for b in bonds:
            rm.write("%2i %2i RIGID_BOND\n" % (b[0], b[1]))
        rm.write("# Number of config moves\n0\n")


mol_file = os.path.abspath(sys.argv[1])
print('Reading -> %s' % mol_file)
mol = Molecule(read=mol_file)
mol.get_bonds()

if len(sys.argv) > 2:
    mol_name = os.path.basename(sys.argv[2]).split('.')[0]
    raspa_molecule_file = os.path.abspath(sys.argv[2])
else:
    mol_name = os.path.basename(mol_file).split('.')[0]
    raspa_molecule_file = os.path.join(os.path.split(mol_file)[0], '%s.def' % mol_name)

print('Writing -> %s' % raspa_molecule_file)
write_raspa_molecule(mol, raspa_molecule_file)
