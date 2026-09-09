#!/bin/bash 
# --- Start of slurm commands -----------

# Request an hour of runtime:
#SBATCH --time=5:00:00

# Default resources are 1 core with 2.8GB of memory.
# Use more memory (4GB):
#SBATCH -n 20
#SBATCH --mem=90G

# Specify a job name:
#SBATCH -J FRB190417_mergeCoaddMeas

# Specify an output file
# %j is a special variable that is replaced by the JobID when 
# job starts
#SBATCH -o FRB190417_mergeCoaddMeas-%j.out
#SBATCH -e FRB190417_mergeCoaddMeas-%j.out

#----- End of slurm commands ----
cpunum="20"

module unload intel
module load gcc/6.3 
module unload python

source <LSST_V19_ROOT>/loadLSST.bash 
setup lsst_distrib

mergeCoaddMeasurements.py DATA --rerun coaddMeasure2 --id filter=u2^g2^r2^i3 -C config/mergeCoaddMeasurementsConfig.py -j ${cpunum} --longlog --clobber-config
