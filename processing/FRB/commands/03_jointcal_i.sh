#!/bin/bash 
# --- Start of slurm commands -----------

# Request an hour of runtime:
#SBATCH --time=32:00:00

# Default resources are 1 core with 2.8GB of memory.
# Use more memory (4GB):
#SBATCH -n 10
#SBATCH --mem=90G

# Specify a job name:
#SBATCH -J FRB190417_jc_i

# Specify an output file
# %j is a special variable that is replaced by the JobID when 
# job starts
#SBATCH -o j_FRB190417_jc_i-%j.out
#SBATCH -e j_FRB190417_jc_i-%j.out

#----- End of slurm commands ----

cpunum="10"

module unload intel
module unload python
module load gcc/6.3

source <LSST_V19_ROOT>/loadLSST.bash 
setup lsst_distrib


sed "s/id /id tract=0 /g" list_process_i.list > list_jc_i.list

jointcal.py DATA --rerun coadd:jointcal_i -C config/jointcal_config.py @list_jc_i.list -j ${cpunum} --clobber-config --longlog


#sed 's/id/selectId/g' glist > select_g.list
#sed 's/id/selectId/g' rlist > select_r.list
#sed 's/id/selectId/g' process_u.list > select_u.list
#sed 's/id/selectId/g' process_i.list > select_i.list
#sed 's/id/selectId/g' process_z.list > select_z.list
