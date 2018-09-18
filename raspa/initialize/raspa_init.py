"""
Initialize RASPA input files.
"""
import os
import shutil
import yaml
import numpy as np
from raspa_input import write_raspa_file
from raspa_slurm import write_raspa_slurm
from ipmof.crystal import MOF


MOF_DIR = '/home/kutay/Documents/Research/InnoCentive-H2-Storage/IPMOFs'
RASPA_DIR = '/home/kutay/Documents/Research/InnoCentive-H2-Storage/RASPA'
CONFIG = '../config/raspa_config_h2.yaml'
CLEANUP = True
STORAGE = True


def calculate_replication(mof, cutoff=12):
    mof.calculate_vectors()
    cell = [np.linalg.norm(i) for i in mof.uc_vectors]
    return [int(np.ceil(cutoff * 2 / i)) for i in cell]


with open(CONFIG, 'r') as rc:
    raspa_config = yaml.load(rc)


for cif in os.listdir(MOF_DIR):
    mof_name = os.path.splitext(cif)[0]
    sim_dir = os.path.join(RASPA_DIR, mof_name)
    cif_file = os.path.join(MOF_DIR, cif)

    # Create new directory
    os.makedirs(sim_dir, exist_ok=True)

    # Write input file
    inp_file = os.path.join(sim_dir, 'simulation.input')
    mof_config = raspa_config.copy()
    mof_config['framework'] = mof_name
    mof_obj = MOF(cif_file)
    mof_config['unitcell'] = calculate_replication(mof_obj, cutoff=13)
    write_raspa_file(inp_file, mof_config)

    # Write RASPA job submission file
    job_file = os.path.join(sim_dir, 'job.raspa')
    write_raspa_slurm(job_file, '%s' % (mof_name), walltime='24:00:00', cleanup=CLEANUP, storage=STORAGE)

    # Copy MOF file
    sim_cif = os.path.join(sim_dir, cif)
    shutil.copy(cif_file, sim_cif)

    # Copy pseudo atoms file
    # shutil.copy('pseudo_atoms.def', sim_dir)
