"""
Initialize RASPA input files for MOFs that make up an interpenetrated MOF.
Looks at the IPMOF name and separates the two MOFs and creates input files for these MOFs.
"""
import os
import glob
import shutil
import yaml
import numpy as np
from raspa_input import write_raspa_file
from raspa_slurm import write_raspa_slurm
from ipmof.crystal import MOF


CORE_DIR = '/home/kutay/Documents/Research/MOFs/CORE_ALL'
CONFIG = '../config/raspa_config_h2.yaml'


def calculate_replication(mof, cutoff=12):
    mof.calculate_vectors()
    cell = [np.linalg.norm(i) for i in mof.uc_vectors]
    return [int(np.ceil(cutoff * 2 / i)) for i in cell]


with open(CONFIG, 'r') as rc:
    raspa_config = yaml.load(rc)


mofs_done = []
for cif in os.listdir(raspa_config['mof_dir']):
    mofs = cif.split('_')[:2]
    for mof_name in mofs:
        if mof_name not in mofs_done:
            sim_dir = os.path.join(raspa_config['raspa_dir'], mof_name)
            possible_cifs = glob.glob(os.path.join(CORE_DIR, '%s*.cif' % mof_name))
            for cif_file in possible_cifs:
                # Create new directory
                os.makedirs(sim_dir, exist_ok=True)

                # Write input file
                inp_file = os.path.join(sim_dir, 'simulation.input')
                mof_config = raspa_config.copy()
                mof_config['framework'] = os.path.splitext(os.path.basename(cif_file))[0]
                mof_obj = MOF(cif_file)
                mof_config['unitcell'] = calculate_replication(mof_obj, cutoff=13)
                write_raspa_file(inp_file, mof_config)

                # Write RASPA job submission file
                job_file = os.path.join(sim_dir, 'job.raspa')
                write_raspa_slurm(job_file, '%s-%i-%i' % (mof_name, raspa_config['pressure'], raspa_config['temperature']),
                                  walltime='24:00:00', cleanup=raspa_config['cleanup'],
                                  storage=raspa_config['storage'], storage_dir=raspa_config['storage_dir'])

                # Copy MOF file
                shutil.copy(cif_file, sim_dir)

                mofs_done.append(mof_name)
