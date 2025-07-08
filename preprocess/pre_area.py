from math import radians, sin
import numpy as np
import os
from joblib import Parallel, delayed
import math
import xarray as xr
from netCDF4 import Dataset

path1 = '/home/xuxh22/stu01/'

def count_area(lat1,lat2):
    lat1,lat2 = map(radians,[lat1,lat2])
    r = 6.37122e6
    # dlon = 0.00416666688397527
    dlon = 0.5
    dlon_rad = math.radians(dlon)
    area = abs(r**2 * dlon_rad * (sin(lat2)-sin(lat1)))
    # print(area)
    return area

def area():
    dir_path = path1
    os.chdir(dir_path)

    lat = np.arange(89.75,-90,-0.5)
    lon = np.arange(-179.75,180,0.5)
    # inc = 0.00416666688397527
    inc = 0.5
    lat1 = lat-inc/2
    lat2 = lat+inc/2    
    grid1,grid2 = np.meshgrid(lon, lat)
    area = np.zeros_like(grid1)
    result = Parallel(n_jobs=3)(delayed(count_area)(lat1[i], lat2[i]) for i in range(len(lat)))
    for i in range(len(lat)):
        area[i, :] = result[i]
        print(area[i,0])
    print(f'The total area of the earth: {np.sum(area):.3f} $m^2$')
            
    output_ds = xr.Dataset({'area': (('lat', 'lon'), area)},
                        coords={'lat': lat, 'lon': lon})
    output_ds.attrs['title'] = 'Area Data'
    output_ds.attrs['units'] = 'm2'
    output_ds.attrs['created_by'] = 'Xu Xionghui'
    output_ds.attrs['creation_date'] = '2024-11-04'
    output_ds.attrs['gridtype'] = 'lonlat'
    output_ds['area'].attrs['long_name'] = 'Area'
    output_ds['area'].attrs['units'] = 'm2'

    output_ds['lat'].attrs['ylongname'] = 'Latitude'
    output_ds['lat'].attrs['yunits'] = 'degrees_north'
    output_ds['lon'].attrs['xlongname'] = 'Longitude'
    output_ds['lon'].attrs['xunits'] = 'degrees_east'

    output_ds.to_netcdf('Area_0p5.nc')

    with Dataset('Area_0p5.nc', 'r+', format='NETCDF4') as nc:
        nc.setncattr('gridtype', 'lonlat')
    print(area)
    print(f'The total area of the earth: {np.sum(area)/1e12:.3f} million $km^2$')
    # output_ds.to_netcdf('Area.nc')
    print("Area completed")

area()