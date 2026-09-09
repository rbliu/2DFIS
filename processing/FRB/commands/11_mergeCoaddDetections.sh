#!/bin/bash 
# --- Start of slurm commands -----------

# Request an hour of runtime:
#SBATCH --time=16:00:00

# Default resources are 1 core with 2.8GB of memory.
# Use more memory (4GB):
#SBATCH -n 20
#SBATCH --mem=90G

# Specify a job name:
#SBATCH -J FRB190417_mergeCoaddDet

# Specify an output file
# %j is a special variable that is replaced by the JobID when 
# job starts
#SBATCH -o FRB190417_mergeCoaddDet-%j.out
#SBATCH -e FRB190417_mergeCoaddDet-%j.out

#----- End of slurm commands ----
cpunum="20"

module unload intel
module load gcc/6.3 
module unload python

source <LSST_V19_ROOT>/loadLSST.bash 
setup lsst_distrib

mergeCoaddDetections.py DATA --rerun coaddMeasure --id filter=u2^g2^r2^i3 -C config/mergeCoaddDetectionsConfig.py -j ${cpunum} --clobber-config --longlog

#deblendCoaddSources.py DATA --rerun coaddMeasure @patches_g.txt --clobber-config -j ${cpunum} --longlog
#deblendCoaddSources.py DATA --rerun coaddMeasure @patches_r.txt -j ${cpunum} --longlog
#deblendCoaddSources.py DATA --rerun coaddMeasure @patches_i.txt -j ${cpunum} --longlog
#deblendCoaddSources.py DATA --rerun coaddMeasure --id filter=z -j ${cpunum} --longlog
#deblendCoaddSources.py DATA --rerun coaddMeasure @patches_u.txt -j ${cpunum} --longlog
