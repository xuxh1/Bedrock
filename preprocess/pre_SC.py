from pyhdf.SD import SD, SDC
import matplotlib.pyplot as plt
import glob
import numpy as np
import netCDF4 as nc
import xarray as xr
import subprocess
from tqdm import tqdm
from netCDF4 import Dataset
import os
import glob

def ln():
    path1 = '/stu01/zhanghan/snowf/data/MYD_C1/'
    path2 = '/tera04/zhwei/xionghui/bedrock/SC/data_1d/'

    for year in range(2003,2021):
        list = glob.glob(f'{path1}MYD10C1.A{year}*.hdf')
        for name in list:
            print(name[-38:])
            # os.system(f'cp {name} {path2}{name[-38:]}')
            os.system(f'ln -sf {name} {path2}{name[-38:]}')
        
def readin(onehdf):
    readfile=onehdf
    #read in MODIS HDF file
    hdf = SD(readfile, SDC.READ)
    #read in reflectance data
    data   = np.array(hdf.select('Day_CMG_Snow_Cover'))
    qcflag = np.array(hdf.select('Snow_Spatial_QA'))
    usedata=np.where(qcflag==0,data,np.nan)
    usedata=np.where(usedata>100,np.nan,usedata)
    usedata=np.where(usedata<0,np.nan,usedata)
    print(usedata)
    return(usedata)

def main(DIRUSE):
    #loop every hdf file in the directory
    filelist=subprocess.getoutput("ls "+DIRUSE+"/data_1d/").split("\n")
    large_snowf_d8=np.ndarray((828,3600,7200))
    large_snowf_d8=large_snowf_d8*0+np.nan
    large_snowf_all=np.ndarray((8,3600,7200))
    large_snowf_all=large_snowf_all*0+np.nan
    # yearday = [365,366,365,365,365,366,365,365,365,366,365,365,365,366,365,365,365,366]
    sumday = [365, 731, 1096, 1461, 1826, 2192, 2557, 2922, 3287, 3653, 4018, 4383, 4748, 5114, 5479, 5844, 6209, 6575]
    day_8d=0
    for i,filename in tqdm(enumerate(filelist)):
        # year
        year=int(filename.split(".A")[1][0:4])
        # day from 2003
        day = i+1
        # day in this year
        day_yr = int(int(filename.split(".A")[1][4:7]))
        # 8day in this year
        d8_yr = int((day_yr-1)//8+1)
        # 8day from 2003
        d8 = (year-2003)*46 + d8_yr       
        # day in this 8day
        if (day_yr%8==1) or (day_yr==1):
            day_8d = 0
        day_8d = day_8d+1
        
        print(year,day,day_yr,day_8d,d8,d8_yr)
        
        large_snowf_all[day_8d-1,:,:]=readin(DIRUSE+"/data_1d/"+filename)
        if (day_8d%8==0) or (day in sumday):
            large_snowf_d8[d8-1,:,:]=np.nanmean(large_snowf_all[:day_8d,:,:], axis=0)

    large_snowf=large_snowf_d8[:,::-1,:]
    return(large_snowf)

def wrtieout2netcdf(matrix,filename):        
    #write out to netcdf file
    #create netcdf file
    subprocess.getoutput("rm -f "+filename)
    ncfile = Dataset(''+filename, 'w', format='NETCDF4')
    #create dimensions
    # ncfile.createDimension('year', None)
    # ncfile.createDimension('month', None)
    ncfile.createDimension('time', None)
    ncfile.createDimension('lat', 3600)
    ncfile.createDimension('lon', 7200)
    #create variables
    # year = ncfile.createVariable('year', 'i4', ('year',))
    # month = ncfile.createVariable('month', 'i4', ('month',))
    time = ncfile.createVariable('time', 'i4', ('time',))
    lat = ncfile.createVariable('lat', 'f4', ('lat',))
    lon = ncfile.createVariable('lon', 'f4', ('lon',))
    snowf = ncfile.createVariable('snowf', 'f4', ('time','lat','lon',))
    
    time.standard_name = "time"
    time.units = "days since 2001-01-01T00:00:00"
    time.calendar = "proleptic_gregorian"
    time.axis = "T"
    
    lat.standard_name = "latitude"
    lat.long_name = "latitude"
    lat.units = "degrees_north"
    lat.axis = "Y"
    
    lon.standard_name = "longitude"
    lon.long_name = "longitude"
    lon.units = "degrees_east"
    lon.axis = "X"
    
    snowf.Fill_value = "-9999"
    snowf.Long_name = "Snow_Cover_Fraction(%)"
    snowf.Unit = "%"

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
    lat[:] = np.arange(-89.975,90,0.05)
    lon[:] = np.arange(-179.975,180,0.05)
    snowf[:,:,:] = matrix
    #close file
    ncfile.close()

path = '/tera04/zhwei/xionghui/bedrock/SC/'
os.chdir(path)
print(path)

ln()
large_snowf=main(path)
wrtieout2netcdf(large_snowf,'SnowCover_0p05.nc')