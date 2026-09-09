#!/bin/bash
# --- Start of slurm commands -----------

# Request an hour of runtime:
#SBATCH --time=3:00:00

# Default resources are 1 core with 2.8GB of memory per core.
# Use more cores:
#SBATCH -n 1

# Memory per node:
#SBATCH --mem=30G

# Specify a job name:
#SBATCH -J FRB190417_skymap

# Specify an output file
#SBATCH -o j_FRB190417_skymap-%j.out
#SBATCH -e j_FRB190417_skymap-%j.out

#----- End of slurm commands ----

module unload python
module unload intel
module load gcc/6.3

source <LSST_V19_ROOT>/loadLSST.bash
setup lsst_distrib


template_folder="<LEGACY_HELPERS>"

#----- Create a skymap -----
makeDiscreteSkyMap.py DATA @list_process_g.list @list_process_r.list @list_process_i.list @list_process_u.list --rerun processCcdOutputs_noct:coadd -C config/makeDiscreteSkyMapConfig.py > makeDiscreteSkyMap.out

# read ra/dec ranges from the previous output
corner=$(python ${template_folder}/get_skymap_corner.py makeDiscreteSkyMap.out)
echo "corner=${corner}"

#----- Identify the list of (tract,patch) -----
reportPatches.py DATA/rerun/coadd/ --config raDecRange="${corner}" --id tract=0 patch=0,0 filter=r2 > patches.txt


sed 's/^/--id filter=u2 /g;1,2d' patches.txt > patches_u.txt
sed 's/^/--id filter=g2 /g;1,2d' patches.txt > patches_g.txt
sed 's/^/--id filter=r2 /g;1,2d' patches.txt > patches_r.txt
sed 's/^/--id filter=i3 /g;1,2d' patches.txt > patches_i.txt
