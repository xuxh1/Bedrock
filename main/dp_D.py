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
data_path = config.data_path

dir_man = DirMan(data_path)
dir_man.enter()

os.makedirs(f'{data_path}/D', exist_ok=True)

# Set cdo function to use parallel operations 
def cdo_mul(filename1, filename2, filename3):
    subprocess.run(f"cdo mul {filename1} {filename2} {filename3}", shell=True, check=True)
    
def cdo_sub(filename1, filename2, filename3):
    subprocess.run(f"cdo sub {filename1} {filename2} {filename3}", shell=True, check=True)
    
def cdo_expr(filename1, filename2, nday):
    subprocess.run(f'cdo -expr,"Ee=Dr*1000*2257/(3600*24*{nday})" {filename1} {filename2}', shell=True, check=True)

def cdo_setvals(filename1, filename2):
    subprocess.run(f'cdo setvals,0,nan {filename1} {filename2}', shell=True, check=True)

def dp_Dr():
    # remap the 0p1 resolution to 0p1 resolution(no need, but for the sake of formatting consistency)
    for j in range(18):
        print(f"year is {j+2003}")
        subprocess.run(f"cdo -b F32 -P 48 --no_remap_weights remapbil,mask1.nc4 D/Dr_{2003+j}_tmp1.nc4 D/Dr_{2003+j}_tmp2.nc4", shell=True, check=True)
    Parallel(n_jobs=5)(delayed(cdo_mul)(f"D/Dr_{2003+j}_tmp2.nc4", "mask123.nc4", f"D/Dr_{2003+j}.nc4") for j in tqdm(range(18)))

def dp_Dbedrock():
    # remap the 0p1 resolution to 0p1 resolution(no need, but for the sake of formatting consistency)
    for j in range(18):
        print(f"year is {j+2003}")
        subprocess.run(f"cdo -b F32 -P 48 --no_remap_weights remapbil,mask1.nc4 D/Dbedrock_{2003+j}_tmp1.nc4 D/Dbedrock_{2003+j}_tmp2.nc4", shell=True, check=True)
    Parallel(n_jobs=5)(delayed(cdo_mul)(f"D/Dbedrock_{2003+j}_tmp2.nc4", "mask123.nc4", f"D/Dbedrock_{2003+j}.nc4") for j in tqdm(range(18)))

def dp_Dbedrock_median():
    name_list = []
    for year in range(2003,2021):
        name = f'D/Dbedrock_{year}_tmp1.nc4'
        name_list.append(name)

    datasets = [xr.open_dataset(file) for file in name_list]
    data_arrays = [ds['Dbedrock'].values for ds in datasets]
    median_data = np.median(data_arrays, axis=0)

    output_file = 'Dbedrock_median_tmp1.nc4'
    median_ds = xr.Dataset(
        {'Dbedrock': (['lat', 'lon'], median_data)}, 
        coords={'lat': datasets[0].lat, 'lon': datasets[0].lon} 
    )
    median_ds.to_netcdf(output_file)

    subprocess.run(f"cdo -b F32 -P 48 --no_remap_weights remapbil,mask1.nc4 Dbedrock_median_tmp1.nc4 Dbedrock_median_tmp2.nc4", shell=True, check=True)
    cdo_mul("Dbedrock_median_tmp2.nc4", "mask123.nc4", "Dbedrock_median.nc4")

def dp_Dbedrock_mean():
    name_list = 'cdo -O -ensmean '
    for year in range(2003,2021):
        name = f'D/Dbedrock_{year}_tmp1.nc4'
        name_list = name_list+' '+name
    output_file = 'Dbedrock_mean_tmp1.nc4'
    print(name_list+' '+output_file)
    os.system(name_list+' '+output_file)

    subprocess.run(f"cdo -b F32 -P 48 --no_remap_weights remapbil,mask1.nc4 Dbedrock_mean_tmp1.nc4 Dbedrock_mean_tmp2.nc4", shell=True, check=True)
    cdo_mul("Dbedrock_mean_tmp2.nc4", "mask123.nc4", "Dbedrock_mean.nc4")

def dp_Dbedrock_Frequency():
    # calculate Dbedrock Frequency
    s1 = 0
    for year in range(2003,2021):
        file = f'D/Dbedrock_{year}.nc4'
        image = xr.open_dataset(file)
        s = image['Dbedrock']
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

    file_mask = f'mask12.nc4'
    mask = xr.open_dataset(file_mask)
    s2 = mask['Band1']
    print(s1.min(),s1.max())

    s1 = np.where((s1==0) & (s2 == 1), 4, s1)
    # s1 = np.where((s1==0), np.nan, s1)

    print(s1.min(),s1.max())
    shutil.copyfile('D/Dbedrock_2003.nc4', 'Dbedrock_Frequency.nc4')

    with nc.Dataset('Dbedrock_Frequency.nc4', 'a') as file:
        s_var = file.variables['Dbedrock']
        new_s_data = s1 
        s_var[:,:] = new_s_data

    # os.system('cdo -b F32 -P 48 --no_remap_weights remapbil,mask1.nc4 Dbedrock_Frequency_tmp1.nc4 Dbedrock_Frequency_tmp2.nc4')
    # os.system('cdo mul Dbedrock_Frequency_tmp2.nc4 mask123.nc4 Dbedrock_Frequency.nc4')


def dp_FD_median():
    name_list = []
    for year in range(2003,2021):
        name = f'D/D_FD_{year}_tmp1.nc4'
        name_list.append(name)

    datasets = [xr.open_dataset(file) for file in name_list]
    data_arrays = [ds['FD'].values for ds in datasets]
    median_data = np.median(data_arrays, axis=0)

    output_file = 'D_FD_median_tmp1.nc4'
    median_ds = xr.Dataset(
        {'FD': (['lat', 'lon'], median_data)}, 
        coords={'lat': datasets[0].lat, 'lon': datasets[0].lon} 
    )
    median_ds.to_netcdf(output_file)

    subprocess.run(f"cdo -b F32 -P 48 --no_remap_weights remaplaf,mask1.nc4 D_FD_median_tmp1.nc4 D_FD_median_tmp2.nc4", shell=True, check=True)
    cdo_mul("D_FD_median_tmp2.nc4", "mask123.nc4", "D_FD_median.nc4")

def dp_FD_median_to_FM_median():
    dp_FD_median()
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    sumday = 0
    command_list = ''
    for i, day in enumerate(days_in_month):
        sumday += day  
        command_name = f"-setrtoc,{sumday-day},{sumday},{i+1} "
        command_list = command_name + command_list
    command = f'cdo {command_list}D_FD_median_tmp1.nc4 D_FM_median_tmp1.nc4'
    print(f"Executing: {command}")  
    os.system(command)

    subprocess.run(f"cdo -b F32 -P 48 --no_remap_weights remaplaf,mask1.nc4 D_FM_median_tmp1.nc4 D_FM_median_tmp2.nc4", shell=True, check=True)
    os.system('cdo mul D_FM_median_tmp2.nc4 mask123.nc4 D_FM_median.nc4')

def dp_FD_mean():
    name_list = 'cdo -O -ensmean '
    for year in range(2003,2021):
        name = f'D/D_FD_{year}_tmp1.nc4'
        name_list = name_list+' '+name

    output_file = 'D_FD_mean_tmp1.nc4'
    os.system(name_list+' '+output_file)

    subprocess.run(f"cdo -b F32 -P 48 --no_remap_weights remapbil,mask1.nc4 D_FD_mean_tmp1.nc4 D_FD_mean_tmp2.nc4", shell=True, check=True)
    cdo_mul("D_FD_mean_tmp2.nc4", "mask123.nc4", "D_FD_mean.nc4")

def dp_FD_mean_to_FM_mean():
    dp_FD_mean()
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    sumday = 0
    command_list = ''
    for i, day in enumerate(days_in_month):
        sumday += day  
        command_name = f"-setrtoc,{sumday-day},{sumday},{i+1} "
        command_list = command_name + command_list
    command = f'cdo {command_list}D_FD_mean_tmp1.nc4 D_FM_mean_tmp1.nc4'
    print(f"Executing: {command}")  
    os.system(command)

    subprocess.run(f"cdo -b F32 -P 48 --no_remap_weights remaplaf,mask1.nc4 D_FM_mean_tmp1.nc4 D_FM_mean_tmp2.nc4", shell=True, check=True)
    os.system('cdo mul D_FM_mean_tmp2.nc4 mask123.nc4 D_FM_mean.nc4')

def dp_D_Duration_median():
    name_list = []
    for year in range(2003,2021):
        name = f'D/D_Duration_{year}_tmp1.nc4'
        name_list.append(name)

    datasets = [xr.open_dataset(file) for file in name_list]
    data_arrays = [ds['Duration'].values for ds in datasets]
    median_data = np.median(data_arrays, axis=0)

    output_file = 'D_Duration_median_tmp1.nc4'
    median_ds = xr.Dataset(
        {'Duration': (['lat', 'lon'], median_data)}, 
        coords={'lat': datasets[0].lat, 'lon': datasets[0].lon} 
    )
    median_ds.to_netcdf(output_file)

    subprocess.run(f"cdo -b F32 -P 48 --no_remap_weights remapbil,mask1.nc4 D_Duration_median_tmp1.nc4 D_Duration_median_tmp2.nc4", shell=True, check=True)
    cdo_mul("D_Duration_median_tmp2.nc4", "mask123.nc4", "D_Duration_median.nc4")

def dp_D_Duration_mean():
    name_list = 'cdo -O -ensmean '
    for year in range(2003,2021):
        name = f'D/D_Duration_{year}_tmp1.nc4'
        name_list = name_list+' '+name

    output_file = 'D_Duration_mean_tmp1.nc4'
    os.system(name_list+' '+output_file)

    subprocess.run(f"cdo -b F32 -P 48 --no_remap_weights remapbil,mask1.nc4 D_Duration_mean_tmp1.nc4 D_Duration_mean_tmp2.nc4", shell=True, check=True)
    cdo_mul("D_Duration_mean_tmp2.nc4", "mask123.nc4", "D_Duration_mean.nc4")

def dp_D_Duration_set0_to_nan():
    Parallel(n_jobs=5)(delayed(cdo_setvals)(f"D/D_Duration_{2003+j}_tmp1.nc4", f"D/D_Duration_{2003+j}_set0_to_nan_tmp1.nc4") for j in tqdm(range(18)))

def dp_D_Duration_set0_to_nan_median():
    name_list = []
    for year in range(2003,2021):
        name = f'D/D_Duration_set0_to_nan_{year}_tmp1.nc4'
        name_list.append(name)

    datasets = [xr.open_dataset(file) for file in name_list]
    data_arrays = [ds['Duration'].values for ds in datasets]
    median_data = np.median(data_arrays, axis=0)

    output_file = 'D_Duration_set0_to_nan_median_tmp1.nc4'
    median_ds = xr.Dataset(
        {'Duration': (['lat', 'lon'], median_data)}, 
        coords={'lat': datasets[0].lat, 'lon': datasets[0].lon} 
    )
    median_ds.to_netcdf(output_file)

    subprocess.run(f"cdo -b F32 -P 48 --no_remap_weights remapbil,mask1.nc4 D_Duration_set0_to_nan_median_tmp1.nc4 D_Duration_set0_to_nan_median_tmp2.nc4", shell=True, check=True)
    cdo_mul("D_Duration_set0_to_nan_median_tmp2.nc4", "mask123.nc4", "D_Duration_set0_to_nan_median.nc4")

def dp_D_Duration_set0_to_nan_mean():
    name_list = 'cdo -O -ensmean '
    for year in range(2003,2021):
        name = f'D/D_Duration_set0_to_nan_{year}_tmp1.nc4'
        name_list = name_list+' '+name

    output_file = 'D_Duration_set0_to_nan_mean_tmp1.nc4'
    os.system(name_list+' '+output_file)

    subprocess.run(f"cdo -b F32 -P 48 --no_remap_weights remapbil,mask1.nc4 D_Duration_set0_to_nan_mean_tmp1.nc4 D_Duration_set0_to_nan_mean_tmp2.nc4", shell=True, check=True)
    cdo_mul("D_Duration_set0_to_nan_mean_tmp2.nc4", "mask123.nc4", "D_Duration_set0_to_nan_mean.nc4")

def dp_D_Duration_set0_to_nan_max():
    name_list = 'cdo -O -ensmax '
    for year in range(2003,2021):
        name = f'D/D_Duration_set0_to_nan_{year}_tmp1.nc4'
        name_list = name_list+' '+name

    output_file = 'D_Duration_set0_to_nan_max_tmp1.nc4'
    os.system(name_list+' '+output_file)

    subprocess.run(f"cdo -b F32 -P 48 --no_remap_weights remapbil,mask1.nc4 D_Duration_set0_to_nan_max_tmp1.nc4 D_Duration_set0_to_nan_max_tmp2.nc4", shell=True, check=True)
    cdo_mul("D_Duration_set0_to_nan_max_tmp2.nc4", "mask123.nc4", "D_Duration_set0_to_nan_max.nc4")

if __name__=='__main__':
    # dp_Dbedrock()
    # dp_Dr()
    # dp_Dbedrock_median()
    # dp_Dbedrock_mean()
    # dp_Dbedrock_Frequency()
    # dp_FD_median_to_FM_median()
    # dp_FD_mean_to_FM_mean()
    # dp_D_Duration_median()
    # dp_D_Duration_mean()
    dp_D_Duration_set0_to_nan()
    dp_D_Duration_set0_to_nan_median()
    dp_D_Duration_set0_to_nan_mean()
    dp_D_Duration_set0_to_nan_max()