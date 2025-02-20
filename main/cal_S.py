import os
import subprocess
import numpy as np
import xarray as xr
from myfunc import timer
from myfunc import DirMan
import config

resolution = config.resolution
data_path = config.data_path

dir_man = DirMan(data_path)
dir_man.enter()

def cal_S():
    # Read data
    ds = xr.open_dataset(f'{data_path}diff.nc4')
    current_diff = ds['et'].load()
    ds2 = xr.open_dataset(f'{data_path}SnowCover.nc4')
    snowf = ds2['snowf'].load()
    ds3 = xr.open_dataset(f'{data_path}../0p1/Ssoil.nc4')
    ssoil = ds3['Band1'].load()

    # Obtain shape and duration
    shape = current_diff.isel(time=0).shape
    time_len = len(ds.time)

    # Initialize variables
    current_cwd = np.zeros(shape) 
    sr = np.zeros(shape)
    # sbedrock = np.zeros(shape)

    use_sbedrock_first_day = np.zeros(shape)
    use_sbedrock_duration = np.zeros(shape)
    use_sbedrock_period = np.zeros((time_len, *shape))

    for i in range(time_len):
        print(f"Processing time index: {i}")
        day_stt = 8*i+1-3*(i//46)+((i//46)+2)//4
        day_end = 8*(i+1)+1-3*((i+1)//46)+(((i+1)//46)+2)//4-1
        day_duration = day_end-day_stt+1
        print(f"the period {i+1:3} day from {day_stt:4} to {day_end:4}")
        print(f"the period {i+1:3} day is {day_duration:1}")

        # Calculate current delta_tn, cwd and sr
        current_delta_tn = current_diff.isel(time=i).values * snowf.isel(time=i).values
        current_cwd = np.where(current_delta_tn >= 0, current_cwd + current_delta_tn, 0)
        sr = np.maximum(sr, current_cwd)

        # Calculate the first day, duration and all time periods of using bedrock water  
        mask = current_cwd > ssoil
        use_sbedrock_first_day = np.where((use_sbedrock_first_day == 0) & mask, day_stt, use_sbedrock_first_day)
        use_sbedrock_duration = np.where(mask, use_sbedrock_duration+day_duration, use_sbedrock_duration)
        use_sbedrock_period[i, :, :] = np.where(mask, 1, 0)

        # if i == 0:
        #     drought_period[i, :, :] = np.where(current_diff.isel(time=i) > 0, day_duration,0)

        # drought_period[i, :, :] = np.where(current_diff.isel(time=i)>0,drought_period[i-1,:,:]+day_duration,0) 

    # sbedrock = np.maximum(sr-ssoil, 0)
    
    output_ds = xr.Dataset({'Sr': (('lat', 'lon'), sr)},
                        coords={'lat': ds['lat'], 'lon': ds['lon']})
    output_ds.to_netcdf(f'{data_path}Sr_tmp1.nc4')

    output_ds1 = xr.Dataset({'Sbedrock': (('lat', 'lon'), (sr-ssoil).data)},
                        coords={'lat': ds['lat'], 'lon': ds['lon']})
    output_ds1.to_netcdf(f'{data_path}Sbedrock_tmp1.nc4')

    output_ds2 = xr.Dataset({'FD': (('lat', 'lon'), use_sbedrock_first_day)},
                        coords={'lat': ds['lat'], 'lon': ds['lon']})
    output_ds2.to_netcdf(f'{data_path}S_FD_tmp1.nc4')

    output_ds3 = xr.Dataset({'Duration': (('lat', 'lon'), use_sbedrock_duration)},
                        coords={'lat': ds['lat'], 'lon': ds['lon']})
    output_ds3.to_netcdf(f'{data_path}S_Duration_tmp1.nc4')

    output_ds4 = xr.Dataset({'Period': (('time', 'lat', 'lon'), use_sbedrock_period)},
                        coords={'time': ds['time'], 'lat': ds['lat'], 'lon': ds['lon']})
    output_ds4.to_netcdf(f'{data_path}S_Period_tmp1.nc4')

    # output_ds5 = xr.Dataset({'Drought_Period': (('time', 'lat', 'lon'), drought_period)},
    #                     coords={'time': ds['time'], 'lat': ds['lat'], 'lon': ds['lon']})
    # output_ds5.to_netcdf(f'{data_path}Drought_Period_tmp1.nc4')

    ds.close()
    ds2.close()
    ds3.close()

def cal_drought():
    ds = xr.open_dataset(f'{data_path}diff.nc4')
    current_diff = ds['et'].load()

    shape = current_diff.isel(time=0).shape
    time_len = len(ds.time)

    drought_period = np.zeros((time_len, *shape))
    for i in range(time_len):
        print(f"Processing time index: {i}")
        day_stt = 8*i+1-3*(i//46)+((i//46)+2)//4
        day_end = 8*(i+1)+1-3*((i+1)//46)+(((i+1)//46)+2)//4-1
        day_duration = day_end-day_stt+1
        print(f"the period {i+1:3} day from {day_stt:4} to {day_end:4}")
        print(f"the period {i+1:3} day is {day_duration:1}")

        if i == 0:
            drought_period[i, :, :] = np.where(current_diff.isel(time=i) > 0, day_duration,0)

        drought_period[i, :, :] = np.where(current_diff.isel(time=i)>0,drought_period[i-1,:,:]+day_duration,0) 

    output_ds5 = xr.Dataset({'Drought_Period': (('time', 'lat', 'lon'), drought_period)},
                        coords={'time': ds['time'], 'lat': ds['lat'], 'lon': ds['lon']})
    output_ds5.to_netcdf(f'{data_path}Drought_Period_tmp1.nc4')

if __name__=='__main__':
    # cal_S()
    cal_drought()




