#!/bin/bash 
# --- Start of slurm commands -----------

# Request an hour of runtime:
#SBATCH --time=23:00:00

# Default resources are 1 core with 2.8GB of memory.
# Use more memory (4GB):
#SBATCH -n 24
#SBATCH --mem=150G

# Specify a job name:
#SBATCH -J FRB190417_measCo

# Specify an output file
# %j is a special variable that is replaced by the JobID when 
# job starts
#SBATCH -o FRB190417_measCoadd-%j.out
#SBATCH -e FRB190417_measCoadd-%j.out

#----- End of slurm commands ----
cpunum="24"

module unload intel
module load gcc/6.3 
module unload python

source <LSST_V19_ROOT>/loadLSST.bash 
setup lsst_distrib

measureCoaddSources.py DATA --rerun coaddMeasure:coaddMeasure2 --id filter=g2 -C config/measureCoaddSourcesConfig.py -j ${cpunum} --longlog --clobber-config
measureCoaddSources.py DATA --rerun coaddMeasure:coaddMeasure2 --id filter=r2 -C config/measureCoaddSourcesConfig.py -j ${cpunum} --longlog --clobber-config
measureCoaddSources.py DATA --rerun coaddMeasure:coaddMeasure2 --id filter=i3 -C config/measureCoaddSourcesConfig.py -j ${cpunum} --longlog --clobber-config
measureCoaddSources.py DATA --rerun coaddMeasure:coaddMeasure2 --id filter=u2 -C config/measureCoaddSourcesConfig.py -j ${cpunum} --longlog --clobber-config
#measureCoaddSources.py DATA --rerun coaddMeasure:coaddMeasure2 --id filter=z -C config/measureCoaddSourcesConfig.py -j ${cpunum} --longlog --clobber-config
