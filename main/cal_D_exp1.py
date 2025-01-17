import os
import shutil
import subprocess
import numpy as np
import xarray as xr
import netCDF4 as nc
from tqdm import tqdm, trange
from joblib import Parallel, delayed
from myfunc import timer
from myfunc import DirMan
import config
import calendar


resolution = config.resolution
name = config.name
data_path = config.data_path


# Calculate Dr(the Culmulate Water Deficit - CWD) version2 and 
# the first month to use bedrock water
@timer
def Dr():
    ds = xr.open_dataset('diff.nc')
    data_var = ds['et'].load()
    ds2 = xr.open_dataset('SnowCover.nc')
    snowf = ds2['snowf'].load()
    ds3 = xr.open_dataset(f'{data_path}../0p1/Ssoil.nc')
    ssoil = ds3['Band1'].load()

    shape = data_var.isel(time=0).shape
    time_len = len(ds.time)

    deficit_acc = np.zeros((time_len, *shape))

    for j in range(18):
        print(f"year is {j+2003}")

        pmax = np.zeros(shape) 
        pmin = np.zeros(shape)  
        Drv1 = np.zeros(shape)
        data_acc = np.zeros(shape)
        first_day = np.full_like(data_var.isel(time=0+46*j).values, -1, dtype=int)
        p = np.zeros(shape)
        n = np.zeros(shape)
        for i in range(0+46*j,46+46*j):
            # print(i-46*j)
            current_data_mask = data_var.isel(time=i).values * snowf.isel(time=i).values

            if i < 46+46*j - 1:
                next_data_mask = data_var.isel(time=i + 1).values * snowf.isel(time=i + 1).values
            else:
                next_data_mask = current_data_mask

            p = np.where((current_data_mask>0)&(next_data_mask<0),p+1,p)
            n = np.where((current_data_mask<0)&(next_data_mask>0),n+1,n)

            data_acc += current_data_mask

            # set pmax(the closest maximum point)
            pmin_last = pmin
            pmax = np.where((current_data_mask>0)&(next_data_mask<0),data_acc,pmax)
            pmin = np.where((current_data_mask<0)&(next_data_mask>0),data_acc,pmin)

            diff_max = np.where(current_data_mask<0,pmax-pmin_last,data_acc-pmin_last)
            Drv1 = np.maximum(Drv1,diff_max)
            
            deficit_acc[i, :, :] = data_acc

            # When first use the bedrock water?
            first_occurrence = ((data_acc-pmin) > ssoil.values) & (first_day == -1)
            first_day[first_occurrence] = 8*(i-46*j)+1

        # Save the results to a new NetCDF file
        output_ds = xr.Dataset({'Dr': (('lat', 'lon'), Drv1)},
                            coords={'lat': ds['lat'], 'lon': ds['lon']})
        output_ds.to_netcdf(f'Dr_{2003+j}_temp1.nc')

        output_ds1 = xr.Dataset({'FD': (('lat', 'lon'), first_day)},
                    coords={'lat': ds['lat'], 'lon': ds['lon']})
        output_ds1.to_netcdf(f'FD_{2003+j}_temp1.nc')

        output_ds2 = xr.Dataset({'nmax': (('lat', 'lon'), p)},
                        coords={'lat': ds['lat'], 'lon': ds['lon']})
        output_ds2.to_netcdf(f'{data_path}nmax_{2003+j}.nc')

        output_ds3 = xr.Dataset({'nmin': (('lat', 'lon'), n)},
                            coords={'lat': ds['lat'], 'lon': ds['lon']})
        output_ds3.to_netcdf(f'{data_path}nmin_{2003+j}.nc')

    output_ds4 = xr.Dataset({'Deficit': (('time', 'lat', 'lon'), deficit_acc)},
                        coords={'time': ds['time'], 'lat': ds['lat'], 'lon': ds['lon']})
    output_ds4.to_netcdf('Deficit_D.nc')

    # Close datasets
    ds.close()
    ds2.close()   


# Set cdo function to use parallel operations 
def cdo_mul(filename1, filename2, filename3):
    subprocess.run(f"cdo mul {filename1} {filename2} {filename3}", shell=True, check=True)
    
def cdo_sub(filename1, filename2, filename3):
    subprocess.run(f"cdo sub {filename1} {filename2} {filename3}", shell=True, check=True)
    
def cdo_expr(filename1, filename2, nday):
    subprocess.run(f'cdo -expr,"Ee=Dr*1000*2257/(3600*24*{nday})" {filename1} {filename2}', shell=True, check=True)

# Mask Dr
@timer
def Dr_mask():
    # remap the 0p1 resolution to 0p1 resolution(no need, but for the sake of formatting consistency)
    for j in range(18):
        print(j+2003)
        subprocess.run(f"cdo -b F32 -P 12 --no_remap_weights remapbil,mask1.nc Dr_{2003+j}_temp1.nc Dr_{2003+j}_temp2.nc", shell=True, check=True)
    
    Parallel(n_jobs=5)(delayed(cdo_mul)(f"Dr_{2003+j}_temp2.nc", "mask123.nc", f"Dr_{2003+j}.nc") for j in tqdm(range(18)))


# Calculate Dbedrock(rock moisture) 
@timer
def Db():
    Parallel(n_jobs=5)(delayed(cdo_sub)(f"Dr_{2003+j}.nc", "Ssoil.nc", f"Dbedrock_{2003+j}_temp1.nc") for j in tqdm(range(18)))
    
    Parallel(n_jobs=5)(delayed(cdo_mul)(f"Dbedrock_{2003+j}_temp1.nc", "mask123.nc", f"Dbedrock_{2003+j}.nc") for j in tqdm(range(18)))

def LH_yr():
    yearday = [366 if calendar.isleap(year) else 365 for year in range(2003, 2021)]    
    Parallel(n_jobs=5)(delayed(cdo_expr)(f"Dbedrock_{2003+j}.nc", f"LH_{2003+j}_temp1.nc", f"{yearday[j]}") for j in tqdm(range(18)))
    Parallel(n_jobs=5)(delayed(cdo_mul)(f"LH_{2003+j}_temp1.nc", "mask123.nc", f"LH_{2003+j}.nc") for j in tqdm(range(18)))

def cal_LH_median():
    name_list = []
    for year in range(2003,2021):
        name = f'LH/LH_{year}.nc'
        name_list.append(name)

    datasets = [xr.open_dataset(file) for file in name_list]
    data_arrays = [ds['Ee'].values for ds in datasets]
    median_data = np.median(data_arrays, axis=0)

    output_file = f'LH/LH_median.nc'
    median_ds = xr.Dataset(
        {'Ee': (['lat', 'lon'], median_data)}, 
        coords={'lat': datasets[0].lat, 'lon': datasets[0].lon} 
    )
    median_ds.to_netcdf(output_file)

# Delete the intermediate data to save memory
@timer
def delete():
    os.system('rm -rf Dr_*_temp1.nc')
    os.system('rm -rf Dr_*_temp2.nc')
    os.system('rm -rf Dbedrock_*_temp1.nc')    
    

# calculate Dbedrock Frequency
def cal_DbF():
    s1 = 0
    # i =2
    for year in range(2003,2021):
        file = f'Dbedrock_{year}.nc'
        image = xr.open_dataset(file)
        # print(dtb)
        s = image['Dr']
        print(f'year: {year}, min: {s.min().values}, max: {s.max().values}')
        
        s = np.where(s > 0, 2, np.where(s < 0, 1, 0))
        print(f'year: {year}, min: {s.min()}, max: {s.max()}')
        
        print(s.min(),s.max())
        
        if year == 2003:
            s1 = s
        else:
            s1 = s*s1
        
        s_nonan = np.where((s1<0), 0, s1)
        print(s1.min(),s1.max(),np.mean(s_nonan))
        image.close()
    print('end do')

    s1 = np.where((s1 >=2) & (s1 < 262144), 2, s1)
    s1 = np.where((s1 == 1), 3, s1)
    s1 = np.where(s1==262144, 1, s1)

    file_mask = f'mask12.nc'
    mask = xr.open_dataset(file_mask)
    s2 = mask['Band1']
    print(s1.min(),s1.max())

    s1 = np.where((s1==0) & (s2 == 1), 4, s1)
    # s1 = np.where((s1==0), np.nan, s1)

    print(s1.min(),s1.max())
    shutil.copyfile('Dbedrock_2003.nc', 'Dbedrock_Frequency.nc')

    with nc.Dataset('Dbedrock_Frequency.nc', 'a') as file:
        s_var = file.variables['Dr']

        new_s_data = s1 

        s_var[:,:] = new_s_data

def cal_FD():
    for year in range(2003,2021):
        os.system(f'cdo setrtoc,-1,0,0 FD_{year}_temp1.nc FD_{year}_temp2.nc')

def cal_FM_mean():
    name_list = 'cdo -O -ensmean '
    for year in range(2003,2021):
        name = f'FD_{year}_temp2.nc '
        name_list = name_list+name
    name_list = name_list+'FD_mean_temp1.nc'
    os.system(name_list)
    os.system('cdo -b F32 -P 12 --no_remap_weights remapbil,mask1.nc FD_mean_temp1.nc FD_mean_temp2.nc')
    os.system('cdo mul FD_mean_temp2.nc mask123.nc FD_mean.nc')

    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    sumday = 0
    command_list = ''
    for i, day in enumerate(days_in_month):
        sumday += day  
        command_name = f"-setrtoc,{sumday-day},{sumday},{i+1} "
        command_list = command_name + command_list
    command = f'cdo {command_list}FD_mean.nc FM_mean_temp1.nc'
    print(f"Executing: {command}")  
    os.system(command)

    os.system('cdo mul FM_mean_temp1.nc mask123.nc FM_mean.nc')

def cal_FM_median():
    name_list = []
    for year in range(2003,2021):
        name = f'FD_{year}_temp2.nc'
        name_list.append(name)

    datasets = [xr.open_dataset(file) for file in name_list]
    data_arrays = [ds['FD'].values for ds in datasets]
    median_data = np.median(data_arrays, axis=0)

    output_file = 'FD_median_temp1.nc'
    median_ds = xr.Dataset(
        {'FD': (['lat', 'lon'], median_data)}, 
        coords={'lat': datasets[0].lat, 'lon': datasets[0].lon} 
    )
    median_ds.to_netcdf(output_file)
    os.system('cdo -b F32 -P 12 --no_remap_weights remapbil,mask1.nc FD_median_temp1.nc FD_median_temp2.nc')
    os.system('cdo mul FD_median_temp2.nc mask123.nc FD_median.nc')

    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    sumday = 0
    command_list = ''
    for i, day in enumerate(days_in_month):
        sumday += day  
        command_name = f"-setrtoc,{sumday-day},{sumday},{i+1} "
        command_list = command_name + command_list
    command = f'cdo {command_list}FD_median.nc FM_median_temp1.nc'
    print(f"Executing: {command}")  
    os.system(command)

    os.system('cdo mul FM_median_temp1.nc mask123.nc FM_median.nc')

# Execute all program
def cal_D():        
    # Transfer the current path to the calculation path
    dir_man = DirMan(data_path)
    dir_man.enter()
    path = os.getcwd()+'/'
    print("Current file path: ", path)

    # Dr()
    # Dr_mask()
    # Db()
    # LH_yr()
    cal_LH_median()
    # delete()
    # cal_DbF()
    # cal_FD()
    # cal_FM_mean()
    # cal_FM_median()
    
    # Transfer from the calculation path to the later path 
    dir_man.exit()
    path = os.getcwd()+'/'
    print("Current file path: ", path)


if __name__=='__main__':
    cal_D()