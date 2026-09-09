#!/bin/bash 
# --- Start of slurm commands -----------

# Request an hour of runtime:
#SBATCH --time=23:00:00

# Default resources are 1 core with 2.8GB of memory.
# Use more memory (4GB):
#SBATCH -n 24
#SBATCH --mem=90G

# Specify a job name:
#SBATCH -J FRB190417_assemCo

# Specify an output file
# %j is a special variable that is replaced by the JobID when 
# job starts
#SBATCH -o j_FRB190417_assemCo-%j.out
#SBATCH -e j_FRB190417_assemCo-%j.out

#----- End of slurm commands ----
cpunum="24"

module unload intel
module unload python
module load gcc/6.3

source <LSST_V19_ROOT>/loadLSST.bash 
setup lsst_distrib


assembleCoadd.py --warpCompare DATA --rerun coadd2 @select_r.list @patches_r.txt -j ${cpunum} --longlog
#assembleCoadd.py --warpCompare DATA --rerun coadd @select_z.list @patches_z.txt -j ${cpunum} --longlog
#assembleCoadd.py --warpCompare DATA --rerun coadd @select_i.list @patches_i.txt -j ${cpunum} --longlog
#assembleCoadd.py --warpCompare DATA --rerun coadd @select_u.list @patches_u.txt -j ${cpunum} --longlog
