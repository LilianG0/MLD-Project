#!/bin/sh
### /data0/data/REFERENCE_DATA/OCEAN_REP/ARMOR3D/data/2009


###  dataset-armor-3d-rep-weekly_20100310T1200Z_P20190301T0000Z.nc
###  ARMOR3D_REPv4_20050105_MLD_OptimalDeBoyer_cmemsformat


dir_i=/home/lgarcia/Documents/Original
file=ARMOR3D_REPv4
dir_o=/home/lgarcia/Documents/New_ARMOR



#for year in {1979..2018}; do
#    cdo sellonlatbox,-180,180,-90,90 $dir/$file       $dir/$file2
#    ncks -d latitude,10.,85. -d longitude,-90.,50. $dir/$file2 $dir/out.nc
#echo $month
#done

for year in {2005..2006}; do

#    for f in $dir_i/$ff*.nc; do
    echo $f
    ncks -O -h --mk_rec_dmn time $dir_i/ARMOR3D_REPv4_$year* $dir_o/f-$year.nc
#    done 

#    ncrcat -h $dir_o/tmp/$f-2.nc $dir_o/tmp/tmp_$year.nc

#    cdo sellonlatbox,-180,180,-90,90 $dir_o/tmp/tmp_$year.nc $dir_o/ARGON_$year.nc
#    ncks -d latitude,10.,85. -d longitude,-90.,50. $dir_o/ARGON_$year.nc $dir_o/ARGON_$year.nc

#    rm -f $dir_o/tmp
#    echo $year
done
