#!/bin/bash
# --- Start of slurm commands -----------

# Request an hour of runtime:
#SBATCH --time=17:00:00

# Default resources are 1 core with 2.8GB of memory.
# Use more memory (4GB):
#SBATCH -n 20
#SBATCH --mem=90G

# Specify a job name:
#SBATCH -J FRB_fp

# Specify an output file
# %j is a special variable that is replaced by the JobID when
# job starts
#SBATCH -o FRB_fp-%j.out
#SBATCH -e FRB_fp-%j.out

#----- End of slurm commands ----
cpunum="20"

module unload intel
module load gcc/6.3
module unload python

source <LSST_V19_ROOT>/loadLSST.bash
setup lsst_distrib

ls DATA/rerun/coaddMeasure2/deepCoadd-results/g2/0/ > patches_g_forcedPhotCoadd.txt
sed -i "s/^/--id filter=g2 tract=0 patch=/g" patches_g_forcedPhotCoadd.txt
sed -i 's|'/'||g' patches_g_forcedPhotCoadd.txt
ls DATA/rerun/coaddMeasure2/deepCoadd-results/r2/0/ > patches_r_forcedPhotCoadd.txt
sed -i "s/^/--id filter=r2 tract=0 patch=/g" patches_r_forcedPhotCoadd.txt
sed -i 's|'/'||g' patches_r_forcedPhotCoadd.txt
ls DATA/rerun/coaddMeasure2/deepCoadd-results/i3/0/ > patches_i_forcedPhotCoadd.txt
sed -i "s/^/--id filter=i3 tract=0 patch=/g" patches_i_forcedPhotCoadd.txt
sed -i 's|'/'||g' patches_i_forcedPhotCoadd.txt
ls DATA/rerun/coaddMeasure2/deepCoadd-results/u2/0/ > patches_u_forcedPhotCoadd.txt
sed -i "s/^/--id filter=u2 tract=0 patch=/g" patches_u_forcedPhotCoadd.txt
sed -i 's|'/'||g' patches_u_forcedPhotCoadd.txt

#forcedPhotCoadd.py DATA --rerun coaddMeasure2:coaddForcedPhot @patches_g_forcedPhotCoadd.txt -C config/forcedPhotCoaddConfig.py -j ${cpunum} --longlog
forcedPhotCoadd.py DATA --rerun coaddMeasure2:coaddForcedPhot @patches_r_forcedPhotCoadd.txt -C config/forcedPhotCoaddConfig.py -j ${cpunum} --longlog
forcedPhotCoadd.py DATA --rerun coaddMeasure2:coaddForcedPhot @patches_i_forcedPhotCoadd.txt -C config/forcedPhotCoaddConfig.py -j ${cpunum} --longlog
forcedPhotCoadd.py DATA --rerun coaddMeasure2:coaddForcedPhot @patches_u_forcedPhotCoadd.txt -C config/forcedPhotCoaddConfig.py -j ${cpunum} --longlog
