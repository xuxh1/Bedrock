from netCDF4 import Dataset
import netCDF4 as nc
import subprocess
import xarray as xr
import numpy as np
import os
from joblib import Parallel, delayed

path1 = '/tera06/zhwei/CoLM_Forcing/'
path2 = '/tera11/zhwei/students/Xionghui/data/PR/'
months = [str(i).zfill(2) for i in range(1, 13)]
yearday = [365,366,365,365,365,366,365,365,365,366,365,365,365,366,365,365,365,366]
sumday = [0, 365, 731, 1096, 1461, 1826, 2192, 2557, 2922, 3287, 3653, 4018, 4383, 4748, 5114, 5479, 5844, 6209, 6575]


# ---------------------------------------------------------------------------------- cdo -------------------------------------------------------------------------------------------------
# remapbil,r?x? make the data's lon from 0 to 360
def cdo_cal_ERA5(filename1, filename2):
    subprocess.run(f"cdo -remapbil,r3600x1800 -invertlat -mulc,3600 -daysum {filename1} {filename2}", shell=True, check=True)
    
def cdo_cal_ERA5LAND(filename1, filename2):
    subprocess.run(f"cdo -invertlat -mulc,1000 -daysum {filename1} {filename2}", shell=True, check=True)
   
def cdo_cal_GDAS_GPCP(filename1, filename2):
    subprocess.run(f"cdo -remapbil,r3600x1800 -mulc,10800 -daysum {filename1} {filename2}", shell=True, check=True)
    
def cdo_cal_MSWX_V100(filename1, filename2):
    subprocess.run(f"cdo -invertlat -daysum {filename1} {filename2}", shell=True, check=True)
    
def cdo_mergetime(filename1, filename2):  
    subprocess.run(f"cdo mergetime {filename1} {filename2}", shell=True, check=True)
# ---------------------------------------------------------------------------------- cdo -------------------------------------------------------------------------------------------------
    
    
# ---------------------------------------------------------------------------------- write 2 nc -------------------------------------------------------------------------------------------------
def wrtieout2netcdf_ERA5(matrix,filename):        
    #write out to netcdf file
    #create netcdf file
    subprocess.getoutput("rm -f "+filename)
    ncfile = Dataset(''+filename, 'w', format='NETCDF4')
    #create dimensions
    ncfile.createDimension('time', None)
    ncfile.createDimension('lat', 1800)
    ncfile.createDimension('lon', 3600)
    #create variables
    time = ncfile.createVariable('time', 'i4', ('time',))
    lat = ncfile.createVariable('lat', 'f4', ('lat',))
    lon = ncfile.createVariable('lon', 'f4', ('lon',))
    data = ncfile.createVariable('tp', 'f4', ('time','lat','lon',))
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
    data.Long_name = "Total Precipitation"
    data.Unit = "mm.8day-1"
    for i in range(828):
        if (i+1)%46==1:
            j = yearday[(i+1)//46-1]-360     
        else:
            j = 8
        if i ==0:
            time[i] = 730   
        else:
            time[i] = time[i-1]+j    
        print(time[i])
    lat[:] = np.arange(-89.95,90,0.1)
    lon[:] = np.arange(-179.95,180,0.1)
    data[:,:,:1800] = matrix[:,:,1800:]
    data[:,:,1800:] = matrix[:,:,:1800]
    ncfile.close()
    
def wrtieout2netcdf(matrix,filename):        
    #write out to netcdf file
    #create netcdf file
    subprocess.getoutput("rm -f "+filename)
    ncfile = Dataset(''+filename, 'w', format='NETCDF4')
    #create dimensions
    ncfile.createDimension('time', None)
    ncfile.createDimension('lat', 1800)
    ncfile.createDimension('lon', 3600)
    #create variables
    time = ncfile.createVariable('time', 'i4', ('time',))
    lat = ncfile.createVariable('lat', 'f4', ('lat',))
    lon = ncfile.createVariable('lon', 'f4', ('lon',))
    data = ncfile.createVariable('tp', 'f4', ('time','lat','lon',))
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
    data.Long_name = "Total Precipitation"
    data.Unit = "mm.8day-1"
    for i in range(828):
        if (i+1)%46==1:
            j = yearday[(i+1)//46-1]-360     
        else:
            j = 8
        if i ==0:
            time[i] = 730   
        else:
            time[i] = time[i-1]+j    
        print(time[i])
    lat[:] = np.arange(-89.95,90,0.1)
    lon[:] = np.arange(-179.95,180,0.1)
    data[:,:,:] = matrix
    ncfile.close()
# ---------------------------------------------------------------------------------- write 2 nc -------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------- main -------------------------------------------------------------------------------------------------
def main(input_path,name,var):  
    outdata=np.ndarray((828,1800,3600))
    outdata=outdata*0+np.nan
    outdata_all=np.ndarray((366,1800,3600))
    outdata_all=outdata_all*0+np.nan
    interval_8d = np.full(46,8)
    for year in range(2003,2021):
        filename = f'{name}_{year}_total_precipitation_mmd.nc4'
        print("--------------------------------------------------------------------------------------------")
        print(year)
        with xr.open_dataset(input_path+filename) as ncname:
            ncdata = np.array(ncname[var][:,:,:])
            ncdata_invertlat = ncdata[:,:,:]
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
# ---------------------------------------------------------------------------------- main -------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------- data preprocess -------------------------------------------------------------------------------------------------
# ERA5:   2003-2020,721(90~-90)x1440(0~360),hourly,mtpr(kg m**-2 s**-1)
def ERA5():
    input_path = f'{path1}/ERA5/mean_total_precipitation_rate/'
    output_path = f'{path2}/ERA5/'
    os.makedirs(output_path, exist_ok=True)
    os.chdir(output_path)
    name = 'ERA5'
    var = 'mtpr'
    # filelistname = []
    # for year in range(2003,2021):
    #     Parallel(n_jobs=5)(delayed(cdo_cal_ERA5)(f"{input_path}ERA5_{year}_{mon}_mean_total_precipitation_rate.nc4", f"{name}_{year}_{mon}_total_precipitation_mmd.nc4") for mon in months)
    #     filelistname.append(' '.join(f'{name}_{year}_{mon}_total_precipitation_mmd.nc4' for mon in months))
    #     print(filelistname[year-2003])
    #     subprocess.getoutput(f"rm -f {name}_{year}_total_precipitation_mmd.nc4")
    # Parallel(n_jobs=5)(delayed(cdo_mergetime)(filelistname[year-2003], f"{name}_{year}_total_precipitation_mmd.nc4") for year in range(2003,2021))
    data = main(output_path,name,var)   
    wrtieout2netcdf_ERA5(data,f'PR_{name}_2003_2020_8D_0p1_mm8d.nc')
    print(f"{name}数据处理已经结束了")
    
# ERA5LAND:  2003-2020,1801(90~-90)x3600(0~360),hourly,tp(m/hr)
def ERA5LAND():
    input_path = f'{path1}/ERA5LAND/Precipitation_m_hr/'
    output_path = f'{path2}/ERA5LAND/'
    os.makedirs(output_path, exist_ok=True)
    os.chdir(output_path)
    name = 'ERA5LAND'
    var = 'tp'
    # for year in range(2003,2021):
    #     filelistname = ' '.join(f'ERA5LAND_{year}_{mon}_total_precipitation_mmd.nc' for mon in months)
    #     print(filelistname)
    #     Parallel(n_jobs=5)(delayed(cdo_cal_ERA5LAND)(f"{input_path}ERA5LAND_{year}_{mon}_total_precipitation_m_hr.nc", f"ERA5LAND_{year}_{mon}_total_precipitation_mmd.nc") for mon in months)
    # Parallel(n_jobs=5)(delayed(cdo_mergetime)(filelistname, f"{name}_{year}_total_precipitation_mmd.nc") for year in range(2003,2021))
    data = main(output_path,name,var)   
    wrtieout2netcdf_ERA5(data,f'PR_{name}_2003_2020_8D_0p1_mm8d.nc')
    print(f"{name}数据处理已经结束了")

# GDAS_GPCP:  2003-2020,600(-60~90)x1440,3hours,Rainf_f_tavg(kg m-2 s-1)
def GDAS_GPCP():
    input_path = f'{path1}/GDAS_GPCP/'
    output_path = f'{path2}/GDAS_GPCP/'
    os.makedirs(output_path, exist_ok=True)
    os.chdir(output_path)
    name = 'GDAS_GPCP'
    var = 'Rainf_f_tavg'
    # filelistname = []
    # for year in range(2003,2021):
    #     Parallel(n_jobs=5)(delayed(cdo_cal_GDAS_GPCP)(f"{input_path}GLDAS_GDAS_3H_tot_prcip.{year}{mon}.nc4", f"{name}_{year}_{mon}_total_precipitation_mmd.nc4") for mon in months)
    #     filelistname.append(' '.join(f'{name}_{year}_{mon}_total_precipitation_mmd.nc4' for mon in months))
    #     print(filelistname[year-2003])
    #     subprocess.getoutput(f"rm -f {name}_{year}_total_precipitation_mmd.nc4")
    # Parallel(n_jobs=5)(delayed(cdo_mergetime)(filelistname[year-2003], f"{name}_{year}_total_precipitation_mmd.nc4") for year in range(2003,2021))
    data = main(output_path,name,var)   
    wrtieout2netcdf_ERA5(data,f'PR_{name}_2003_2020_8D_0p1_mm8d.nc')
    print(f"{name}数据处理已经结束了")
    
# MSWX_V100:  2003-2020,1800(90~-90)x3600,precipitation(mm/3h)
def MSWX_V100():
    input_path = f'{path1}/MSWX_V100/'
    output_path = f'{path2}/MSWX_V100/'
    os.makedirs(output_path, exist_ok=True)
    os.chdir(output_path)
    name = 'MSWX_V100'
    var = 'precipitation'
    for year in range(2003,2021):
        filelistname = ' '.join(f'{name}_{year}_{mon}_total_precipitation_mmd.nc' for mon in months)
        print(filelistname)
        Parallel(n_jobs=5)(delayed(cdo_cal_MSWX_V100)(f"{input_path}P_{year}_{mon}.nc", f"{name}_{year}_{mon}_total_precipitation_mmd.nc") for mon in months)
    Parallel(n_jobs=5)(delayed(cdo_mergetime)(filelistname, f"{name}_{year}_total_precipitation_mmd.nc") for year in range(2003,2021))
    data = main(output_path,name,var)   
    wrtieout2netcdf(data,f'PR_{name}_2003_2020_8D_0p1_mm8d.nc')
    print(f"{name}数据处理已经结束了")
# ---------------------------------------------------------------------------------- data preprocess -------------------------------------------------------------------------------------------------

    





# CLDAS:      2008-2020 1600x1040
# CMFD:       -2018
# crujra:     360x720, too coarse
# cruncep_v4: -2011
# cruncep_v7: -2016
# GSWP3:     -2014
# JRA55:     320x640
# MPI-ESM1-2-HR: ssp585
# PLUMBER2:    site
# PLUMBER2-20231122:site
# PLUMBER2-bk: site
# PLUMBER2-old:site
# princeton-r:-2006
# qian:       -2004
# TPMFD:      region(lon:61.05 to 105.6455, lat:41.34843 to 25.74999)
# WFDE5:     360x720,-2019
# WFDEI:     -2016

# ERA5()
# ERA5LAND()
GDAS_GPCP()
# MSWX_V100()