"""
Generates RASPA job submission file for slurm scheduler.
"""
# Author: Kutay B. Sezginel
# Date: Nov 2017


def write_raspa_slurm(slurm_file, jobname, walltime="24:00:00"):
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
            "echo JOB_ID: $SBATCH_JOBID JOB_NAME: $SBATCH_JOB_NAME\n" +
            "echo start_time: `date`\n" +
            "cd $SLURM_SUBMIT_DIR\n\n" +
            "simulate simulation.input\n\n" +
            "echo end_time: `date`\n" +
            "exit\n")
