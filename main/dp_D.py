import os
import shutil
import subprocess
import numpy as np
import xarray as xr
import netCDF4 as nc
from tqdm import tqdm, trange
from joblib import Parallel, delayed
from myfunc import timer
from myfunc import DirMan, run_command
import config
import calendar

# configuration
# resolution = "0p1"
resolution = "500"
region = [-180,180,-60,90]
data_path = f'/tera04/zhwei/xionghui/bedrock/run/{resolution}/'
post_data_path = '/tera04/zhwei/xionghui/bedrock/'
shp_path = '/tera04/zhwei/xionghui/bedrock/Shp/'
fig_path = f'/home/xuxh22/stu01/Bedrock/fig/{resolution}/'
path = '/home/xuxh22/stu01/Bedrock/'

if resolution == "0p1":
    size = 0.1
    lon_num = '3600'
    lat_num = '1800'
    remap_command = f'cdo -f nc4 -z zip -b F32 -P 48 --no_remap_weights -remapbil,{resolution}.txt'
elif resolution == "500":
    size = 0.0005
    lon_num = '86400'
    lat_num = '43200'
    lon_lat = f'{lon_num} {lat_num}'
    remap_command = f'gdalwarp -multi -wo NUM_THREADS=48 -ot Float32 -of netCDF -co FORMAT=NC4 -r bilinear -ts {lon_lat} -overwrite'


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

def cdo_setrtoc(filename1, filename2):
    subprocess.run(f'cdo -setrtoc,1e-1,inf,1 -setrtoc,-inf,1e-1,nan {filename1} {filename2}', shell=True, check=True)

def dp_Dr():
    # remap the 0p1 resolution to 0p1 resolution(no need, but for the sake of formatting consistency)
    for j in range(18):
        print(f"year is {j+2003}")
        subprocess.run(f"{remap_command} D/Dr_{2003+j}_tmp1.nc4 D/Dr_{2003+j}_tmp2.nc4", shell=True, check=True)
    Parallel(n_jobs=5)(delayed(cdo_mul)(f"D/Dr_{2003+j}_tmp2.nc4", "mask1234.nc4", f"D/Dr_{2003+j}.nc4") for j in tqdm(range(18)))

def dp_Dbedrock():
    # remap the 0p1 resolution to 0p1 resolution(no need, but for the sake of formatting consistency)
    # for j in range(18):
    # # for j in range(13,18):
    #     print(f"year is {j+2003}")
    #     # subprocess.run(f"{remap_command} D/Dbedrock_{2003+j}_tmp1.nc4 D/Dbedrock_{2003+j}_tmp2.nc4", shell=True, check=True)
    #     subprocess.run(f"cdo -f nc4 -z zip -b F32 -P 48 --no_remap_weights -remapbil,{resolution}.txt D/Dbedrock_{2003+j}_tmp1.nc4 D/Dbedrock_{2003+j}_tmp2.nc4", shell=True, check=True)
    
    name_list = 'cdo -O -ensmax '
    for year in range(2003,2021):
        name = f'D/Dbedrock_{year}_tmp1.nc4'
        name_list = name_list+' '+name
    output_file = 'Dbedrock_max_tmp1.nc4'
    print(name_list+' '+output_file)
    os.system(name_list+' '+output_file)

    subprocess.run(f"cdo -b F32 -P 48 --no_remap_weights remapbil,mask1.nc4 Dbedrock_max_tmp1.nc4 Dbedrock_max_tmp2.nc4", shell=True, check=True)

    run_command(f"cdo -O -f nc4 -z zip -setrtoc2,-inf,1e-1,nan,1 Dbedrock_max_tmp2.nc4 mask4.nc4")
    run_command(f"cdo -O mul mask123.nc4 mask4.nc4 mask1234.nc4")

    Parallel(n_jobs=5)(delayed(cdo_mul)(f"D/Dbedrock_{2003+j}_tmp2.nc4", "mask1234.nc4", f"D/Dbedrock_{2003+j}.nc4") for j in tqdm(range(18)))

# def dp_Dbedrock_median():
#     name_list = []
#     for year in range(2003,2021):
#         name = f'D/Dbedrock_{year}_tmp1.nc4'
#         name_list.append(name)

#     datasets = [xr.open_dataset(file) for file in name_list]
#     data_arrays = [ds['Dbedrock'].values for ds in datasets]
#     median_data = np.median(data_arrays, axis=0)

#     output_file = 'Dbedrock_median_tmp1.nc4'
#     median_ds = xr.Dataset(
#         {'Dbedrock': (['lat', 'lon'], median_data)}, 
#         coords={'lat': datasets[0].lat, 'lon': datasets[0].lon} 
#     )
#     median_ds.to_netcdf(output_file)

#     subprocess.run(f"cdo -b F32 -P 48 --no_remap_weights remapbil,mask1.nc4 Dbedrock_median_tmp1.nc4 Dbedrock_median_tmp2.nc4", shell=True, check=True)
#     cdo_mul("Dbedrock_median_tmp2.nc4", "mask1234.nc4", "Dbedrock_median.nc4")

# def dp_Dbedrock_mean():
#     name_list = 'cdo -O -ensmean '
#     for year in range(2003,2021):
#         name = f'D/Dbedrock_{year}_tmp1.nc4'
#         name_list = name_list+' '+name
#     output_file = 'Dbedrock_mean_tmp1.nc4'
#     print(name_list+' '+output_file)
#     os.system(name_list+' '+output_file)

#     subprocess.run(f"cdo -b F32 -P 48 --no_remap_weights remapbil,mask1.nc4 Dbedrock_mean_tmp1.nc4 Dbedrock_mean_tmp2.nc4", shell=True, check=True)
#     cdo_mul("Dbedrock_mean_tmp2.nc4", "mask1234.nc4", "Dbedrock_mean.nc4")

def dp_Dbedrock_Frequency():
    # Parallel(n_jobs=5)(delayed(cdo_setrtoc)(f"D/Dbedrock_{2003+j}.nc4", f"D/Dbedrock_{2003+j}_count.nc4") for j in tqdm(range(18)))
    # filelist = [f"D/Dbedrock_{2003+j}_count.nc4" for j in range(18)]
    # filelistname =' '.join(filelist)
    # run_command(f'cdo -O -f nc4 -z zip -enssum {filelistname} Dbedrock_count.nc4')
    # run_command(f"cdo -O -f nc4 -z zip -setrtoc,17.5,18.5,2 -setrtoc,0.5,17.5,1 -setrtoc,-inf,0.5,nan Dbedrock_count.nc4 temp.nc4 && ncap2 -O -s 'Band1=int(Band1)' temp.nc4 Dbedrock_Frequency_tmp1.nc4")
    # # os.system('cdo -O -b F32 -P 48 --no_remap_weights remapbil,mask1.nc4 Dbedrock_Frequency_tmp1.nc4 Dbedrock_Frequency_tmp2.nc4')
    # os.system('cdo -O mul Dbedrock_Frequency_tmp1.nc4 mask1234.nc4 Dbedrock_Frequency.nc4')

    # calculate Dbedrock Frequency
    s1 = 0
    for year in range(2003,2021):
        file = f'D/Dbedrock_{year}_tmp2.nc4'
        image = xr.open_dataset(file)
        # if resolution=='0p1':
        s = image['Dbedrock']
        # elif resolution=='500':
        #     s = image['Band1']

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
    shutil.copyfile('D/Dbedrock_2003.nc4', 'Dbedrock_Frequency_tmp1.nc4')

    with nc.Dataset('Dbedrock_Frequency_tmp1.nc4', 'a') as file:
        s_var = file.variables['Dbedrock']
        new_s_data = s1 
        s_var[:,:] = new_s_data

    # os.system('cdo -b F32 -P 48 --no_remap_weights remapbil,mask1.nc4 Dbedrock_Frequency_tmp1.nc4 Dbedrock_Frequency_tmp2.nc4')
    os.system('cdo mul Dbedrock_Frequency_tmp1.nc4 mask1234.nc4 Dbedrock_Frequency.nc4')


# def dp_FD_median():
#     name_list = []
#     for year in range(2003,2021):
#         name = f'D/D_FD_{year}_tmp1.nc4'
#         name_list.append(name)

#     datasets = [xr.open_dataset(file) for file in name_list]
#     data_arrays = [ds['FD'].values for ds in datasets]
#     median_data = np.median(data_arrays, axis=0)

#     output_file = 'D_FD_median_tmp1.nc4'
#     median_ds = xr.Dataset(
#         {'FD': (['lat', 'lon'], median_data)}, 
#         coords={'lat': datasets[0].lat, 'lon': datasets[0].lon} 
#     )
#     median_ds.to_netcdf(output_file)

#     subprocess.run(f"cdo -b F32 -P 48 --no_remap_weights remaplaf,mask1.nc4 D_FD_median_tmp1.nc4 D_FD_median_tmp2.nc4", shell=True, check=True)
#     cdo_mul("D_FD_median_tmp2.nc4", "mask1234.nc4", "D_FD_median.nc4")

# def dp_FD_median_to_FM_median():
#     dp_FD_median()
#     days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
#     sumday = 0
#     command_list = ''
#     for i, day in enumerate(days_in_month):
#         sumday += day  
#         command_name = f"-setrtoc,{sumday-day},{sumday},{i+1} "
#         command_list = command_name + command_list
#     command = f'cdo {command_list}D_FD_median_tmp1.nc4 D_FM_median_tmp1.nc4'
#     print(f"Executing: {command}")  
#     os.system(command)

#     subprocess.run(f"cdo -b F32 -P 48 --no_remap_weights remaplaf,mask1.nc4 D_FM_median_tmp1.nc4 D_FM_median_tmp2.nc4", shell=True, check=True)
#     os.system('cdo mul D_FM_median_tmp2.nc4 mask1234.nc4 D_FM_median.nc4')

# def dp_FD_mean():
#     name_list = 'cdo -O -ensmean '
#     for year in range(2003,2021):
#         name = f'D/D_FD_{year}_tmp1.nc4'
#         name_list = name_list+' '+name

#     output_file = 'D_FD_mean_tmp1.nc4'
#     os.system(name_list+' '+output_file)

#     subprocess.run(f"cdo -b F32 -P 48 --no_remap_weights remapbil,mask1.nc4 D_FD_mean_tmp1.nc4 D_FD_mean_tmp2.nc4", shell=True, check=True)
#     cdo_mul("D_FD_mean_tmp2.nc4", "mask1234.nc4", "D_FD_mean.nc4")

# def dp_FD_mean_to_FM_mean():
#     dp_FD_mean()
#     days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
#     sumday = 0
#     command_list = ''
#     for i, day in enumerate(days_in_month):
#         sumday += day  
#         command_name = f"-setrtoc,{sumday-day},{sumday},{i+1} "
#         command_list = command_name + command_list
#     command = f'cdo {command_list}D_FD_mean_tmp1.nc4 D_FM_mean_tmp1.nc4'
#     print(f"Executing: {command}")  
#     os.system(command)

#     subprocess.run(f"cdo -b F32 -P 48 --no_remap_weights remaplaf,mask1.nc4 D_FM_mean_tmp1.nc4 D_FM_mean_tmp2.nc4", shell=True, check=True)
#     os.system('cdo mul D_FM_mean_tmp2.nc4 mask1234.nc4 D_FM_mean.nc4')

# def dp_D_Duration_median():
#     name_list = []
#     for year in range(2003,2021):
#         name = f'D/D_Duration_{year}_tmp1.nc4'
#         name_list.append(name)

#     datasets = [xr.open_dataset(file) for file in name_list]
#     data_arrays = [ds['Duration'].values for ds in datasets]
#     median_data = np.median(data_arrays, axis=0)

#     output_file = 'D_Duration_median_tmp1.nc4'
#     median_ds = xr.Dataset(
#         {'Duration': (['lat', 'lon'], median_data)}, 
#         coords={'lat': datasets[0].lat, 'lon': datasets[0].lon} 
#     )
#     median_ds.to_netcdf(output_file)

#     subprocess.run(f"cdo -b F32 -P 48 --no_remap_weights remapbil,mask1.nc4 D_Duration_median_tmp1.nc4 D_Duration_median_tmp2.nc4", shell=True, check=True)
#     cdo_mul("D_Duration_median_tmp2.nc4", "mask1234.nc4", "D_Duration_median.nc4")

# def dp_D_Duration_mean():
#     name_list = 'cdo -O -ensmean '
#     for year in range(2003,2021):
#         name = f'D/D_Duration_{year}_tmp1.nc4'
#         name_list = name_list+' '+name

#     output_file = 'D_Duration_mean_tmp1.nc4'
#     os.system(name_list+' '+output_file)

#     subprocess.run(f"cdo -b F32 -P 48 --no_remap_weights remapbil,mask1.nc4 D_Duration_mean_tmp1.nc4 D_Duration_mean_tmp2.nc4", shell=True, check=True)
#     cdo_mul("D_Duration_mean_tmp2.nc4", "mask1234.nc4", "D_Duration_mean.nc4")

# def dp_D_Duration_set0_to_nan():
#     Parallel(n_jobs=5)(delayed(cdo_setvals)(f"D/D_Duration_{2003+j}_tmp1.nc4", f"D/D_Duration_{2003+j}_set0_to_nan_tmp1.nc4") for j in tqdm(range(18)))

# def dp_D_Duration_set0_to_nan_median():
#     name_list = []
#     for year in range(2003,2021):
#         name = f'D/D_Duration_set0_to_nan_{year}_tmp1.nc4'
#         name_list.append(name)

#     datasets = [xr.open_dataset(file) for file in name_list]
#     data_arrays = [ds['Duration'].values for ds in datasets]
#     median_data = np.median(data_arrays, axis=0)

#     output_file = 'D_Duration_set0_to_nan_median_tmp1.nc4'
#     median_ds = xr.Dataset(
#         {'Duration': (['lat', 'lon'], median_data)}, 
#         coords={'lat': datasets[0].lat, 'lon': datasets[0].lon} 
#     )
#     median_ds.to_netcdf(output_file)

#     subprocess.run(f"cdo -b F32 -P 48 --no_remap_weights remapbil,mask1.nc4 D_Duration_set0_to_nan_median_tmp1.nc4 D_Duration_set0_to_nan_median_tmp2.nc4", shell=True, check=True)
#     cdo_mul("D_Duration_set0_to_nan_median_tmp2.nc4", "mask1234.nc4", "D_Duration_set0_to_nan_median.nc4")

# def dp_D_Duration_set0_to_nan_mean():
#     name_list = 'cdo -O -ensmean '
#     for year in range(2003,2021):
#         name = f'D/D_Duration_set0_to_nan_{year}_tmp1.nc4'
#         name_list = name_list+' '+name

#     output_file = 'D_Duration_set0_to_nan_mean_tmp1.nc4'
#     os.system(name_list+' '+output_file)

#     subprocess.run(f"cdo -b F32 -P 48 --no_remap_weights remapbil,mask1.nc4 D_Duration_set0_to_nan_mean_tmp1.nc4 D_Duration_set0_to_nan_mean_tmp2.nc4", shell=True, check=True)
#     cdo_mul("D_Duration_set0_to_nan_mean_tmp2.nc4", "mask1234.nc4", "D_Duration_set0_to_nan_mean.nc4")

# def dp_D_Duration_set0_to_nan_max():
#     name_list = 'cdo -O -ensmax '
#     for year in range(2003,2021):
#         name = f'D/D_Duration_set0_to_nan_{year}_tmp1.nc4'
#         name_list = name_list+' '+name

#     output_file = 'D_Duration_set0_to_nan_max_tmp1.nc4'
#     os.system(name_list+' '+output_file)

#     subprocess.run(f"cdo -b F32 -P 48 --no_remap_weights remapbil,mask1.nc4 D_Duration_set0_to_nan_max_tmp1.nc4 D_Duration_set0_to_nan_max_tmp2.nc4", shell=True, check=True)
#     cdo_mul("D_Duration_set0_to_nan_max_tmp2.nc4", "mask1234.nc4", "D_Duration_set0_to_nan_max.nc4")

def dp_frequency_per_year():
    os.system(f'cdo -setrtoc,-0.5,0.5,nan D_frequency_per_year_tmp1.nc4 D_frequency_per_year_set0_to_nan_tmp1.nc4')
    os.system(f'cdo timmean D_frequency_per_year_set0_to_nan_tmp1.nc4 D_frequency_per_year_mean_tmp1.nc4')
    os.system(f'cdo timmax D_frequency_per_year_set0_to_nan_tmp1.nc4 D_frequency_per_year_max_tmp1.nc4')
    # os.system(f'cdo timmin D_frequency_per_year_set0_to_nan_tmp1.nc4 D_frequency_per_year_min_tmp1.nc4')
    # os.system(f'cdo sub D_frequency_per_year_max_tmp1.nc4 D_frequency_per_year_mean_tmp1.nc4 D_frequency_per_year_max_sub_mean_tmp1.nc4')
    # os.system(f'cdo sub D_frequency_per_year_max_tmp1.nc4 D_frequency_per_year_min_tmp1.nc4 D_frequency_per_year_max_sub_min_tmp1.nc4')

    os.system(f'{remap_command} D_frequency_per_year_mean_tmp1.nc4 D_frequency_per_year_mean_tmp2.nc4')
    os.system(f"cdo mul D_frequency_per_year_mean_tmp2.nc4 mask1234.nc4 D_frequency_per_year_mean.nc4")

    os.system(f'{remap_command} D_frequency_per_year_max_tmp1.nc4 D_frequency_per_year_max_tmp2.nc4')
    os.system(f"cdo mul D_frequency_per_year_max_tmp2.nc4 mask1234.nc4 D_frequency_per_year_max.nc4")

    # os.system(f'cdo -b F32 -P 48 --no_remap_weights remapbil,{resolution}.txt D_frequency_per_year_min_tmp1.nc4 D_frequency_per_year_min_tmp2.nc4')
    # os.system(f"cdo mul D_frequency_per_year_min_tmp2.nc4 mask1234.nc4 D_frequency_per_year_min.nc4")

    # os.system(f'cdo -b F32 -P 48 --no_remap_weights remapbil,{resolution}.txt D_frequency_per_year_max_sub_mean_tmp1.nc4 D_frequency_per_year_max_sub_mean_tmp2.nc4')
    # os.system(f"cdo mul D_frequency_per_year_max_sub_mean_tmp2.nc4 mask1234.nc4 D_frequency_per_year_max_sub_mean.nc4")
    
    # os.system(f'cdo -b F32 -P 48 --no_remap_weights remapbil,{resolution}.txt D_frequency_per_year_max_sub_min_tmp1.nc4 D_frequency_per_year_max_sub_min_tmp2.nc4')
    # os.system(f"cdo mul D_frequency_per_year_max_sub_min_tmp2.nc4 mask1234.nc4 D_frequency_per_year_max_sub_min.nc4")

def dp_sum_frequency():
    os.system(f'cdo -setrtoc,-0.5,0.5,nan D_sum_frequency_tmp1.nc4 D_sum_frequency_tmp2.nc4')
    os.system(f'{remap_command} D_sum_frequency_tmp2.nc4 D_sum_frequency_tmp3.nc4')
    os.system(f"cdo mul D_sum_frequency_tmp3.nc4 mask1234.nc4 D_sum_frequency.nc4")

def dp_duration_per_year():
    os.system(f'cdo -setrtoc,-0.5,0.5,nan D_duration_per_year_tmp1.nc4 D_duration_per_year_set0_to_nan_tmp1.nc4')
    os.system(f'cdo timmean D_duration_per_year_set0_to_nan_tmp1.nc4 D_duration_per_year_mean_tmp1.nc4')
    os.system(f'cdo timmax D_duration_per_year_set0_to_nan_tmp1.nc4 D_duration_per_year_max_tmp1.nc4')
    # os.system(f'cdo sub D_duration_per_year_max_tmp1.nc4 D_duration_per_year_mean_tmp1.nc4 D_duration_per_year_max_sub_mean_tmp1.nc4')

    os.system(f'{remap_command} D_duration_per_year_mean_tmp1.nc4 D_duration_per_year_mean_tmp2.nc4')
    os.system(f"cdo mul D_duration_per_year_mean_tmp2.nc4 mask1234.nc4 D_duration_per_year_mean.nc4")

    os.system(f'{remap_command} D_duration_per_year_max_tmp1.nc4 D_duration_per_year_max_tmp2.nc4')
    os.system(f"cdo mul D_duration_per_year_max_tmp2.nc4 mask1234.nc4 D_duration_per_year_max.nc4")

    # os.system(f'cdo -b F32 -P 48 --no_remap_weights remapbil,{resolution}.txt D_duration_per_year_max_sub_mean_tmp1.nc4 D_duration_per_year_max_sub_mean_tmp2.nc4')
    # os.system(f"cdo mul D_duration_per_year_max_sub_mean_tmp2.nc4 mask1234.nc4 D_duration_per_year_max_sub_mean.nc4")

def dp_duration_per_use():
    os.system(f'cdo -setrtoc,-0.5,0.5,nan D_duration_per_use_max_tmp1.nc4 D_duration_per_use_max_tmp2.nc4')
    os.system(f'{remap_command} D_duration_per_use_max_tmp2.nc4 D_duration_per_use_max_tmp3.nc4')
    os.system(f"cdo mul D_duration_per_use_max_tmp3.nc4 mask1234.nc4 D_duration_per_use_max.nc4")

    os.system(f'cdo -setrtoc,-0.5,0.5,nan D_duration_per_use_mean_tmp1.nc4 D_duration_per_use_mean_tmp2.nc4')
    os.system(f'{remap_command} D_duration_per_use_mean_tmp2.nc4 D_duration_per_use_mean_tmp3.nc4')
    os.system(f"cdo mul D_duration_per_use_mean_tmp3.nc4 mask1234.nc4 D_duration_per_use_mean.nc4")

def dp_sum_duration():
    os.system(f'cdo -setrtoc,-0.5,0.5,nan D_sum_duration_tmp1.nc4 D_sum_duration_tmp2.nc4')
    os.system(f'{remap_command} D_sum_duration_tmp2.nc4 D_sum_duration_tmp3.nc4')
    os.system(f"cdo mul D_sum_duration_tmp3.nc4 mask1234.nc4 D_sum_duration.nc4")

def dp_first_day():
    os.system(f'cdo -setrtoc,-0.5,0.5,nan D_first_day_tmp1.nc4 D_first_day_set0_to_nan_tmp1.nc4')
    # os.system(f'cdo timmean D_first_day_set0_to_nan_tmp1.nc4 D_first_day_mean_tmp1.nc4')
    os.system(f'cdo timmax D_first_day_set0_to_nan_tmp1.nc4 D_first_day_max_tmp1.nc4')
    os.system(f'cdo timmin D_first_day_set0_to_nan_tmp1.nc4 D_first_day_min_tmp1.nc4')
    # os.system(f'cdo sub D_first_day_max_tmp1.nc4 D_first_day_mean_tmp1.nc4 D_first_day_max_sub_mean_tmp1.nc4')
    os.system(f'cdo sub D_first_day_max_tmp1.nc4 D_first_day_min_tmp1.nc4 D_first_day_max_sub_min_tmp1.nc4')


    # os.system(f'cdo -b F32 -P 48 --no_remap_weights remapbil,{resolution}.txt D_first_day_mean_tmp1.nc4 D_first_day_mean_tmp2.nc4')
    # os.system(f"cdo mul D_first_day_mean_tmp2.nc4 mask1234.nc4 D_first_day_mean.nc4")

    # os.system(f'cdo -b F32 -P 48 --no_remap_weights remapbil,{resolution}.txt D_first_day_max_tmp1.nc4 D_first_day_max_tmp2.nc4')
    # os.system(f"cdo mul D_first_day_max_tmp2.nc4 mask1234.nc4 D_first_day_max.nc4")

    os.system(f'{remap_command} D_first_day_min_tmp1.nc4 D_first_day_min_tmp2.nc4')
    os.system(f"cdo mul D_first_day_min_tmp2.nc4 mask1234.nc4 D_first_day_min.nc4")

    # os.system(f'cdo -b F32 -P 48 --no_remap_weights remapbil,{resolution}.txt D_first_day_max_sub_mean_tmp1.nc4 D_first_day_max_sub_mean_tmp2.nc4')
    # os.system(f"cdo mul D_first_day_max_sub_mean_tmp2.nc4 mask1234.nc4 D_first_day_max_sub_mean.nc4")

    os.system(f'{remap_command} D_first_day_max_sub_min_tmp1.nc4 D_first_day_max_sub_min_tmp2.nc4')
    os.system(f"cdo mul D_first_day_max_sub_min_tmp2.nc4 mask1234.nc4 D_first_day_max_sub_min.nc4")

if __name__=='__main__':

    # dp_Dbedrock_median()
    # dp_Dbedrock_mean()
    # dp_FD_median_to_FM_median()
    # dp_FD_mean_to_FM_mean()
    # dp_D_Duration_median()
    # dp_D_Duration_mean()
    # dp_D_Duration_set0_to_nan()
    # dp_D_Duration_set0_to_nan_median()
    # dp_D_Duration_set0_to_nan_mean()
    # dp_D_Duration_set0_to_nan_max()

    # dp_Dr()
    # dp_Dbedrock()
    dp_Dbedrock_Frequency()

    # dp_frequency_per_year()
    # dp_sum_frequency()
    # dp_duration_per_year()
    # dp_duration_per_use()
    # dp_sum_duration()
    # dp_first_day()