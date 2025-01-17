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
from datetime import datetime, timedelta

resolution = config.resolution
name = config.name
data_path = config.data_path

def get_step_info():
    all_step = 828
    stt_y = np.zeros(all_step)
    stt_m = np.zeros(all_step)
    stt_d = np.zeros(all_step)
    stt_i = np.zeros(18*12)
    end_y = np.zeros(all_step)
    end_m = np.zeros(all_step)
    end_d = np.zeros(all_step)
    end_i = np.zeros(18*12)
    stt_last = np.zeros(all_step)
    end_last = np.zeros(all_step)
    cum_d = np.zeros(all_step)
    s = 0

    start_date = datetime(2003, 1, 1)
    current_date = start_date
    cumulative_days = 0

    # Iterate through each step to find the correct range
    for current_step in range(1, all_step + 1):
        # Determine the interval length
        if current_date.year % 4 == 0 and (current_date.year % 100 != 0 or current_date.year % 400 == 0):
            # Leap year
            if current_step % 46 == 0:
                interval_length = 6
            else:
                interval_length = 8
        else:
            # Non-leap year
            if current_step % 46 == 0:
                interval_length = 5
            else:
                interval_length = 8


        next_date = current_date + timedelta(days=interval_length)
        cumulative_days += interval_length

        start = current_date
        end = next_date - timedelta(days=1)
        end_temorrow = next_date
        stt_y[current_step-1],stt_m[current_step-1],stt_d[current_step-1] = start.year,start.month,start.day
        end_y[current_step-1],end_m[current_step-1],end_d[current_step-1] = end.year,end.month,end.day
        cum_d[current_step-1] = cumulative_days - interval_length + 1

        # Check if the step crosses a month boundary
        if start.month != end.month:
            start_month_days = (datetime(start.year, start.month + 1, 1) - start).days
            end_month_days = (end - datetime(end.year, end.month, 1)).days + 1

            stt_last[current_step-1] = start_month_days
            end_last[current_step-1] = end_month_days
            end_i[s] = current_step - 1
            s = s+1
            stt_i[s] = current_step - 1
        elif end.month != end_temorrow.month:
            end_i[s] = current_step - 1
            s = s+1
            if s != 216:
                stt_i[s] = current_step

        current_date = next_date

    return stt_i,end_i,stt_last,end_last

# Calculate Dr(the Culmulate Water Deficit - CWD) version2 and 
# the first month to use bedrock water
@timer
def Dr_mon():
    stt_i,end_i,stt_last,end_last = get_step_info()

    ds = xr.open_dataset('diff.nc')
    data_var = ds['et'].load()
    ds2 = xr.open_dataset('SnowCover.nc')
    snowf = ds2['snowf'].load()

    shape = data_var.isel(time=0).shape
    # time_len = len(ds.time)

    # deficit_acc = np.zeros((time_len, *shape))

    for j in range(18*12):
        print(f"year is {j//12+2003}")
        print(f"mon is {j%12+1}")

        pmax = np.zeros(shape) 
        pmin = np.zeros(shape)  
        Drv1 = np.zeros(shape)
        data_acc = np.zeros(shape)
        p = np.zeros(shape)
        n = np.zeros(shape)

        for i in range(int(stt_i[j]),int(end_i[j])+1):
            print(i)
            if i == int(stt_i[j]) and stt_i[j] == end_i[j-1]:
                plus = (1-stt_last[i]/8)
            elif j!=215 and i == int(end_i[j]) and stt_i[j+1] == end_i[j]:
                plus = (1-end_last[i]/8)
            else:
                plus = 1

            current_data_mask = data_var.isel(time=i).values * snowf.isel(time=i).values * plus
            if (i+1)%46 != 0:
                next_data_mask = data_var.isel(time=i + 1).values * snowf.isel(time=i + 1).values * plus
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
            
        # Save the results to a new NetCDF file
        output_ds = xr.Dataset({'Dr': (('lat', 'lon'), Drv1)},
                            coords={'lat': ds['lat'], 'lon': ds['lon']})
        output_ds.to_netcdf(f'temp/Dr_{2003+j//12}_{j%12+1}_temp1.nc')
        del data_acc, pmax, pmin, Drv1

    # Close datasets
    ds.close()
    ds2.close()  

# Set cdo function to use parallel operations 
def cdo_mul(filename1, filename2, filename3):
    subprocess.run(f"cdo mul {filename1} {filename2} {filename3}", shell=True, check=True)
    
def cdo_sub(filename1, filename2, filename3):
    subprocess.run(f"cdo sub {filename1} {filename2} {filename3}", shell=True, check=True)
    
def cdo_expr(filename1, filename2, nday):
    subprocess.run(f'cdo -setrtoc,-inf,0,0 -expr,"Ee=Dr*1000*2257/(3600*24*{nday})" {filename1} {filename2}', shell=True, check=True)

# Mask Dr
@timer
def Dr_mask():
    # remap the 0p1 resolution to 0p1 resolution(no need, but for the sake of formatting consistency)
    for j in range(18*12):
        print(j+2003)
        subprocess.run(f"cdo -b F32 -P 12 --no_remap_weights remapbil,mask1.nc temp/Dr_{2003+j//12}_{j%12+1}_temp1.nc temp/Dr_{2003+j//12}_{j%12+1}_temp2.nc", shell=True, check=True)
    
    Parallel(n_jobs=5)(delayed(cdo_mul)(f"temp/Dr_{2003+j//12}_{j%12+1}_temp2.nc", "mask123.nc", f"temp/Dr_{2003+j//12}_{j%12+1}.nc") for j in tqdm(range(18*12)))


# Calculate Dbedrock(rock moisture) 
@timer
def Db():
    Parallel(n_jobs=5)(delayed(cdo_sub)(f"temp/Dr_{2003+j//12}_{j%12+1}.nc", "Ssoil.nc", f"temp/Dbedrock_{2003+j//12}_{j%12+1}_temp1.nc") for j in tqdm(range(18*12)))
    
    Parallel(n_jobs=5)(delayed(cdo_mul)(f"temp/Dbedrock_{2003+j//12}_{j%12+1}_temp1.nc", "mask123.nc", f"temp/Dbedrock_{2003+j//12}_{j%12+1}.nc") for j in tqdm(range(18*12)))

def cal_Dbedrock_mon_median():
    for mon in range(1,13):
        name_list = []
        for year in range(2003,2021):
            name = f'Dbedrock/Dbedrock_{year}_{mon}.nc'
            name_list.append(name)

        datasets = [xr.open_dataset(file) for file in name_list]
        data_arrays = [ds['Dr'].values for ds in datasets]
        median_data = np.median(data_arrays, axis=0)

        output_file = f'Dbedrock/Dbedrock_{mon}_median.nc'
        median_ds = xr.Dataset(
            {'Dr': (['lat', 'lon'], median_data)}, 
            coords={'lat': datasets[0].lat, 'lon': datasets[0].lon} 
        )
        median_ds.to_netcdf(output_file)
        # os.system('cdo -b F32 -P 12 --no_remap_weights remapbil,mask1.nc FD_median_temp1.nc FD_median_temp2.nc')
        # os.system('cdo mul FD_median_temp2.nc mask123.nc FD_median.nc')

def LH_mon_median():
    monday = [31,28,31,30,31,30,31,31,30,31,30,31]    
    Parallel(n_jobs=5)(delayed(cdo_expr)(f"Dbedrock_{j+1}_median.nc", f"LH_{j+1}_median.nc", f"{monday[j]}") for j in tqdm(range(12)))
    # Parallel(n_jobs=5)(delayed(cdo_mul)(f"LH_{2003+j}_temp1.nc", "mask123.nc", f"LH_{2003+j}.nc") for j in tqdm(range(12)))

def cal_Dr_mon_median():
    for mon in range(1,13):
        name_list = []
        for year in range(2003,2021):
            name = f'Dr/Dr_{year}_{mon}.nc'
            name_list.append(name)

        datasets = [xr.open_dataset(file) for file in name_list]
        data_arrays = [ds['Dr'].values for ds in datasets]
        median_data = np.median(data_arrays, axis=0)

        output_file = f'Dr/Dr_{mon}_median.nc'
        median_ds = xr.Dataset(
            {'Dr': (['lat', 'lon'], median_data)}, 
            coords={'lat': datasets[0].lat, 'lon': datasets[0].lon} 
        )
        median_ds.to_netcdf(output_file)
        # os.system('cdo -b F32 -P 12 --no_remap_weights remapbil,mask1.nc FD_median_temp1.nc FD_median_temp2.nc')
        # os.system('cdo mul FD_median_temp2.nc mask123.nc FD_median.nc')

def LH_mon_Dr_median():
    monday = [31,28,31,30,31,30,31,31,30,31,30,31]    
    Parallel(n_jobs=5)(delayed(cdo_expr)(f"Dr/Dr_{j+1}_median.nc", f"LH/LH_{j+1}_Dr_median.nc", f"{monday[j]}") for j in tqdm(range(12)))
    # Parallel(n_jobs=5)(delayed(cdo_mul)(f"LH_{2003+j}_temp1.nc", "mask123.nc", f"LH_{2003+j}.nc") for j in tqdm(range(12)))

# def LH_mon():
#     # Calculate Latent Heat(Ee=Sbedrock*1000*2257/(3600*24*30))
#     monday = [calendar.monthrange(year, month)[1] for year in range(2003, 2021) for month in range(1, 13)]
#     Parallel(n_jobs=5)(delayed(cdo_expr)(f"Dbedrock_{2003+j//12}_{j%12+1}.nc", f"LH_{2003+j//12}_{j%12+1}_temp1.nc", f"{monday[j]}") for j in tqdm(range(18*12)))
#     Parallel(n_jobs=5)(delayed(cdo_mul)(f"LH_{2003+j//12}_{j%12+1}_temp1.nc", "mask123.nc", f"LH_{2003+j//12}_{j%12+1}.nc") for j in tqdm(range(18*12)))

# def cal_LH_mon_median():
#     for mon in range(1,2):
#         name_list = []
#         for year in range(2003,2021):
#             name = f'LH_{year}_{mon}.nc'
#             name_list.append(name)

#         datasets = [xr.open_dataset(file) for file in name_list]
#         data_arrays = [ds['Ee'].values for ds in datasets]
#         median_data = np.median(data_arrays, axis=0)

#         output_file = f'LH_{mon}_median.nc'
#         median_ds = xr.Dataset(
#             {'Ee': (['lat', 'lon'], median_data)}, 
#             coords={'lat': datasets[0].lat, 'lon': datasets[0].lon} 
#         )
#         median_ds.to_netcdf(output_file)


def delete():
    os.system('rm -rf Dr_*_temp1.nc')
    os.system('rm -rf Dr_*_temp2.nc')
    os.system('rm -rf Dbedrock_*_temp1.nc') 
    os.system('rm -rf LH_*_temp1.nc') 

# Execute all program
def cal_D_mon():        
    # Transfer the current path to the calculation path
    dir_man = DirMan(data_path)
    dir_man.enter()
    path = os.getcwd()+'/'
    print("Current file path: ", path)

    # Dr_mon()
    # Dr_mask()
    # Db()
    # cal_Dbedrock_mon_median()
    # LH_mon_median()
    cal_Dr_mon_median()
    LH_mon_Dr_median()

    # LH_mon()
    # cal_LH_mon_median()

    # delete()
    
    # Transfer from the calculation path to the later path 
    dir_man.exit()
    path = os.getcwd()+'/'
    print("Current file path: ", path)


if __name__=='__main__':
    cal_D_mon()