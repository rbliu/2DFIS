#!/bin/bash 
# --- Start of slurm commands -----------

# Request an hour of runtime:
#SBATCH --time=6:00:00

# Default resources are 1 core with 2.8GB of memory.
# Use more memory (4GB):
#SBATCH -n 1
#SBATCH --mem=16G

# Specify a job name:
#SBATCH -J CLrot_ingest

# Specify an output file
# %j is a special variable that is replaced by the JobID when 
# job starts
#SBATCH -o j_CLrot_ingest-%j.out
#SBATCH -e j_CLrot_ingest-%j.out

#----- End of slurm commands ----

module unload intel
#module load gcc/6.3 
module unload python
cpunum="1"
source <LSST_V19_ROOT>/loadLSST.bash 
setup lsst_distrib

ingestImages.py DATA rawData/*.fz --mode=link

#processCcd.py DATA @process_g.list --rerun processCcdOutputs -C config/processCcdConfig.py --clobber-config -j ${cpunum} --longlog
