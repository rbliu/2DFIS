#!/bin/bash 
# --- Start of slurm commands -----------

# Request an hour of runtime:
#SBATCH --time=23:59:59

# Default resources are 1 core with 2.8GB of memory.
# Use more memory (4GB):
#SBATCH -n 24
#SBATCH --mem=90G

# Specify a job name:
#SBATCH -J FRB190417_makeCo

# Specify an output file
# %j is a special variable that is replaced by the JobID when 
# job starts
#SBATCH -o j_FRB190417_makeCo-%j.out
#SBATCH -e j_FRB190417_makeCo-%j.out

#----- End of slurm commands ----
cpunum="24"

module unload intel
module unload python
module load gcc/6.3

source <LSST_V19_ROOT>/loadLSST.bash 
setup lsst_distrib


sed "s/id tract=0/selectId/g" list_jc_i.list > select_i.list

makeCoaddTempExp.py DATA --rerun jointcal_i:coadd2 @select_i.list @patches_i.txt --config doApplyUberCal=True makePsfMatched=True -j ${cpunum} --longlog

