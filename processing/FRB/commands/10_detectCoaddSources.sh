#!/bin/bash 
# --- Start of slurm commands -----------

# Request an hour of runtime:
#SBATCH --time=24:00:00

# Default resources are 1 core with 2.8GB of memory.
# Use more memory (4GB):
#SBATCH -n 24
#SBATCH --mem=100G

# Specify a job name:
#SBATCH -J FRB190417_detCo

# Specify an output file
# %j is a special variable that is replaced by the JobID when 
# job starts
#SBATCH -o FRB190417_detCo-%j.out
#SBATCH -e FRB190417_detCo-%j.out

#----- End of slurm commands ----
cpunum="24"

module unload intel
module load gcc/6.3 
module unload python

source <LSST_V19_ROOT>/loadLSST.bash 
setup lsst_distrib

detectCoaddSources.py DATA --rerun coadd2:coaddMeasure @patches_g.txt -j ${cpunum} --longlog
detectCoaddSources.py DATA --rerun coadd2:coaddMeasure @patches_r.txt -j ${cpunum} --longlog
detectCoaddSources.py DATA --rerun coadd2:coaddMeasure @patches_i.txt -j ${cpunum} --longlog
detectCoaddSources.py DATA --rerun coadd2:coaddMeasure @patches_u.txt -j ${cpunum} --longlog
#detectCoaddSources.py DATA --rerun coadd:coaddMeasure @patches_u.txt -j ${cpunum} --longlog
