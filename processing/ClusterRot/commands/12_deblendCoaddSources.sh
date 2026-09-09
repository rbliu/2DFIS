#!/bin/bash 
# --- Start of slurm commands -----------

# Request an hour of runtime:
#SBATCH --time=16:00:00

# Default resources are 1 core with 2.8GB of memory.
# Use more memory (4GB):
#SBATCH -n 24
#SBATCH --mem=150G

# Specify a job name:
#SBATCH -J CLrot_deblend

# Specify an output file
# %j is a special variable that is replaced by the JobID when 
# job starts
#SBATCH -o CLrot_deblend-%j.out
#SBATCH -e CLrot_deblend-%j.out

#----- End of slurm commands ----
cpunum="24"

module unload intel
module load gcc/6.3 
module unload python

source <LSST_V19_ROOT>/loadLSST.bash 
setup lsst_distrib

deblendCoaddSources.py DATA --rerun coaddMeasure @patches_g.txt -j ${cpunum} --longlog
deblendCoaddSources.py DATA --rerun coaddMeasure @patches_r.txt -j ${cpunum} --longlog
deblendCoaddSources.py DATA --rerun coaddMeasure @patches_i.txt -j ${cpunum} --longlog
deblendCoaddSources.py DATA --rerun coaddMeasure @patches_u.txt -j ${cpunum} --longlog
