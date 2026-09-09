#!/bin/bash

#SBATCH --time=8:30:00
#SBATCH -n 1
#SBATCH --mem=16G
#SBATCH -J CLrot_read_catalog_all
#SBATCH -o CLrot_read_catalog_all-%j.out 
#SBATCH -e CLrot_read_catalog_all-%j.out 


#===========================
module unload python
module unload intel

source <LSST_V19_ROOT>/loadLSST.bash
setup lsst_distrib


#===========================
# Variables

script_folder="<LEGACY_CFHT_SCRIPTS>/read_catalog_all"
DATA_folder="DATA"
output_folder="a03_read_catalog_all_output"


#-----------------------

patches=""

for ((x=1; x<=5; x++))
do
    for ((y=1; y<=5; y++))
    do
        patches="${patches}^${x},${y}"
    done
done

patches=${patches:1}
echo "******patches: ${patches}******"

tag="all_shapes"
patches_tag="CLrot_11-55"
dm_csv="${output_folder}/${patches_tag}_${tag}.csv"



#---------------------------
# Script

[ ! -d ${output_folder} ] && mkdir ${output_folder} 

echo "Loading DM output..."
python ${script_folder}/load_dm_output_all_other_shapes_test.py ${patches} ${dm_csv} ${DATA_folder} 



