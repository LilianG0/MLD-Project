import xarray as xr
import pandas as pd
import gsw

dir ='/home/liliang/Documents/MLD-project/'

f1 = 'G-DTS.csv'
f2 = 'L-DTS.csv'
f3 = 'N-DTS.csv'


##Format of the files: depth, AS, CT, density, Potential T

g =  pd.read_csv(dir+f1, header=None)
l =  pd.read_csv(dir+f2, header=None)
n =  pd.read_csv(dir+f3, header=None)


p_g = gsw.p_from_z(g[0], 32.375)
sa_g = gsw.conversions.SA_from_SP(g[1], p_g, -72.575, 32.375)
ct_g = gsw.conversions.CT_from_t(sa_g, g[2], p_g)
ds_g = gsw.density.sigma0(sa_g, ct_g)
pt_g = gsw.pt0_from_t(sa_g, g[2], p_g)



def New_density(temp_10, sal_10, p_0):
    dpt = temp_10 - 0.43
    tem_02 = gsw.conversions.CT_from_pt(sal_10, dpt)
    
    ds_02 = gsw.density.sigma0(sal_10, tem_02)
    return ds_02

# Density
g[3] = ds_g

# Potential temperature
g[4] = pt_g

g.to_csv(dir+f1, index = False, header=False)


temg = g[4]     # potential temperature
salg = sa_g[1]  # density from origunal data
pg = p_g[1]     # pressure, calculated here

print('hola!')
print(salg)

ds_10g = ds_g[1]
ds02_g = New_density(float(temg[1]), salg, pg)


delta_g = ds02_g - ds_10g


print(ds_10g, ds_10l, ds_10n)
print(ds02_g, ds02_l, ds02_n)
print(delta_g, delta_l, delta_n)
#delta_l =
#delta_n = 


