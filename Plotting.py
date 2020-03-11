#!/bin/python3

#########################
######### ROUTINE TO PLOT THE SEASONAL MEAN OF ANY VARIABLE OVER AN ALREADY 
######### SELECTED REGION.
#########################


import cartopy
import cartopy.feature as cfeat
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import xarray as xr
import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
from mpl_toolkits.axes_grid1 import make_axes_locatable


#########################dict(data1.data_vars).keys()
######### OPENING FILES AND DIRECTORIES
#########################


directory = '/home/lgarcia/Documents/data_ARMOR/'
file_name = 'dataset-armor-3d-rep-weekly_20020703T1200Z_P20190301T0000Z.nc'
name = 'out.nc'

data1 = xr.open_dataset(directory+file_name)
data = xr.open_dataset(directory+name)


#########################
######### STARTING THE PLOT
#########################

##Stating the number of plots to do in this plot. Is better to make just one!!!
Nrows = 1
Ncols = 1


##Seting the coordinates
x = data.longitude
y = data.latitude
x_n, y_n = np.meshgrid(x, y)

var = data.mlotst[0]


#########################
### PARAMETERS OF COLORBAR:
###    (just uncomment)
#########################
### PRECIPITATION 
#ticks = ['<-8.3', '-6.7', '-5.1', '-3.5', '-1.9', '0.0', 
#         '1.9', '3.5', '5.1', '6.7', '>8.3']
#title_cbr = 'pp [mm day-1]'
cmap = 'YlGnBu'

orientation = 'vertical'


##Projection and region to plot
#proj = ccrs.PlateCarree(360)
#reg = [-180, -30, -10, 45]


fig, ax = plt.subplots(nrows=Nrows, ncols=Ncols, figsize=(15,5))
#subplot_kw=dict(projection=proj),


#ax.set_global()
#ax.coastlines('50m')
#ax.add_feature(cartopy.feature.BORDERS, linestyle=':')
#ax.set_extent(reg, crs=ccrs.PlateCarree())     #lat, lon

ax.contourf(x_n, y_n, var.data, cmap=cmap)
contr = ax.contourf(x_n, y_n, var.data, cmap=cmap)
#cb0 = fig.colorbar(contr, ax=ax, orientation=orientation)
#cb0.set_label(title_cbr)

#For pressure/wind include this line
#ax.quiver(x_n[::10, ::10]+360, y_n[::10,::10], u_norm[::10, ::10], v_norm[::10, ::10], pivot='tip', width=0.001)

#ax.set_title(title_fig)

plt.subplots_adjust(top=0.912, bottom=0.046, left=0.015, right=0.985, hspace=0.43, wspace=0.2)
#fig.savefig('/media/lgarcia2/CHIBIMOON/Tesis_ICTP/September_wind.pdf')
plt.show()








def Get_Variables(data_set):
    names = dict(data_set.data_vars).keys()
    
    for n in names:
        n = 
