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

# def day2mon(day):
#     # if year%4==0:
#     #     days_in_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
#     # else:
#     days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

#     cumulative_days = np.cumsum([0] + days_in_month)
#     for month in range(1, 13):
#         if cumulative_days[month - 1] <= day < cumulative_days[month]:
#             return month
#     return 12 

def cal_FD():
    name_list = 'cdo ensmean '
    for year in range(2003,2021):
        name = f'FD_{year}_temp1.nc '
        name_list = name_list+name
    name_list = name_list+'FD_mean_temp1.nc'
    os.system(name_list)
    os.system('cdo -b F32 -P 12 --no_remap_weights remapbil,mask1.nc FD_mean_temp1.nc FM_mean_temp2_0.nc')
    # ds = xr.open_dataset('FD_mean_temp2.nc') 
    # days = ds['FD'].values
    # months = np.vectorize(day2mon)(days)
    # ds["FM"] = (("time",), months)
    # ds.to_netcdf('FD_mean_temp3.nc')

    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    sumday = 0
    for i, day in enumerate(days_in_month):
        sumday += day  
        input_file = f"FM_mean_temp2_{i}.nc"     
        output_file = f"FM_mean_temp2_{i+1}.nc"  
        command = f'cdo setrtoc,{sumday-day},{sumday},{i+1} {input_file} {output_file}'
        print(f"Executing: {command}")  
        os.system(command)

    os.system('cdo mul FM_mean_temp2_12.nc mask123.nc FM_mean.nc')

# Execute all program
def cal_D():        
    # Transfer the current path to the calculation path
    dir_man = DirMan(data_path)
    dir_man.enter()
    path = os.getcwd()+'/'
    print("Current file path: ", path)

    Dr()
    Dr_mask()
    Db()
    delete()
    cal_DbF()
    cal_FD()
    
    # Transfer from the calculation path to the later path 
    dir_man.exit()
    path = os.getcwd()+'/'
    print("Current file path: ", path)


if __name__=='__main__':
    cal_D()