import netCDF4 as nc
import numpy as np

input_file = '/tera04/zhwei/xionghui/bedrock/DTB/DTB_Pelletier/upland_hillslope_soil_remap_cm.nc'  
output_file = '/home/xuxh22/stu01/Mode/data/bedrock_Pelletier.nc'  

with nc.Dataset(input_file, 'r') as src:
    lon = src.variables['lon'][:]
    lat = src.variables['lat'][::-1]
    band1 = src.variables['Band1'][::-1,:]

    fill_value = src.variables['Band1']._FillValue if '_FillValue' in src.variables['Band1'].ncattrs() else np.nan
    missing_value = src.variables['Band1'].missing_value if 'missing_value' in src.variables['Band1'].ncattrs() else np.nan

    # band1 = np.where(np.isnan(band1), 0, band1)  
    # band1 = np.where(band1 == fill_value, 0, band1)  
    # band1 = np.where(band1 == missing_value, 0, band1) 

with nc.Dataset(output_file, 'w', format='NETCDF4') as dst:
    dst.createDimension('longitude', len(lon))
    dst.createDimension('latitude', len(lat))

    landmask = dst.createVariable('dbedrock', 'i4', ('latitude', 'longitude'), zlib=True, chunksizes=(432, 864))

    landmask[:, :] = band1.astype(np.int32)

    # dst.description = "Processed landmask file with missing values set to 0"
    dst.history = "Created by Python script"
    dst.source = "Original file: " + input_file

print("The NetCDF file was successfully created: ", output_file)