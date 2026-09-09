#!/bin/bash 
# --- Start of slurm commands -----------

# Request an hour of runtime:
#SBATCH --time=6:00:00

# Default resources are 1 core with 2.8GB of memory.
# Use more memory (4GB):
#SBATCH -n 20
#SBATCH --mem=64G

# Specify a job name:
#SBATCH -J CLrot_proc

# Specify an output file
# %j is a special variable that is replaced by the JobID when 
# job starts
#SBATCH -o j_CLrot_proc-%j.out
#SBATCH -e j_CLrot_proc-%j.out

#----- End of slurm commands ----

module unload intel
module load gcc/6.3 
module unload python
cpunum="20"
source <LSST_V19_ROOT>/loadLSST.bash 
setup lsst_distrib


#processCcd.py DATA --rerun processCcdOutputs --id --show data
processCcd.py DATA @list_process_i.list --rerun processCcdOutputs_noct -C config/processCcdConfig.py --clobber-config -j ${cpunum} --longlog
#processCcd.py DATA --rerun processCcdOutputs --id visit=2785487 ccd=12 -C config/processCcdConfig.py --clobber-config -j ${cpunum} --longlog
