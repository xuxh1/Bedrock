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

# Calculate Dr(the Culmulate Water Deficit - CWD) and 
# the first month to use bedrock water
def cal_D():
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
    use_dbedrock_period = np.zeros((time_len, *shape))

    for j in range(18):
        print(f"year is {j+2003}")

        # Initialize variables
        current_cwd = np.zeros(shape) 
        dr = np.zeros(shape)
        # dbedrock = np.zeros(shape)
        use_dbedrock_first_day = np.zeros(shape)
        use_dbedrock_duration = np.zeros(shape)

        for i in range(0+46*j,46+46*j):
            print(f"Processing time index: {i}")
            day_stt = 8*(i-46*j)+1
            day_end = 8*(i-46*j)+1+\
                ((5 if ((j + 2003) % 4 == 0 and ((j + 2003) % 100 != 0 or (j + 2003) % 400 == 0)) else 4)\
                if (i+1) % 46 == 0 else 7)
            day_duration = day_end-day_stt+1
            print(f"the period {i-46*j+1:3} day from {day_stt:4} to {day_end:4}")
            print(f"the period {i-46*j+1:3} day is {day_duration:1}")

            # Calculate current delta_tn, cwd and sr
            current_delta_tn = current_diff.isel(time=i).values * snowf.isel(time=i).values
            current_cwd = np.where(current_delta_tn >= 0, current_cwd + current_delta_tn, 0)
            dr = np.maximum(dr, current_cwd)

            # Calculate the first day, duration and all time periods of using bedrock water  
            mask = current_cwd > ssoil
            use_dbedrock_first_day = np.where((use_dbedrock_first_day == 0) & mask, day_stt, use_dbedrock_first_day)
            use_dbedrock_duration = np.where(mask, use_dbedrock_duration+day_duration, use_dbedrock_duration)
            use_dbedrock_period[i, :, :] = np.where(mask, 1, 0)

        # dbedrock = np.maximum(dr-ssoil, 0)

        output_ds = xr.Dataset({'Dr': (('lat', 'lon'), dr)},
                        coords={'lat': ds['lat'], 'lon': ds['lon']})
        output_ds.to_netcdf(f'{data_path}D/Dr_{j+2003}_tmp1.nc4')

        output_ds1 = xr.Dataset({'Dbedrock': (('lat', 'lon'), (dr-ssoil).data)},
                            coords={'lat': ds['lat'], 'lon': ds['lon']})
        output_ds1.to_netcdf(f'{data_path}D/Dbedrock_{j+2003}_tmp1.nc4')

        output_ds2 = xr.Dataset({'FD': (('lat', 'lon'), use_dbedrock_first_day)},
                            coords={'lat': ds['lat'], 'lon': ds['lon']})
        output_ds2.to_netcdf(f'{data_path}D/D_FD_{j+2003}_tmp1.nc4')

        output_ds3 = xr.Dataset({'Duration': (('lat', 'lon'), use_dbedrock_duration)},
                            coords={'lat': ds['lat'], 'lon': ds['lon']})
        output_ds3.to_netcdf(f'{data_path}D/D_Duration_{j+2003}_tmp1.nc4')

    output_ds4 = xr.Dataset({'Period': (('time', 'lat', 'lon'), use_dbedrock_period)},
                        coords={'time': ds['time'], 'lat': ds['lat'], 'lon': ds['lon']})
    output_ds4.to_netcdf(f'{data_path}D/D_Period_tmp1.nc4')

    ds.close()
    ds2.close()
    ds3.close()

if __name__=='__main__':
    cal_D()