import os
import subprocess
import numpy as np
import xarray as xr
from myfunc import timer
from myfunc import DirMan
import config

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

def dp_Sbedrock():
    os.system(f"{remap_command} Sbedrock_tmp1.nc4 Sbedrock_tmp2.nc4")
    os.system(f"cdo mul Sbedrock_tmp2.nc4 mask1234.nc4 Sbedrock.nc4")
    print(f'The Sbedrock has finished')  

def dp_Sr():
    os.system(f'{remap_command} Sr_tmp1.nc4 Sr_tmp2.nc4')
    os.system(f"cdo mul Sr_tmp2.nc4 mask1234.nc4 Sr.nc4")
    print(f'The Sr has finished')    

# def dp_FD2FY():
#     os.system('cdo -b F32 -P 48 --no_remap_weights remapbil,mask1.nc4 S_FD_tmp1.nc4 S_FD_tmp2.nc4')
#     os.system('cdo mul S_FD_tmp2.nc4 mask1234.nc4 S_FD.nc4')

#     days_in_year = [366 if (i % 4 == 0 and (i % 100 != 0 or i % 400 == 0)) else 365 for i in range(2003,2021)]
#     sumday = 0
#     command_list = ''
#     for i, day in enumerate(days_in_year):
#         sumday += day  
#         command_name = f"-setrtoc,{sumday-day},{sumday},{i+1} "
#         command_list = command_name + command_list

#     command = f'cdo {command_list}-setrtoc,-1,0,0 S_FD_tmp2.nc4 S_FY_tmp1.nc4'
#     print(f"Executing: {command}")  
#     os.system(command)
#     os.system('cdo mul S_FY_tmp1.nc4 mask1234.nc4 S_FY.nc4')

# def dp_S_year_Frequency():
#     os.system(f'cdo setvals,0,nan S_Frequency_tmp1.nc4 S_Frequency_set0_to_nan_tmp1.nc4')
#     os.system(f'cdo timmean S_Frequency_set0_to_nan_tmp1.nc4 S_Frequency_mean_tmp1.nc4')
#     os.system(f'cdo timmax S_Frequency_set0_to_nan_tmp1.nc4 S_Frequency_max_tmp1.nc4')
#     os.system(f'cdo sub S_Frequency_max_tmp1.nc4 S_Frequency_mean_tmp1.nc4 S_Frequency_max_sub_mean_tmp1.nc4')

#     os.system(f'cdo -b F32 -P 48 --no_remap_weights remapbil,{resolution}.txt S_Frequency_mean_tmp1.nc4 S_Frequency_mean_tmp2.nc4')
#     os.system(f"cdo mul S_Frequency_mean_tmp2.nc4 mask1234.nc4 S_Frequency_mean.nc4")

#     os.system(f'cdo -b F32 -P 48 --no_remap_weights remapbil,{resolution}.txt S_Frequency_max_tmp1.nc4 S_Frequency_max_tmp2.nc4')
#     os.system(f"cdo mul S_Frequency_max_tmp2.nc4 mask1234.nc4 S_Frequency_max.nc4")

#     os.system(f'cdo -b F32 -P 48 --no_remap_weights remapbil,{resolution}.txt S_Frequency_max_sub_mean_tmp1.nc4 S_Frequency_max_sub_mean_tmp2.nc4')
#     os.system(f"cdo mul S_Frequency_max_sub_mean_tmp2.nc4 mask1234.nc4 S_Frequency_max_sub_mean.nc4")

# def dp_S_time():
#     os.system(f'cdo setvals,0,nan S_time_max_duration_tmp1.nc4 S_time_max_duration_tmp2.nc4')
#     os.system(f'cdo -b F32 -P 48 --no_remap_weights remapbil,{resolution}.txt S_time_max_duration_tmp2.nc4 S_time_max_duration_tmp3.nc4')
#     os.system(f"cdo mul S_time_max_duration_tmp3.nc4 mask1234.nc4 S_time_max_duration.nc4")

#     os.system(f'cdo setvals,0,nan S_time_mean_duration_tmp1.nc4 S_time_mean_duration_tmp2.nc4')
#     os.system(f'cdo -b F32 -P 48 --no_remap_weights remapbil,{resolution}.txt S_time_mean_duration_tmp2.nc4 S_time_mean_duration_tmp3.nc4')
#     os.system(f"cdo mul S_time_mean_duration_tmp3.nc4 mask1234.nc4 S_time_mean_duration.nc4")

#     os.system(f'cdo setvals,0,nan S_sum_Frequency_tmp1.nc4 S_sum_Frequency_tmp2.nc4')
#     os.system(f'cdo -b F32 -P 48 --no_remap_weights remapbil,{resolution}.txt S_sum_Frequency_tmp2.nc4 S_sum_Frequency_tmp3.nc4')
#     os.system(f"cdo mul S_sum_Frequency_tmp3.nc4 mask1234.nc4 S_sum_Frequency.nc4")

#     os.system(f'cdo setvals,0,nan S_sum_duration_tmp1.nc4 S_sum_duration_tmp2.nc4')
#     os.system(f'cdo -b F32 -P 48 --no_remap_weights remapbil,{resolution}.txt S_sum_duration_tmp2.nc4 S_sum_duration_tmp3.nc4')
#     os.system(f"cdo mul S_sum_duration_tmp3.nc4 mask1234.nc4 S_sum_duration.nc4")

# def dp_S_CY():
#     os.system(f'cdo setvals,0,nan S_CY_tmp1.nc4 S_CY_tmp2.nc4')
#     os.system(f'cdo -b F32 -P 48 --no_remap_weights remapbil,{resolution}.txt S_CY_tmp2.nc4 S_CY_tmp3.nc4')
#     os.system(f"cdo mul S_CY_tmp3.nc4 mask1234.nc4 S_CY.nc4")

# def dp_S_year_Duration():
#     os.system(f'cdo setvals,0,nan S_Duration_tmp1.nc4 S_Duration_set0_to_nan_tmp1.nc4')
#     os.system(f'cdo timmean S_Duration_set0_to_nan_tmp1.nc4 S_Duration_mean_tmp1.nc4')
#     os.system(f'cdo timmax S_Duration_set0_to_nan_tmp1.nc4 S_Duration_max_tmp1.nc4')
#     os.system(f'cdo sub S_Duration_max_tmp1.nc4 S_Duration_mean_tmp1.nc4 S_Duration_max_sub_mean_tmp1.nc4')

#     os.system(f'cdo -b F32 -P 48 --no_remap_weights remapbil,{resolution}.txt S_Duration_mean_tmp1.nc4 S_Duration_mean_tmp2.nc4')
#     os.system(f"cdo mul S_Duration_mean_tmp2.nc4 mask1234.nc4 S_Duration_mean.nc4")

#     os.system(f'cdo -b F32 -P 48 --no_remap_weights remapbil,{resolution}.txt S_Duration_max_tmp1.nc4 S_Duration_max_tmp2.nc4')
#     os.system(f"cdo mul S_Duration_max_tmp2.nc4 mask1234.nc4 S_Duration_max.nc4")

#     os.system(f'cdo -b F32 -P 48 --no_remap_weights remapbil,{resolution}.txt S_Duration_max_sub_mean_tmp1.nc4 S_Duration_max_sub_mean_tmp2.nc4')
#     os.system(f"cdo mul S_Duration_max_sub_mean_tmp2.nc4 mask1234.nc4 S_Duration_max_sub_mean.nc4")

# def dp_S_year_FD():
#     os.system(f'cdo setvals,0,nan S_FD_tmp1.nc4 S_FD_set0_to_nan_tmp1.nc4')
#     os.system(f'cdo timmean S_FD_set0_to_nan_tmp1.nc4 S_FD_mean_tmp1.nc4')
#     os.system(f'cdo timmax S_FD_set0_to_nan_tmp1.nc4 S_FD_max_tmp1.nc4')
#     os.system(f'cdo sub S_FD_max_tmp1.nc4 S_FD_mean_tmp1.nc4 S_FD_max_sub_mean_tmp1.nc4')

#     os.system(f'cdo -b F32 -P 48 --no_remap_weights remapbil,{resolution}.txt S_FD_mean_tmp1.nc4 S_FD_mean_tmp2.nc4')
#     os.system(f"cdo mul S_FD_mean_tmp2.nc4 mask1234.nc4 S_FD_mean.nc4")

#     os.system(f'cdo -b F32 -P 48 --no_remap_weights remapbil,{resolution}.txt S_FD_max_tmp1.nc4 S_FD_max_tmp2.nc4')
#     os.system(f"cdo mul S_FD_max_tmp2.nc4 mask1234.nc4 S_FD_max.nc4")

#     os.system(f'cdo -b F32 -P 48 --no_remap_weights remapbil,{resolution}.txt S_FD_max_sub_mean_tmp1.nc4 S_FD_max_sub_mean_tmp2.nc4')
#     os.system(f"cdo mul S_FD_max_sub_mean_tmp2.nc4 mask1234.nc4 S_FD_max_sub_mean.nc4")

# # def dp_S_Drought():
# #     os.system('cdo yearmax Drought_Period_tmp1.nc4 Drought_Period_yearmax_tmp1.nc4')
# #     os.system('cdo timmean Drought_Period_yearmax_tmp1.nc4 Drought_Period_yearmax_timmean_tmp1.nc4')
# #     os.system('cdo timmax Drought_Period_tmp1.nc4 Drought_Period_timmax_tmp1.nc4')

# #     os.system(f'cdo -b F32 -P 48 --no_remap_weights remapbil,{resolution}.txt Drought_Period_yearmax_timmean_tmp1.nc4 Drought_Period_yearmax_timmean_tmp2.nc4')
# #     os.system('cdo mul Drought_Period_yearmax_timmean_tmp2.nc4 mask1234.nc4 Drought_Period_yearmax_timmean.nc4')

# #     os.system(f'cdo -b F32 -P 48 --no_remap_weights remapbil,{resolution}.txt Drought_Period_timmax_tmp1.nc4 Drought_Period_timmax_tmp2.nc4')
# #     os.system('cdo mul Drought_Period_timmax_tmp2.nc4 mask1234.nc4 Drought_Period_timmax.nc4')

# #     os.system('cdo sub Drought_Period_timmax.nc4 Drought_Period_yearmax_timmean.nc4 Drought_Period_sub.nc4')

# def dp_S_Drought():
#     # os.system('cdo yearmax Drought_Period_tmp1.nc4 Drought_Period_yearmax_tmp1.nc4')
#     # os.system(f'cdo -b F32 -P 48 --no_remap_weights remapbil,{resolution}.txt Drought_Period_timmax_tmp1.nc4 Drought_Period_timmax_tmp2.nc4')
#     # os.system('cdo mul Drought_Period_timmax_tmp2.nc4 mask1234.nc4 Drought_Period_timmax.nc4')

#     os.system('cdo timmean Drought_Period_yearmax_tmp1.nc4 Drought_Period_yearmax_timmean_tmp1.nc4')
#     os.system(f'cdo -b F32 -P 48 --no_remap_weights remapbil,{resolution}.txt Drought_Period_yearmax_timmean_tmp1.nc4 Drought_Period_yearmax_timmean_tmp2.nc4')
#     os.system('cdo mul Drought_Period_yearmax_timmean_tmp2.nc4 mask1234.nc4 Drought_Period_yearmax_timmean.nc4')

#     # os.system('cdo yearmax Drought_Period_tmp1.nc4 Drought_Period_yearmax_tmp1.nc4')
#     # ds = xr.open_dataset(f'{data_path}Drought_Period_yearmax_tmp1.nc4')
#     # drought_duration_yearmax = ds['Drought_Period'].load()
#     # drought_duration_yearmax_median = np.median(drought_duration_yearmax, axis=0)

#     # output_file = 'Drought_Period_yearmax_median_tmp1.nc4'
#     # median_ds = xr.Dataset(
#     #                 {'Dbedrock': (['lat', 'lon'], drought_duration_yearmax_median)}, 
#     #                 coords={'lat': drought_duration_yearmax.lat, 'lon': drought_duration_yearmax.lon} 
#     #                 )
#     # median_ds.to_netcdf(output_file)    
#     # os.system(f'cdo -b F32 -P 48 --no_remap_weights remapbil,{resolution}.txt Drought_Period_yearmax_median_tmp1.nc4 Drought_Period_yearmax_median_tmp2.nc4')
#     # os.system('cdo mul Drought_Period_yearmax_median_tmp2.nc4 mask1234.nc4 Drought_Period_yearmax_median.nc4')

#     # os.system('cdo sub Drought_Period_timmax.nc4 Drought_Period_yearmax_median.nc4 Drought_Period_max_sub_median.nc4')

if __name__=='__main__':
    dp_Sbedrock()
    dp_Sr()

    # dp_FD2FY()
    # dp_S_Drought()
    # dp_S_year_Frequency()
    # dp_S_time()
    # dp_S_CY()
    # dp_S_year_Duration()
    # dp_S_year_FD()