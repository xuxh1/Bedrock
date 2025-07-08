import netCDF4 as nc
import numpy as np

input_file = '/home/xuxh22/stu01/data/mask1/mask1_v3/mask1_0p1.nc'  
output_file = '/home/xuxh22/stu01/data/mask1/mask1_v3/mask1_0p1_set0_correct.nc'  

with nc.Dataset(input_file, 'r') as src:
    lon = src.variables['lon'][:]
    lat = src.variables['lat'][::-1]
    band1 = src.variables['Band1'][::-1,:]

    fill_value = src.variables['Band1']._FillValue if '_FillValue' in src.variables['Band1'].ncattrs() else np.nan
    missing_value = src.variables['Band1'].missing_value if 'missing_value' in src.variables['Band1'].ncattrs() else np.nan

    band1 = np.where(np.isnan(band1), 0, band1)  
    band1 = np.where(band1 == fill_value, 0, band1)  
    band1 = np.where(band1 == missing_value, 0, band1)  

with nc.Dataset(output_file, 'w', format='NETCDF4') as dst:
    dst.createDimension('lat', len(lat))
    dst.createDimension('lon', len(lon))

    lon_w = dst.createVariable('lon_w', 'd', ('lon',), zlib=True, chunksizes=(3600,))
    lon_e = dst.createVariable('lon_e', 'd', ('lon',), zlib=True, chunksizes=(3600,))
    lat_s = dst.createVariable('lat_s', 'd', ('lat',), zlib=True, chunksizes=(1800,))
    lat_n = dst.createVariable('lat_n', 'd', ('lat',), zlib=True, chunksizes=(1800,))
    landmask = dst.createVariable('landmask', 'b', ('lat', 'lon'), zlib=True, chunksizes=(1800, 3600))


    landmask[:, :] = band1.astype(np.byte)

    lon_w[:] = lon-0.05
    lon_e[:] = lon+0.05
    lat_s[:] = lat-0.05
    lat_n[:] = lat+0.05

    dst.description = "Processed landmask file with missing values set to 0"
    dst.history = "Created by Python script"
    dst.source = "Original file: " + input_file

print("The NetCDF file was successfully created: ", output_file)