from netCDF4 import Dataset
import netCDF4 as nc
import subprocess
import xarray as xr
import numpy as np
import os
from tqdm import tqdm


def main(input_path,name):
    # loop every hdf file in the directory
    
    outdata=np.ndarray((828,1800,3600))
    outdata=outdata*0+np.nan
    
    outdata_all=np.ndarray((366,1800,3600))
    outdata_all=outdata_all*0+np.nan
    
    interval_8d = np.full(46,8)
        
    for year in range(2003,2021):
        filename = f'{name}_predict_{year}_1D_0p1.nc'
        print("--------------------------------------------------------------------------------------------")
        print(year)

        with xr.open_dataset(input_path+filename) as ncname:
            ncdata = np.array(ncname['ET'][:,:-1,:])
            ncdata_invertlat = ncdata[:,::-1,:]
            
            if year%4==0:
                print(f"{year}年是闰年")
                outdata_all[:,:,:] = ncdata_invertlat[:,:,:]
                interval_8d[-1] = 6
            else:
                print(f"{year}年是平年")
                outdata_all[:-1,:,:] = ncdata_invertlat[:,:,:]
                interval_8d[-1] = 5

            for i in range(46):
                j = np.sum(interval_8d[:i])
                k = np.sum(interval_8d[:i+1])
                l = (year-2003)*46+i
                outdata[l,:,:] = np.nansum(outdata_all[j:k,:,:], axis=0)

        print("--------------------------------------------------------------------------------------------")
    
    return(outdata)

def wrtieout2netcdf(matrix,filename):        
    #write out to netcdf file
    #create netcdf file
    subprocess.getoutput("rm -f "+filename)
    ncfile = Dataset(''+filename, 'w', format='NETCDF4')
    #create dimensions
    # ncfile.createDimension('year', None)
    # ncfile.createDimension('month', None)
    ncfile.createDimension('time', None)
    ncfile.createDimension('lat', 1800)
    ncfile.createDimension('lon', 3600)
    #create variables
    # year = ncfile.createVariable('year', 'i4', ('year',))
    # month = ncfile.createVariable('month', 'i4', ('month',))
    time = ncfile.createVariable('time', 'i4', ('time',))
    lat = ncfile.createVariable('lat', 'f4', ('lat',))
    lon = ncfile.createVariable('lon', 'f4', ('lon',))
    data = ncfile.createVariable('et', 'f4', ('time','lat','lon',))
    
    time.standard_name = "time"
    time.units = "days since 2001-01-01T00:00:00"
    time.calendar = "proleptic_gregorian"
    time.axis = "T"
    
    lat.standard_name = "lat"
    lat.long_name = "latitude"
    lat.units = "degrees_north"
    lat.axis = "Y"
    
    lon.standard_name = "lon"
    lon.long_name = "longitude"
    lon.units = "degrees_east"
    lon.axis = "X"
    
    data.Fill_value = "-9999"
    data.Long_name = "Evapotranspiration"
    data.Unit = "mm.8day-1"

    yearday = [365,366,365,365,365,366,365,365,365,366,365,365,365,366,365,365,365,366]
    sumday = [0, 365, 731, 1096, 1461, 1826, 2192, 2557, 2922, 3287, 3653, 4018, 4383, 4748, 5114, 5479, 5844, 6209, 6575]
    
    for i in range(828):
        if (i+1)%46==1:
            j = yearday[(i+1)//46-1]-360
            # print(j)       
        else:
            j = 8
            
        if i ==0:
            time[i] = 730   
        else:
            time[i] = time[i-1]+j    

    data[:,:,:] = matrix
    lat[:] = np.arange(-89.95,90,0.1)
    lon[:] = np.arange(-179.95,180,0.1)
    ncfile.close()

input_path = '/media/zhwei/data02/DataML/step2/ET_input/1D_0p1/'
output_path = '/home/zhwei/Bedrock/data/ET/'
os.chdir(output_path)
print(output_path)

namelist = ['EB_ET','ERA5LAND','ERA5','ET_3T','FLUXCOM_9km','FLUXCOM','GLDAS_CLSM_2.2','GLDAS_Noah_2.1','GLEAM_hybrid','GLEAM_v3.6a','GLEAM_v3.6b','PMLV2','REA']
# namelist = ['EB_ET']
for name in namelist:
    print(f"{name}数据处理已经开始了")
    
    data = main(input_path,name)
    wrtieout2netcdf(data,f'ET_{name}_2003_2020_8D_0p1_mm8d.nc')
    
    print(f"{name}数据处理已经结束了")