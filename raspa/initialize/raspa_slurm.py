"""
Generates RASPA job submission file for slurm scheduler.
"""
# Author: Kutay B. Sezginel
# Date: Nov 2017


def write_raspa_slurm(slurm_file, jobname, walltime="24:00:00", cleanup=False, storage=False,
                      scripts_dir='/ihome/cwilmer/kbs37/git/chem-tools-tutorials/raspa',
                      storage_dir='/zfs1/cwilmer/kbs37/RASPA/IPMOF/298K'):
    """
    Writes RASPA slurm file for simulating gas adsorption.
    Arguments:
        - slurm_file (str)     : path to slurm file.
        - job_name (str)       : Slurm job name
        - walltime (str)       : Slurm job max. wall time
    """
    with open(slurm_file, "w") as raspa_slurm_file:
        raspa_slurm_file.write(
            "#!/bin/bash\n" +
            "#SBATCH --nodes=1\n" +
            "#SBATCH --ntasks-per-node=1\n" +
            "#SBATCH --cluster=smp\n" +
            "#SBATCH --time=%s\n" % walltime +
            "#SBATCH --job-name=%s\n" % jobname +
            "#SBATCH --output=out.raspa\n\n" +
            ". /ihome/cwilmer/kbs37/venv/ipmof/bin/activate\n" +
            "echo JOB_ID: $SLURM_JOB_ID JOB_NAME: $SLURM_JOB_NAME\n" +
            "echo start_time: `date`\n" +
            "cd $SLURM_SUBMIT_DIR\n\n" +
            "simulate simulation.input\n\n")
        if cleanup:
            raspa_slurm_file.write("scriptsdir='%s'\n" % scripts_dir)
            if not storage:
                raspa_slurm_file.write("python $scriptsdir/raspa_cleanup.py .\n\n")
        if storage:
            raspa_slurm_file.write(
                "storagedir='%s'\n" % storage_dir +
                "simstorage=$storagedir/$SLURM_JOB_NAME\n" +
                "mkdir -p $simstorage\n" +
                "python $scriptsdir/raspa_cleanup.py . $simstorage\n\n")
        raspa_slurm_file.write(
            "echo end_time: `date`\n" +
            "exit\n")
