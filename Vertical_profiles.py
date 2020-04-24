import xarray as xr
import numpy as np
import datetime
import pandas as pd
import gsw
from scipy import interpolate

import matplotlib as mpl
import matplotlib.pyplot as plt

################################################################################
########    DICTIONARIES
################################################################################

reg_ext = {
    'lab': {
        'lon' : (-60, -30),
        'lat' : (50, 65),
        'name' : 'Labrador and Irminger Seas'
    },
    'gul': {
        'lon' : (-75, -45),
        'lat' : (30, 45),
        'name' : 'Gulf Stream'
    },
    'noe': {
        'lon' : (-30, -5),
        'lat' : (45, 60),
        'name' : 'North East Sea'
    }
}

## Selected points in the regions
### Gulf S: (60W, 35N)
### Lab -I: (50W, 55N)
### Nor E: (17.5W, 52.5N)
points = {
    'gul': {
        'lon': -60., 
        'lat': 35.
    },
    'lab': {
        'lon': -50., 
        'lat': 55.
    },
    'noe': {
        'lon': -17.5, 
        'lat': 52.5}
}




gulf = {
    'A': {
        't': (18., 19.), 
        's': (36.55, 36.65),
        'd': (26.3, 26.5)
    },
    'B': {
        't': (17.5, 25.), 
        's': (36.25, 36.75),
        'd': (24., 27.)
    },
    'C': {
        't': (17.5, 26.), 
        's': (36.4, 36.8),
        'd': (24., 26.5)
    },
    'D': {
        't': (18., 22.2), 
        's': (36.4, 36.7),
        'd': (25., 26.5)
    }
}


labrador = {
    'A': {
        't': (2.75, 3.5), 
        's': (34.65, 34.85),
        'd': (27.6, 27.75)
    },
    'B': {
        't': (3., 8.), 
        's': (34.5, 35.),
        'd': (26., 29.)
    },
    'C': {
        't': (3., 11.), 
        's': (34.5, 35.),
        'd': (26., 28.)
    },
    'D': {
        't': (4., 5.5), 
        's': (34.25, 35.),
        'd': (27.2, 27.7)
    }
}


north = {
    'A': {
        't': (10.7, 11.7), 
        's': (35.35, 35.5),
        'd': (26.9, 27.3)
    },
    'B': {
        't': (10., 15.), 
        's': (35.3, 35.7),
        'd': (26.2, 27.2)
    },
    'C': {
        't': (11., 16.), 
        's': (35.3, 35.7),
        'd': (26., 28.)
    },
    'D': {
        't': (11., 13.), 
        's': (35.45, 35.65),
        'd': (26.8, 27.2)
    }
}

################################################################################
########    FUNCTIONS
################################################################################

## Function to make the (x,y)-> (lon,lat) grid
def Grid(data_set):
    """
        Grid is a function that creates a rectangular grid using as x a longitude
        array and for y a latitude array.
        
        Parameters:
        ------------
            
        data_set : DataArray
            Is the dataset from which we will plot the histogram.
        
        Output:
        -------
        (x, y) : n-arrays
            Arrays that correspond for each (lon,lat) point
    """
    x = data_set.longitude
    y = data_set.latitude
    
    x, y = np.meshgrid(x, y)
    return(x, y)



## Function to crop the dataset
def Crops(coord, d_set):
    """
        Crops is a function that takes a data set and crops it into smaller
        region, using as parameters the values given by the dictionary 
        reg_ext.
        
        Parameters:
        ------------
            
        coord : string
            Key value that identifies the region to obtain
        
        d_set : DataArray
            Dataset to be cropped
        
        Output:
        -------
        new_ds : DataArray
            New data array corresponding to the region stated by 'coord'
    """
    
    lon1, lon2 = reg_ext[coord]['lon']
    lat1, lat2 = reg_ext[coord]['lat']
    name_fig = reg_ext[coord]['name']
    
    new_ds = d_set.sel(longitude=slice(lon1, lon2), latitude=slice(lat1, lat2))
    return(new_ds)


def Limits(dictionary, t):
    a = dictionary[t]['t']
    b = dictionary[t]['s']
    c = dictionary[t]['d']
    
    return(a, b, c)

################ PLOTS
## dep, tem, sal, ds_g

def Plot_density(dep, tem, sal, den, name=None):
    # Temperature
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(6, 9))
    color = 'orange'
    ax[0].set_xlabel('Temperature ($^o$C)', color=color)
    ax[0].set_ylabel('Depth (m)')
    ax[0].plot(tem, dep, color=color)
    ax[0].tick_params(axis='x', labelcolor=color)
    ax[0].set_ylim(-4500., 0.)

    # Salinity
    ax2 = ax[0].twiny()
    color = 'blue'
    ax2.set_xlabel('Salinity (PSU)', color=color)
    ax2.plot(sal, dep, color=color)
    ax2.tick_params(axis='x', labelcolor=color)
#    ax2.set_xlim(34.5, 37.)

    # Density
    ax3 = ax[0].twiny()
    color = 'green'
    ax3.set_xlabel('Density (kg m$^{-3}$)', color=color)
    ax3.plot(den, dep, color=color)
    ax3.spines["top"].set_position(("axes", 1.15))
    ax3.tick_params(axis='x', labelcolor=color)
#    ax3.set_xlim(25., 28.)

#############
    ###Second plot, zoomed
    lims_t, lims_s, lims_d = Limits(place, t)
    # Temperature
    color = 'orange'
    ax[1].set_xlabel('Temperature ($^o$C)', color=color)
    #ax[1].set_ylabel('Depth (m)')
    ax[1].plot(tem, dep, color=color)
    ax[1].tick_params(axis='x', labelcolor=color)
    ax[1].set_xlim(lims_t)

    # Salinity
    ax2 = ax[1].twiny()
    color = 'blue'
    ax2.set_xlabel('Salinity (PSU)', color=color)  
    ax2.plot(sal, dep, color=color)
    ax2.tick_params(axis='x', labelcolor=color)
    ax2.set_xlim(lims_s)

    # Density
    ax3 = ax[1].twiny()
    color = 'green'
    ax3.set_xlabel('Density (kg m$^{-3}$)', color=color)
    ax3.plot(den, dep, color=color)
    ax3.spines["top"].set_position(("axes", 1.15))
    ax3.tick_params(axis='x', labelcolor=color)
    ax3.set_xlim(lims_d)

    plt.ylim(-300., 0)
    fig.tight_layout()  # otherwise the right y-label is slightly clipped

    if not name:
        plt.show()
    else:
        plt.savefig(name)



def Plot_lines(dpt, tem, sal, den, MLD_a, MLD_f, MLD_v, reg, t):
    lims_t, lims_s, lims_d = Limits(reg, t)
    
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(3, 9))
    
    color = 'orange'
    ax.set_xlabel('Temperature ($^o$C)', color=color)
    ax.set_ylabel('Depth (m)')
    ax.plot(tem, dpt, color=color)
    ax.tick_params(axis='x', labelcolor=color)
    ax.set_xlim(lims_t)
    
    plt.hlines(-MLD_a, xmin, xmax, colors='k', 
                linestyles='solid', linewidths=1)

    plt.hlines(MLD_f, xmin, xmax, colors='m', 
                linestyles='solid', linewidths=3)

    plt.hlines(MLD_v, xmin, xmax, colors='c', l
                inestyles='solid', linewidths=1)

    ax2 = ax.twiny()  # instantiate a second axes that shares the same x-axis
    color = 'blue'
    ax2.set_xlabel('Salinity (PSU)', color=color)
    ax2.plot(sal, dpt, color=color)
    ax2.tick_params(axis='x', labelcolor=color)
    ax2.set_xlim(35.4, 35.7)

    ax3 = ax.twiny()
    color = 'green'
    ax3.set_xlabel('Density (kg m$^{-3}$)', color=color)
    ax3.plot(den, dpt, color=color)
    ax3.spines["top"].set_position(("axes", 1.15))
    ax3.tick_params(axis='x', labelcolor=color)
    ax3.set_xlim(26.85, 27.15)

    plt.ylim(-300., 0)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped

    if not name_fig:
        plt.show()
    else:
        plt.savefig(name_fig)



def Convert(data_set, t):
    dep = - data_set.depth
    sal = data_set.so[t].values
    tem = data_set.to[t].values
    lon = float(data_set.longitude.values)
    lat = float(data_set.latitude.values)
    
    # Pressure -> depth latitudde
    pr = gsw.p_from_z(dep, lat)
    sa = gsw.conversions.SA_from_SP(sal, pr, lon, lat)
    ct = gsw.conversions.CT_from_t(sa, tem, pr)
    ds = gsw.density.sigma0(sa, ct)
    pt = gsw.pt0_from_t(sa, tem, pr)

    return(dep, sa, ct, ds, pt)



def New_density(pot_10, sal_10):

    dpt = pot_10 - 0.2
    tem_02 = gsw.conversions.CT_from_pt(sal_10, dpt)

    ds_02 = gsw.density.sigma0(sal_10, tem_02)

    return (ds_02)


def Point(data_set, coord):
    point = data_set.sel(longitude=points[coord]['lon'], 
           latitude=points[coord]['lat'], method='nearest')
    return(point)


#Function to calculate MLD, according to a threshold value
def MLD_den(depth, density, delta):

    for i in range(2, len(density)):
        diff = density[i] - density[1]
#        print(diff)

        if (diff >= delta):
            return(float(depth[i]))
            break


###############################################################################
###########         MAIN PROGRAM
###############################################################################

dir_1 = '/home/liliang/Documents/data_ARMOR/'
fl_n1 = 'ARMOR_2005.nc'

c_armor = xr.open_dataset(dir_1 + fl_n1)

## Selected points in the regions
### Gulf S: (60W, 35N)
### Lab -I: (50W, 55N)
### Nor E: (17.5W, 52.5N)

gl = Crops('gul', c_armor)
lb = Crops('lab', c_armor)
nr = Crops('noe', c_armor)


p_gl = Point(nr, 'noe')

# Time step we work on:: 12, 25, 38, 51
t = 51
print('Holi!')
print(t)


# Convert(data_set, t) -> (dep, sal, tem, den, temp_pot)
dep_gl, sal_gl, tem_gl, den_gl, tpot_gl = Convert(p_gl, t)

# Calculating the density at dT = 0.2 degrees
# pot temp_10, sal at 10m -> Ne density at dT = 0.2
dn10_gl = den_gl[1]
pot10_gl = tpot_gl[1]
sal10_gl = sal_gl[1]

dn02_gl = New_density(pot10_gl, sal10_gl)

deltaD_gl = dn02_gl - dn10_gl
deltaD_fx = 0.03

#### Calculating density

MLD_a = p_gl.mlotst[t].values
MLD_f = MLD_den(dep_gl, den_gl, deltaD_fx)
MLD_v = MLD_den(dep_gl, den_gl, deltaD_gl)

print(MLD_a)
print(MLD_v)
print(MLD_f)

# Calculating depth from density
dep_dens = interpolate.interp1d(den_gl, dep_gl)

z = dep_dens(dn02_gl)

print(z)

## Making plot
name_fig = 'VP-Gulf.png'

#Plot_density(dep_gl, p_gl.to[t], p_gl.so[t], den_gl)

#Plot_lines(dep_gl, p_gl.to[t], p_gl.so[t], 
#            den_gl, MLD_a, MLD_f, z)








