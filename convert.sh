#!/bin/sh

############################################################################
### This script is used to re-agroup the ARMOR-3D datasets from one file for
### each week into one file for each full year. So we have, the dataset goes
### from ARMOR3D_REPv4_20050105_MLD_OptimalDeBoyer_cmemsformat to 
### ARMOR_year. It also changes the reference point for the longitude and 
### latitude. This script in special uses the new ARMOR-3D dataset.
############################################################################



### /data0/data/REFERENCE_DATA/OCEAN_REP/ARMOR3D/data/2009
###  ARMOR3D_REPv4_20050119_MLD_OptimalDeBoyer_cmemsformat.nc

dir_i=/home/lgarcia/Documents/Original
file=ARMOR3D_REPv4
dir_o=/home/lgarcia/Documents/New_ARMOR



for year in {2005..2018}; do
    cd $dir_i

## First loop into one file per year
    for f in ARMOR3D_REPv4_$year*.nc; do
        ncks -O -h --mk_rec_dmn time $f $dir_i/$f-2
        
    done

    cd ..

## Changing the reference latitude
ncrcat -h $dir_i/ARMOR3D_REPv4_$year*.nc $dir_o/tmp_$year.nc
#    
ncks -O --msa -d longitude,181.,360. -d longitude,0.,180.0 $dir_o/tmp_$year.nc $dir_o/NARMOR_$year.nc
ncap2 -O -s 'where(longitude > 180) longitude=longitude-360' $dir_o/NARMOR_$year.nc $dir_o/NARMOR_$year.nc

    echo $year
    
#    rm -r $dir_i/*-2.nc
#    rm -r $dir_o/tmp_*.nc

done

